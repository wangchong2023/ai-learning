from typing import Annotated, Sequence, List
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class MultiAgentState(TypedDict):
    """
    多智能体协作状态。
    
    Attributes:
        messages: 共享的对话历史。
        next_agent: 下一个执行的 Agent 名称。
        research_notes: 研究员收集到的原始资料（非结构化）。
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_agent: str
    research_notes: List[str]
