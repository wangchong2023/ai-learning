import asyncio
import readline
from planner_app.core.builder import create_planner_graph
from utils.logger import agent_logger

async def main():
    print("🚀 启动深度规划实验室 (Plan-and-Execute Lab)")
    print("📢 运行模式：高级规划与渐进式执行")
    print("✨ 示例指令：")
    print("   - '先总结2023年的AI发展，再基于此预测2024年的趋势'")
    print("=" * 50)
    
    app = create_planner_graph()
    
    while True:
        try:
            user_input = input("\n💡 [深度规划] 请输入您的复杂指令 (输入 'quit' 退出): ")
            if user_input.lower() in ['quit', 'exit']: break
            if not user_input.strip(): continue
            
            state_input = {"input": user_input, "past_steps": []}
            
            # 使用流式输出以实时观测内部运行
            async for event in app.astream(state_input, stream_mode="updates"):
                for node_name, node_state in event.items():
                    if node_name == "planner":
                        print(f"\n📋 [计划生成]:")
                        for i, step in enumerate(node_state["plan"]):
                            print(f"   {i+1}. {step}")
                    elif node_name == "executor":
                        past = node_state["past_steps"][-1]
                        print(f"\n✅ [执行完成]: 步骤 '{past[0]}'")
                    elif node_name == "replanner" and "response" in node_state:
                        print(f"\n🎉 [最终答复]:\n{node_state['response']}")
                    elif node_name == "replanner":
                        print(f"\n🧐 [计划更新]:")
                        for i, step in enumerate(node_state["plan"]):
                            print(f"   {i+1}. {step}")
                        
        except Exception as e:
            print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 已安全退出深度规划实验室。")
