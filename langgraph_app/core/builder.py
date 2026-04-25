from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from .state import AgentState
from .nodes import agent_reasoning_node, tool_execution_node

def create_workflow():
    """构建工作流拓扑"""
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_reasoning_node)
    workflow.add_node("tools", tool_execution_node)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    return workflow

def compile_with_hitl(workflow, memory):
    """带审批流的编译"""
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["tools"]
    )
