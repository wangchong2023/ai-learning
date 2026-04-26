from typing import Dict, Any
from langgraph.prebuilt import ToolNode
from tools.common_tools import tools
from .state import AgentState
from utils.logger import agent_logger
from utils.factory import create_llm

# ==========================================
# 核心推理组件 (通过工厂初始化)
# ==========================================

llm = create_llm()
llm_with_tools = llm.bind_tools(tools)

async def agent_reasoning_node(state: AgentState) -> Dict[str, Any]:
    """Agent 推理节点：通过统一工厂创建的 LLM 进行决策"""
    agent_logger.info("🧠 正在分析对话上下文...")
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    
    if response.tool_calls:
        agent_logger.info(f"🎯 识别到工具调用: {[t['name'] for t in response.tool_calls]}")
    else:
        agent_logger.info("✍️ 生成最终回复。")
        
    return {"messages": [response]}

tool_execution_node = ToolNode(tools)
