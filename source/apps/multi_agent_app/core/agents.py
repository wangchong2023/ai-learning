from langchain_core.messages import HumanMessage, AIMessage
from utils.factory import create_llm
from utils.logger import agent_logger
from .state import MultiAgentState

llm = create_llm()

async def researcher_node(state: MultiAgentState) -> dict:
    """研究员节点：负责模拟资料搜索逻辑。"""
    last_user_msg = state["messages"][0].content
    agent_logger.info(f"🕵️ 研究员正在分析课题: {last_user_msg}")
    
    # 模拟“搜索并提取核心事实”的推理过程
    search_prompt = f"你是一个专业研究员。请针对课题 '{last_user_msg}' 提取出 2-3 个核心事实或研究维度，以帮助作家后续创作。只需输出事实要点。"
    response = await llm.ainvoke(search_prompt)
    
    # 将提取到的事实存入研究笔记
    research_content = [response.content]
    
    return {
        "research_notes": research_content,
        "next_agent": "writer",
        "messages": [AIMessage(content="✅ 我已完成深度调研，以下是我的研究简报，现移交给作家。")]
    }

async def writer_node(state: MultiAgentState) -> dict:
    """作家节点：负责基于研究笔记进行创作。"""
    agent_logger.info("✍️ 作家正在接入研究笔记进行深度创作...")
    
    notes = "\n".join(state.get("research_notes", []))
    prompt = f"你是一个资深作家。请基于以下专业研究笔记，写一段极具洞察力的分析短文：\n\n{notes}"
    
    response = await llm.ainvoke(prompt)
    
    return {
        "messages": [AIMessage(content=f"📝 【最终文案】\n\n{response.content}")],
        "next_agent": "finish"
    }
