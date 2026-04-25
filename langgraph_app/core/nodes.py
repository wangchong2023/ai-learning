from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from tools.common_tools import tools
from .state import AgentState
from utils.config import settings
from utils.logger import agent_logger

# 初始化集成配置的 LLM
llm = ChatOpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL,
    model=settings.LLM_MODEL,
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)

async def agent_reasoning_node(state: AgentState) -> Dict[str, Any]:
    """Agent 推理节点"""
    agent_logger.info("🧠 正在分析对话历史生成下一步决策...")
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    
    if response.tool_calls:
        agent_logger.info(f"🎯 识别到工具调用请求: {[t['name'] for t in response.tool_calls]}")
    else:
        agent_logger.info("✍️ 生成最终答复内容。")
        
    return {"messages": [response]}

tool_execution_node = ToolNode(tools)
