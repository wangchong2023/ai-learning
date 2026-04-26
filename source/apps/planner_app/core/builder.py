from langgraph.graph import StateGraph, START, END
from .state import PlanExecuteState
from .nodes import planner_node, executor_node, replanner_node

def create_planner_graph():
    workflow = StateGraph(PlanExecuteState)
    
    # 添加核心节点
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("replanner", replanner_node)
    
    # 边连线逻辑
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "replanner")
    
    # 动态路由：如果复盘官给出了 response，就结束；否则打回执行官继续执行新计划
    def router(state: PlanExecuteState):
        if state.get("response"):
            return END
        else:
            return "executor"
            
    workflow.add_conditional_edges("replanner", router)
    
    return workflow.compile()
