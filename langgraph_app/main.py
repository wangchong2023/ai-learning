import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_PATH = PROJECT_ROOT / "env" / ".env"
if ENV_PATH.exists(): load_dotenv(ENV_PATH)

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from .core.builder import create_workflow, compile_with_hitl

DB_PATH = ":memory:"

async def handle_stream(app, input_data, config):
    async for event in app.astream(input_data, config, stream_mode="values"):
        if not event.get("messages"): continue
        latest_msg = event["messages"][-1]
        if isinstance(latest_msg, AIMessage) and latest_msg.tool_calls:
            for tc in latest_msg.tool_calls:
                print(f"🛡️ [审批请求]: 执行 -> {tc['name']} (参数: {tc['args']})")
        elif isinstance(latest_msg, ToolMessage):
             print(f"⚙️ [Tool执行]: 结果 = {latest_msg.content}")
             
async def main():
    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as memory:
        workflow = create_workflow()
        app = compile_with_hitl(workflow, memory)
        config = {"configurable": {"thread_id": "hitl_verify"}}
        print("=" * 50)
        print("🌟 LangGraph HITL 模式恢复版 🌟")
        print("=" * 50)
        while True:
            try:
                user_input = input("\n[您]: ")
                if user_input.lower() in ['quit', 'exit']: break
                await handle_stream(app, {"messages": [HumanMessage(content=user_input)]}, config)
                while True:
                    state = await app.aget_state(config)
                    if state.next and "tools" in state.next:
                        approval = input("\n👉 是否授权执行？(y/n): ")
                        if approval.lower() == 'y':
                            await handle_stream(app, None, config)
                        else: break
                    else:
                        if state.values.get("messages"):
                            print(f"\n[AI助手]: {state.values['messages'][-1].content}")
                        break
            except Exception: break

if __name__ == "__main__":
    asyncio.run(main())
