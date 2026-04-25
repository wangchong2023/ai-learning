from langchain_core.messages import HumanMessage, AIMessage
from utils.factory import create_llm
from utils.logger import agent_logger
from .state import MultiAgentState

llm = create_llm()

async def researcher_node(state: MultiAgentState) -> dict:
    """研究员节点：负责模拟资料搜索逻辑。"""
    agent_logger.info("🕵️ 研究员正在深入检索相关领域的资料...")
    
    # 模拟搜索过程
    last_msg = state["messages"][-1].content
    research_content = [
        f"关于 '{last_msg}' 的核心事实 A：数据支撑点 1",
        f"关于 '{last_msg}' 的核心事实 B：关键历史背景"
    ]
    
    return {
        "research_notes": research_content,
        "next_agent": "writer",
        "messages": [AIMessage(content="我已完成初步调研，收集到了核心事实，准备移交给作家进行撰写。")]
    }

async def writer_node(state: MultiAgentState) -> dict:
    """作家节点：负责基于研究笔记进行创作。"""
    agent_logger.info("✍️ 作家正在根据研究资料进行深度创作...")
    
    notes = "\n".join(state.get("research_notes", []))
    prompt = f"请基于以下研究笔记写一段精简的分析：\n{notes}"
    
    response = await llm.ainvoke(prompt)
    
    return {
        "messages": [AIMessage(content=f"【创作完成】\n{response.content}")],
        "next_agent": "finish"
    }
