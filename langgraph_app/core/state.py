from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    定义图的状态结构。
    使用 add_messages reducer 确保消息是追加而非覆盖。
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
