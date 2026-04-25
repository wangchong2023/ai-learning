from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    智能体状态定义。
    
    Attributes:
        messages: 对话历史记录。
            使用 Annotated 包装并注入 add_messages 策略，
            确保新的消息会自动追加到序列末尾，而不是覆盖旧消息。
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
