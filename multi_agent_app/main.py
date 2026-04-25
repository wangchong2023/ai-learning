import asyncio
from langchain_core.messages import HumanMessage
from multi_agent_app.core.builder import create_multi_agent_graph

async def main():
    print("🚀 启动多智能体协作实验室 (Multi-Agent Lab)")
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
                # 打印最新的智能体回复
                msg = event["messages"][-1]
                if msg.content:
                    print(f"\n{msg.content}")
                    
        except KeyboardInterrupt:
            print("\n👋 已安全退出多智能体实验室。")
            break
        except Exception as e:
            print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())
