from langgraph.graph import StateGraph, START, END
from .state import MultiAgentState
from .agents import researcher_node, writer_node

def create_multi_agent_graph():
    """构建多智能体协作流图。"""
    workflow = StateGraph(MultiAgentState)
    
    # 添加节点
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    
    # 定义连接逻辑
    workflow.add_edge(START, "researcher")
    
    # 动态路由：根据 next_agent 字段决定去向
    def router(state: MultiAgentState):
        if state["next_agent"] == "writer":
            return "writer"
        return END

    workflow.add_conditional_edges("researcher", router)
    workflow.add_edge("writer", END)
    
    return workflow.compile()
