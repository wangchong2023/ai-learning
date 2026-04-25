from typing import Any
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from .state import AgentState
from .nodes import agent_reasoning_node, tool_execution_node

def create_workflow() -> StateGraph:
    """
    构建智能体的有向图拓扑结构。
    
    该函数定义了节点及其连接逻辑：
    1. reasoning (思考): 决定执行动作。
    2. tools (执行): 运行具体工具。
    
    Returns:
        StateGraph: 未编译的图对象。
    """
    workflow = StateGraph(AgentState)
    
    # 注册节点
    workflow.add_node("agent", agent_reasoning_node)
    workflow.add_node("tools", tool_execution_node)
    
    # 定义边与逻辑流
    workflow.add_edge(START, "agent")
    
    # 条件路由：根据 agent 的输出决定是进入 tools 还是直接结束
    workflow.add_conditional_edges("agent", tools_condition)
    
    # 工具执行完成后，必须返回 agent 节点进行结果总结
    workflow.add_edge("tools", "agent")
    
    return workflow

def compile_with_hitl(workflow: StateGraph, memory: Any) -> Any:
    """
    带有人工干预机制（HITL）的图编译。
    
    Args:
        workflow: 构建好的 StateGraph。
        memory: 用于持久化会话状态的 Checkpointer 对象。
        
    Returns:
        CompiledGraph: 具备中断能力的已编译图对象。
        
    Note:
        interrupt_before=["tools"] 是核心安全开关。
        它保证了在进入 tools 节点执行任何代码前，系统会自动挂起并等待人工授权。
    """
    return workflow.compile(
        checkpointer=memory,
        # 核心：在工具节点执行前触发中断
        interrupt_before=["tools"]
    )
