import os
import asyncio
import traceback
from pathlib import Path
from dotenv import load_dotenv

# 确保在导入核心模块前加载环境
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_PATH = PROJECT_ROOT / "env" / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from .core.builder import create_workflow, compile_with_hitl

DB_PATH = ":memory:"

async def handle_stream(app, input_data, config):
    """处理并打印流式事件"""
    async for event in app.astream(input_data, config, stream_mode="values"):
        if not event or "messages" not in event: continue
        latest_msg = event["messages"][-1]
        
        # 识别 Agent 的工具调用意图
        if isinstance(latest_msg, AIMessage) and latest_msg.tool_calls:
            for tc in latest_msg.tool_calls:
                print(f"🛡️ [审批请求]: Agent 申请执行 -> {tc['name']} (参数: {tc['args']})")
        # 识别工具的执行结果
        elif isinstance(latest_msg, ToolMessage):
             print(f"⚙️ [Tool执行]: 响应结果 = {latest_msg.content[:50]}...")

async def main():
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 错误: 未检测到 DEEPSEEK_API_KEY，请检查 env/.env 文件")
        return

    print("🚀 正在初始化智能体引擎...")
    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as memory:
        workflow = create_workflow()
        app = compile_with_hitl(workflow, memory)
        
        config = {"configurable": {"thread_id": "hitl_verify_session"}}

        print("=" * 50)
        print("🌟 LangGraph 模块化智能体 (HITL 模式) 🌟")
        print("=" * 50)

        while True:
            try:
                user_input = input("\n[您]: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                if not user_input.strip(): continue

                # 1. 启动推理流
                await handle_stream(app, {"messages": [HumanMessage(content=user_input)]}, config)
                
                # 2. 循环处理可能的审批中断
                while True:
                    state = await app.aget_state(config)
                    # 检查是否有待执行的工具节点（被 interrupt_before 拦截）
                    if state.next and "tools" in state.next:
                        approval = input("\n👉 [人工审批] 是否允许工具执行？(y/n): ")
                        if approval.lower() == 'y':
                            print("✅ 审批通过，正在执行工具...")
                            await handle_stream(app, None, config)
                        else:
                            print("🚫 审批拒绝，停止该轮操作。")
                            break
                    else:
                        # 流程正常结束，打印最终回复
                        if state.values.get("messages"):
                            final_answer = state.values["messages"][-1]
                            if isinstance(final_answer, AIMessage) and not final_answer.tool_calls:
                                print(f"\n[AI助手]: {final_answer.content}")
                        break
                        
            except Exception as e:
                print(f"❌ 运行中发生错误:\n{traceback.format_exc()}")
                # 不要 break，允许用户重试

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 已安全退出智能体应用。")
