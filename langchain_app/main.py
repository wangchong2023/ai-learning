import os
import asyncio
from typing import Annotated, Sequence
from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# ⚠️ 注意: 该文件为基础演示，已适配统一工具库
# ==========================================

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# 引用统一工具库
from tools.common_tools import tools

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_PATH = PROJECT_ROOT / "env" / ".env"
DB_PATH = ":memory:"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

class AgentState(Annotated[dict, "State"]):
    messages: Annotated[Sequence[BaseMessage], add_messages]

async def agent_reasoning_node(state: dict):
    messages = state["messages"]
    llm = ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
        temperature=0
    )
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
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 未设置 DEEPSEEK_API_KEY")
        return

    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as memory:
        app = create_app(memory)
        config = {"configurable": {"thread_id": "legacy_verify"}}
        print("🌟 LangChain 基础演示运行中...")
        
        while True:
            user_input = input("\n[您]: ")
            if user_input.lower() in ['quit', 'exit']: break
            
            async for event in app.astream(
                {"messages": [HumanMessage(content=user_input)]},
                config,
                stream_mode="values"
            ):
                msg = event["messages"][-1]
                if isinstance(msg, AIMessage) and msg.tool_calls:
                    print(f"🤖 [Agent]: 正在调用工具...")
                elif isinstance(msg, ToolMessage):
                    print(f"⚙️ [Tool执行]: 结果已获得")

            state = await app.aget_state(config)
            print(f"\n[AI助手]: {state.values['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())
