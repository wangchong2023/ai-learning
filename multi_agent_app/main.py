import asyncio
from langchain_core.messages import HumanMessage
from multi_agent_app.core.builder import create_multi_agent_graph

async def main():
    print("🚀 启动多智能体协作实验室 (Multi-Agent Lab)")
    print("📢 运行模式：接力协作 (Researcher -> Writer)")
    print("=" * 50)
    
    app = create_multi_agent_graph()
    
    while True:
        try:
            user_input = input("\n[您]: ")
            if user_input.lower() in ['quit', 'exit']: break
            if not user_input.strip(): continue
            
            # 执行多智能体协作
            state_input = {"messages": [HumanMessage(content=user_input)], "research_notes": []}
            async for event in app.astream(state_input, stream_mode="values"):
                if not event or "messages" not in event: continue
                # 获取最新产生的消息
                msg = event["messages"][-1]
                # 仅打印 AI 的新回复
                if msg.content and not isinstance(msg, HumanMessage):
                    print(f"\n{msg.content}")
                    
        except Exception as e:
            print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 已安全退出多智能体实验室。")
