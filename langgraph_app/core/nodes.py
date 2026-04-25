import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from tools.common_tools import tools
from .state import AgentState

# 初始化 LLM
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)

async def agent_reasoning_node(state: AgentState):
    """异步推理节点"""
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}

# 预置工具执行节点
tool_execution_node = ToolNode(tools)
