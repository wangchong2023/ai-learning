import os
import asyncio
import readline
from typing import Annotated, Sequence
from pathlib import Path

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# 引入项目基础设施
from tools.common_tools import tools
from utils.config import settings
from utils.logger import agent_logger
from utils.factory import create_llm

class AgentState(Annotated[dict, "State"]):
    messages: Annotated[Sequence[BaseMessage], add_messages]

async def agent_reasoning_node(state: dict):
    """基础推理节点"""
    agent_logger.info("LangChain 基础演示：正在推理...")
    messages = state["messages"]
    # 使用工厂创建统一配置的 LLM
    llm = create_llm()
    llm_with_tools = llm.bind_tools(tools)
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}

def create_app(memory):
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_reasoning_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    return workflow.compile(checkpointer=memory)

async def main():
    agent_logger.info("🌟 LangChain 基础演示启动...")
    
    async with AsyncSqliteSaver.from_conn_string(settings.SQLITE_DB_PATH) as memory:
        app = create_app(memory)
        config = {"configurable": {"thread_id": "legacy_verify"}}
        
        while True:
            try:
                user_input = input("\n💬 [基础演示] 请输入您的问题 (输入 'quit' 退出): ")
                if user_input.lower() in ['quit', 'exit']: break
                
                async for event in app.astream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config,
                    stream_mode="values"
                ):
                    msg = event["messages"][-1]
                    if isinstance(msg, AIMessage) and msg.tool_calls:
                        agent_logger.info("机器人正在思考并准备调用工具...")
                
                state = await app.aget_state(config)
                print(f"\n[AI助手]: {state.values['messages'][-1].content}")
            except Exception as e:
                agent_logger.error(f"发生错误: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 已安全退出基础演示应用。")
