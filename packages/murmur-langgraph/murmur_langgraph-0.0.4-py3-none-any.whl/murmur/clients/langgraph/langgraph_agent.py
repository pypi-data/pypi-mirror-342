import logging
from types import ModuleType
from typing import Any, Literal

from langchain_core.globals import set_debug
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.messages.base import BaseMessage
from pydantic import Field, model_validator

from murmur.build import ActivateAgent
from murmur.utils.client_options import ClientOptions
from murmur.utils.instructions_handler import InstructionsHandler
from murmur.utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

if logger.getEffectiveLevel() <= logging.DEBUG:
    set_debug(True)


class LangGraphOptions(ClientOptions):
    """Configuration options specific to LangGraphAgent.

    Inherits common options from ClientOptions and extends them with LangGraph-specific settings.
    Adapts to match LangGraph's option types based on their supported language model configurations.

    Attributes:
        instructions (InstructionsMode): Controls instruction handling strategy.
            Inherited from ClientOptions.
        parallel_tool_calls (bool | None): Whether to allow multiple tool calls to execute
            in parallel. None is transformed to False.
        tool_choice (dict[str, str] | Literal['any', 'auto'] | str | None): Controls how
            the model selects and uses tools. None is allowed and passed through.
    """

    parallel_tool_calls: bool | None = Field(
        default=None, description='Whether to allow multiple tool calls to execute in parallel'
    )
    tool_choice: dict[str, str] | Literal['any', 'auto'] | str | None = Field(
        default=None, description='Controls whether and how the model uses tools'
    )

    @model_validator(mode='after')
    def transform_none_values(self) -> 'LangGraphOptions':
        """Transform None values to their appropriate defaults after validation."""
        # Only transform if the field was explicitly set
        if 'parallel_tool_calls' in self.__pydantic_fields_set__:
            self.parallel_tool_calls = True if self.parallel_tool_calls is None else self.parallel_tool_calls

        # tool_choice can remain None if set to None
        return self

    def get_bind_tools_kwargs(self) -> dict[str, Any]:
        """Get kwargs for bind_tools with proper handling of defaults and None values.

        Returns:
            Dictionary of non-None arguments to pass to bind_tools
        """
        # Only include LangGraph-specific fields, excluding parent class fields
        langgraph_fields = {'parallel_tool_calls': self.parallel_tool_calls, 'tool_choice': self.tool_choice}
        return {k: v for k, v in langgraph_fields.items() if v is not None}


class LangGraphAgent:
    """Agent for managing language graph operations.

    Supports both ActivateAgent-based modules and traditional agent modules.
    If the input agent is an ActivateAgent, it will use its invoke functionality.
    """

    def __init__(
        self,
        agent: ModuleType,
        model: BaseChatModel,
        tools: list = [],
        instructions: list[str] | None = None,
        options: LangGraphOptions | None = None,
    ) -> None:
        """Initialize LangGraphAgent.

        Args:
            agent: Agent module (can be an ActivateAgent-based module)
            model: LangChain chat model
            tools: List of tool functions
            instructions: Optional custom instructions
            options: Configuration options
        """
        if not isinstance(model, BaseChatModel):
            raise TypeError('model must be an instance of BaseChatModel')

        # Common setup for all agent types
        self.agent_module = agent
        self.model = model
        self.tools = tools
        self.options = options or LangGraphOptions()
        self.instructions = instructions

        # Agent-specific setup
        self.is_activate_agent = hasattr(agent, 'invoke') and isinstance(agent, ActivateAgent)

    def invoke(self, messages: list[BaseMessage], **kwargs: Any) -> BaseMessage:
        """Process messages using either ActivateAgent or LangGraph workflow.

        Args:
            messages: List of messages to process
            **kwargs: Additional arguments (used for template variables in ActivateAgent and instructions)

        Returns:
            list[BaseMessage]: List of messages including agent's response for LangGraph

        Raises:
            ValueError: If messages list is empty or agent execution fails
        """
        if not messages:
            raise ValueError('Messages list cannot be empty')

        logger.debug(f'kwargs: {kwargs}')

        bound_model = self.model.bind_tools(self.tools, **self.options.get_bind_tools_kwargs())

        # Get system message content based on agent type
        if self.is_activate_agent:
            agent_response = self.agent_module.invoke(messages, **kwargs)
            if not agent_response.success:
                raise ValueError(f'Agent execution failed: {agent_response.error}')
            system_content = str(agent_response.value)
        else:
            instructions_handler = InstructionsHandler()
            system_content = instructions_handler.get_instructions(
                module=self.agent_module,
                provided_instructions=self.instructions,
                instructions_mode=self.options.instructions,
                **kwargs,
            )
            logger.debug(f'Generated instructions: {system_content[:100]}...')

        logger.debug(f'Invoking model with {len(messages)} messages')
        logger.debug(f'Instructions: {system_content}')

        all_messages = [SystemMessage(content=system_content)] + messages
        return bound_model.invoke(all_messages)
