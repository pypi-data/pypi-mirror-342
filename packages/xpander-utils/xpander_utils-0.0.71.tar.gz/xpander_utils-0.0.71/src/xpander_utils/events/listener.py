import json
from typing import Callable, List, Optional, Union, Awaitable
import asyncio
from aiosseclient import aiosseclient
from xpander_sdk import XpanderClient
import httpx
from .models.deployments import DeployedAsset
from .models.events import EventType, WorkerFinishedEvent
from .models.executions import AgentExecutionResult, AgentExecution, AgentExecutionStatus

EVENT_STREAMING_ENDPOINT = "{base}/{organization_id}/events"

ExecutionRequestHandler = Union[
    Callable[[AgentExecution], AgentExecutionResult],
    Callable[[AgentExecution], Awaitable[AgentExecutionResult]]
]

class XpanderEventListener:
    root_worker: DeployedAsset

    def __init__(
        self,
        api_key: str,
        agent_ids: List[str],
        base_url: Optional[str] = None,
        organization_id: Optional[str] = None,
        should_reset_cache: Optional[bool] = False,
        with_metrics_report: Optional[bool] = False
    ):
        """
        Initialize the XpanderEventListener with the provided API key and agent IDs.

        Args:
            api_key (str): The API key for authentication with xpander.ai.
            agent_ids (List[str]): The agent IDs to listen for events.
            base_url (Optional[str], optional): The base URL for the xpander.ai API. Defaults to None.
            organization_id (Optional[str], optional): The organization ID, if applicable. Defaults to None.
            should_reset_cache (Optional[bool], optional): Whether to reset the cache. Defaults to False.
            with_metrics_report (Optional[bool], optional): If to auto-report metrics (LLM & execution). Defaults to False.
        """
        should_pass_organization_id = base_url and not "inbound.stg" in base_url and not "inbound.xpander" in base_url
        self.xpander_client = XpanderClient(
            api_key=api_key,
            base_url=base_url,
            organization_id=organization_id if should_pass_organization_id else None,
            should_reset_cache=should_reset_cache
        )
        self.with_metrics_report = with_metrics_report
        self.organization_id = organization_id
        self.agents = agent_ids

    def is_not_inbound(self) -> bool:
        """
        Checks whether the base URL is not for an inbound environment.

        Returns:
            bool: True if not inbound, False otherwise.
        """
        return "inbound.xpander" not in self.xpander_client.configuration.base_url and \
               "inbound.stg.xpander" not in self.xpander_client.configuration.base_url

    def get_events_base(self) -> str:
        """
        Constructs the base URL for event streaming depending on the environment.

        Returns:
            str: The complete event streaming endpoint URL.
        """
        if self.is_not_inbound():
            return EVENT_STREAMING_ENDPOINT.format(
                base=self.xpander_client.configuration.base_url,
                organization_id=self.organization_id
            )

        is_stg = "stg.xpander" in self.xpander_client.configuration.base_url
        base = "https://agent-controller" + (".stg" if is_stg else "") + ".xpander.ai"
        return EVENT_STREAMING_ENDPOINT.format(base=base, organization_id=self.organization_id)

    def get_headers(self) -> dict:
        """
        Returns headers for authenticated requests.

        Returns:
            dict: Dictionary containing API key header.
        """
        return {"x-api-key": self.xpander_client.configuration.api_key}

    async def _release_worker(self, worker_id: str):
        """
        Sends request to release the worker by ID.

        Args:
            worker_id (str): The ID of the worker to be released.
        """
        try:
            url = f"{self.get_events_base()}/{worker_id}"
            async with httpx.AsyncClient() as client:
                await client.post(
                    url,
                    headers=self.get_headers(),
                    json=WorkerFinishedEvent().model_dump_safe()
                )
        except Exception as e:
            raise Exception(f"Failed to release worker - {str(e)}")

    async def _update_execution_result(self, execution_id: str, execution_result: AgentExecutionResult):
        """
        Updates the execution result for the specified execution ID.

        Args:
            execution_id (str): The ID of the execution to update.
            execution_result (AgentExecutionResult): The result of the agent execution.
        """
        try:
            base = self.get_events_base().replace("/events", "/agent-execution")
            url = f"{base}/{execution_id}/finish"
            async with httpx.AsyncClient() as client:
                await client.patch(
                    url,
                    headers=self.get_headers(),
                    json={
                        "result": execution_result.result,
                        "status": AgentExecutionStatus.Completed if execution_result.is_success else AgentExecutionStatus.Error
                    }
                )
        except Exception as e:
            raise Exception(f"Failed to report execution result - {str(e)}")

    async def _mark_execution_as_executing(self, execution_id: str):
        """
        Marks the execution as 'executing' for the given ID.

        Args:
            execution_id (str): The execution ID to update.
        """
        try:
            base = self.get_events_base().replace("/events", "/agent-execution")
            url = f"{base}/{execution_id}/finish"
            async with httpx.AsyncClient() as client:
                await client.patch(
                    url,
                    headers=self.get_headers(),
                    json={
                        "result": "",
                        "status": AgentExecutionStatus.Executing.value.lower()
                    }
                )
        except Exception as e:
            raise Exception(f"Failed to report execution result - {str(e)}")

    async def _handle_agent_execution(
        self,
        agent_worker: DeployedAsset,
        execution_task: AgentExecution,
        on_execution_request: ExecutionRequestHandler
    ):
        """
        Handles the execution lifecycle for a specific agent execution task.

        Args:
            agent_worker (DeployedAsset): The deployed agent worker.
            execution_task (AgentExecution): The execution task to be processed.
            on_execution_request (ExecutionRequestHandler): The callback to handle the execution logic.
        """
        execution_result = AgentExecutionResult(result="")
        try:
            await self._mark_execution_as_executing(execution_id=execution_task.id)
            if asyncio.iscoroutinefunction(on_execution_request):
                execution_result = await on_execution_request(execution_task)
            else:
                loop = asyncio.get_running_loop()
                execution_result = await loop.run_in_executor(
                    None, lambda: on_execution_request(execution_task)
                )
        except Exception as e:
            execution_result.is_success = False
            execution_result.result = f"Error: {str(e)}"
        finally:
            await self._release_worker(worker_id=agent_worker.id)
            await self._update_execution_result(
                execution_id=execution_task.id,
                execution_result=execution_result
            )

    async def _register_agent_worker(
        self,
        agent_id: str,
        on_execution_request: ExecutionRequestHandler
    ):
        """
        Registers and listens for events from an individual agent.

        Args:
            agent_id (str): The ID of the agent to register.
            on_execution_request (ExecutionRequestHandler): Callback function to handle execution requests.
        """
        try:
            url = f"{self.get_events_base()}/{self.root_worker.id}/{agent_id}"
            agent_worker: DeployedAsset = None

            async for event in aiosseclient(
                url=url,
                headers=self.get_headers(),
                raise_for_status=True
            ):
                if event.event == EventType.WorkerRegistration:
                    agent_worker = DeployedAsset(**json.loads(event.data))
                elif event.event == EventType.AgentExecution:
                    execution_task = AgentExecution(**json.loads(event.data))
                    asyncio.create_task(
                        self._handle_agent_execution(
                            agent_worker=agent_worker,
                            execution_task=execution_task,
                            on_execution_request=on_execution_request
                        )
                    )
        except Exception as e:
            raise Exception("failed to register agent worker", str(e))

    async def _register_parent_worker(self) -> DeployedAsset:
        """
        Registers the root worker for the current execution context.

        Returns:
            DeployedAsset: The root deployed worker.
        """
        try:
            url = self.get_events_base()
            async for event in aiosseclient(
                url=url,
                headers=self.get_headers(),
                raise_for_status=True
            ):
                if event.event == EventType.WorkerRegistration:
                    self.root_worker = DeployedAsset(**json.loads(event.data))
                    return self.root_worker
        except Exception as e:
            raise Exception("failed to register root worker", str(e))

    def register(self, on_execution_request: ExecutionRequestHandler):
        """
        Registers all agent workers and the root worker to handle event streams.

        Args:
            on_execution_request (ExecutionRequestHandler): 
                A callable function that takes an AgentExecution and returns an AgentExecutionResult.
        """
        async def _main():
            await self._register_parent_worker()
            tasks = [
                asyncio.create_task(
                    self._register_agent_worker(agent_id=agent_id, on_execution_request=on_execution_request)
                )
                for agent_id in self.agents
            ]
            await asyncio.gather(*tasks)

        asyncio.run(_main())
