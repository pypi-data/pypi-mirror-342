from __future__ import annotations
import uuid
import logging
import pandas as pd
import requests
import re
from typing import Iterator
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from opentelemetry import trace
from opentelemetry.trace import Span
from .exceptions import IICSAPIException
from .nodes.component import ComponentNode

tracer = trace.get_tracer("IICSAPI")

def _camel_to_snake(name: str) -> str:
    """Convert CamelCase or camelCase to snake_case."""
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class IICSAPI:
    def __init__(
        self,
        provider_url: str,
        pod: str,
        username: str,
        password: str
    ) -> None:
        """
        Initializes the IICSAPI client with the provided credentials and URLs.
        
        Args:
            provider_url (str): The base URL for the Informatica Cloud provider.
            pod (str): The pod name for the Informatica Cloud instance.
            username (str): The username for authentication.
            password (str): The password for authentication.
            
        Raises:
            IICSAPIException: If the login fails or if any other API call fails.
            
        Example:
        ```python
            iicsClient = IICSAPI(
                username="my_username",
                password="my_password",
                pod="use6", # see Informatica Cloud documentation for pod names
                provider_url="https://dm-us.informaticacloud.com" # see Informatica Cloud documentation for provider URLs
            )

            # Get the latest run for a specific taskflow
            latest_run = iicsClient.get_tf_audit_logs("123456789012345678")

            # Convert the result pandas DataFrame to a CSV
            latest_run.to_csv("audit_log.csv", index=False)
        ```
        """
        
        self._client_version = "2.0.3"
        
        # Validate the username and password
        if not username or not password:
            raise IICSAPIException("Username and password cannot be empty")
            
        # Validate the provider URL
        if not provider_url.startswith("https://"):
            raise IICSAPIException("Provider URL must start with 'https://'")
            
        if provider_url.endswith("/"):
            # remove trailing slash
            provider_url = provider_url[:-1]
            
        if not re.match(r"https://[\w-]+\.informaticacloud\.com", provider_url):
            raise IICSAPIException("Invalid provider URL format. Must be like 'https://dm-us.informaticacloud.com'")
        
        self.username = username
        self.password = password
        self.login_url = f"{provider_url}/saas/public/core/v3/login"

        pre_pod_provider_url = provider_url.replace('https://', '')
        self.monitor_url = (
            f"https://{pod}.{pre_pod_provider_url}"  \
            "/active-bpel/services/tf/status"
        )

        self.request_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.session_id = self._login()
        self.request_headers['INFA-SESSION-ID'] = self.session_id

        self.logger = self._init_logger()
        
        self.logger.info("Informatica Cloud API Client v%s", self._client_version)

    @staticmethod
    def _init_logger() -> logging.Logger:
        """
        Initializes the logger for the IICSAPI class.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=(
            retry_if_exception_type(IICSAPIException) |
            retry_if_exception_type(requests.RequestException)
        )
    )
    def _login(self) -> str:
        """
        Logs in to the IICS API and returns the session ID.
        """
        with tracer.start_as_current_span("IICSAPI._login") as span:
            span.set_attribute("username", self.username)
            response = requests.post(
                self.login_url,
                headers=self.request_headers,
                json={'username': self.username, 'password': self.password},
                timeout=10
            )
            if response.status_code == 200:
                session = response.json()['userInfo']['sessionId']
                return session
            else:
                raise IICSAPIException(
                    f"Failed to login: {response.status_code} {response.text}"
                )

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(
            retry_if_exception_type(IICSAPIException) |
            retry_if_exception_type(requests.RequestException)
        )
    )
    def get_latest_run(self, run_id: str) -> list[dict]:
        """
        Retrieves the output of the taskflow monitor for the specific run.
        """
        with tracer.start_as_current_span("IICSAPI.get_latest_run") as span:
            span.set_attribute("run_id", run_id)
            params = {"runId": run_id, "rowLimit": 50}
            response = requests.get(
                self.monitor_url,
                params=params,
                headers=self.request_headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise IICSAPIException(
                    f"Failed to get monitor output: {response.status_code} {response.text}"
                )

    def _get_tf_nodes(self, root_run_id: str) -> Iterator[ComponentNode]:
        """
        Yields each unique node in depth-first order, de-duped via each child's unique UUID.
        """
        with tracer.start_as_current_span("IICSAPI._get_tf_nodes") as span:
            span.set_attribute("root_run_id", root_run_id)
            seen_assets: set[str] = set()
            stack = [
                ComponentNode(
                    run_id=root_run_id,
                    asset_type="TASKFLOW",
                    parent_id=None,
                    depth=0,
                    root=None
                )
            ]

            while stack:
                node = stack.pop()
                self.logger.debug(
                    f"Popped → run_id={node.run_id}, "
                    f"type={node.asset_type}, depth={node.depth}"
                )

                if node.asset_type == "TASKFLOW":
                    try:
                        raw = self.get_latest_run(node.run_id)[0]
                    except IICSAPIException as e:
                        self.logger.error(
                            f"Fetch failed for {node.run_id}: {e}"
                        )
                    else:
                        # populate TASKFLOW fields using camel_to_snake mapping
                        for key in [
                            'assetName', 'duration', 'startTime',
                            'endTime', 'updateTime', 'status',
                            'location', 'runtimeEnv', 'runtimeEnvName',
                            'startedBy', 'subtasks'
                        ]:
                            attr = _camel_to_snake(key)
                            setattr(node, attr, raw[key])

                        # Create a unique ID for the node based on its asset name and start time
                        
                        new_id = uuid.uuid5(uuid.NAMESPACE_DNS, f"{node.asset_name}_{node.start_time}_{node.run_id}")
                        node.id = str(new_id)
                         
                        node.error_message  = raw.get('errorMessage', '')
                        node.errored_rows   = raw.get('erroredRows', 0)
                        node.rows_processed = raw.get('rowsProcessed', 0)
                        node.parent_id      = node.parent_id
                        node.root           = node.root or node
                        node.children       = []

                        # build & push children
                        for c in (
                            raw.get('subtaskDetails', {})
                               .get('details', {})
                               .get('tasks', [])
                        ):
                            child_node = ComponentNode(
                                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{c['assetName']}_{c['startTime']}_{c['runId']}")),
                                run_id=str(c['runId']),
                                asset_name=c['assetName'],
                                asset_type=c['assetType'],
                                duration=c['duration'],
                                start_time=c['startTime'],
                                end_time=c['endTime'],
                                update_time=c['updateTime'],
                                status=c['status'],
                                error_message=c.get('errorMessage',''),
                                errored_rows=c.get('erroredRows',0),
                                location=c['location'],
                                rows_processed=c.get('rowsProcessed',0),
                                runtime_env=c['runtimeEnv'],
                                runtime_env_name=c['runtimeEnvName'],
                                started_by=c['startedBy'],
                                subtasks=c.get('subtasks',0),
                                parent_id=node.run_id,
                                depth=node.depth+1,
                                root=node.root
                            )
                            node.children.append(child_node)
                            if child_node.asset_type == 'TASKFLOW':
                                stack.append(child_node)
                            if child_node.id not in seen_assets:
                                seen_assets.add(child_node.id)
                                yield child_node

                if node.id not in seen_assets:
                    seen_assets.add(node.id)
                    yield node

    def _convert_node_graph_to_df(
        self,
        nodes: Iterator[ComponentNode]
    ) -> pd.DataFrame:
        """
        Converts nodes into a pandas DataFrame.
        """
        with tracer.start_as_current_span("IICSAPI._convert_node_graph_to_df") as span:
            records: list[dict] = []
            for node in nodes:
                records.append({
                    'id': node.id,
                    'asset_name': node.asset_name,
                    'asset_type': node.asset_type,
                    'duration': node.duration,
                    'end_time': node.end_time,
                    'error_message': node.error_message,
                    'errored_rows': node.errored_rows,
                    'location': node.location,
                    'rows_processed': node.rows_processed,
                    'run_id': node.run_id,
                    'runtime_env': node.runtime_env,
                    'runtime_env_name': node.runtime_env_name,
                    'started_by': node.started_by,
                    'start_time': node.start_time,
                    'status': node.status,
                    'subtasks': node.subtasks,
                    'update_time': node.update_time,
                    'parent_id': node.parent_id,
                    'root_id': node.root.run_id if node.root else node.run_id,
                    'depth': node.depth,
                })
            return pd.DataFrame.from_records(records)

    def get_tf_audit_logs(
        self,
        root_run_id: str
    ) -> pd.DataFrame:
        """
        Retrieves audit logs for a taskflow and its subtasks.
        """
        with tracer.start_as_current_span("IICSAPI.get_tf_audit_logs") as span:
            span.set_attribute("root_run_id", root_run_id)
            nodes = self._get_tf_nodes(root_run_id)
            df = self._convert_node_graph_to_df(nodes)
            return df

# Example Usage:
# iicsClient = IICSAPI(
#     username="my_username",
#     password="my_password",
#     pod="use6", # see Informatica Cloud documentation for pod names
#     provider_url="https://dm-us.informaticacloud.com" # see Informatica Cloud documentation for provider URLs
# )

# # Get the latest run for a specific taskflow
# latest_run = iicsClient.get_tf_audit_logs("123456789012345678")

# # Convert the result pandas DataFrame to a CSV
# latest_run.to_csv("iics_audit.csv", index=False)