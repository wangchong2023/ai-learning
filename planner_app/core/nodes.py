from pydantic import BaseModel, Field
from typing import List, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.factory import create_llm
from utils.logger import agent_logger
from .state import PlanExecuteState

# ================================
# 数据结构定义
# ================================
class Plan(BaseModel):
    """规划方案"""
    steps: List[str] = Field(description="解决该问题所需的具体步骤，按逻辑顺序排列。")

class ResponseOrPlan(BaseModel):
    """复盘结论：要么给出最终答案，要么给出修改后的新计划"""
    response: str = Field(description="如果问题已解决，请给出对用户的最终回答。如果未解决，留空字符串。")
    plan: List[str] = Field(description="如果未解决，给出的剩余步骤清单。")

llm = create_llm(temperature=0)

# ================================
# 核心节点实现
# ================================

async def planner_node(state: PlanExecuteState) -> dict:
    """战略家节点：负责生成初始计划"""
    agent_logger.info("🧠 战略家正在进行深度规划与任务拆解...")
    
    parser = JsonOutputParser(pydantic_object=Plan)
    
    planner_prompt = ChatPromptTemplate.from_template(
        "针对用户的目标，请给出一个严格按步骤执行的计划清单。\n"
        "要求：步骤颗粒度要小，不要包含过于抽象的词汇。\n"
        "目标：{objective}\n\n"
        "{format_instructions}"
    )
    
    planner_chain = planner_prompt | llm | parser
    plan = await planner_chain.ainvoke({
        "objective": state["input"],
        "format_instructions": parser.get_format_instructions()
    })
    
    return {"plan": plan["steps"]}

async def executor_node(state: PlanExecuteState) -> dict:
    """执行官节点：只专注执行清单上的第一步"""
    current_step = state["plan"][0]
    agent_logger.info(f"⚙️ 执行官正在处理当前步骤: {current_step}")
    
    executor_prompt = ChatPromptTemplate.from_template(
        "你是一个执行官。你正在解决总目标：'{objective}'。\n"
        "当前你需要执行的步骤是：'{step}'。\n"
        "请提供该步骤的执行结果。"
    )
    
    chain = executor_prompt | llm
    result = await chain.ainvoke({"objective": state["input"], "step": current_step})
    
    return {
        "past_steps": [(current_step, result.content)],
        "plan": state["plan"][1:] # 剔除已完成的第一步
    }

async def replanner_node(state: PlanExecuteState) -> dict:
    """复盘官节点：决定是否结束，或是否需要修改剩余计划"""
    agent_logger.info("🧐 复盘官正在审视进度...")
    
    parser = JsonOutputParser(pydantic_object=ResponseOrPlan)
    
    replanner_prompt = ChatPromptTemplate.from_template(
        "你的目标是：{objective}。\n"
        "我们已经完成的步骤及结果如下：\n{past_steps}\n"
        "请评估：现有结果是否足以回答用户的原始目标？\n"
        "如果可以，请在 response 字段中输出最终答复，并清空 plan。\n"
        "如果还不够，或者遇到了死胡同，请在 plan 字段中重新规划剩余的步骤。\n\n"
        "{format_instructions}"
    )
    
    past_steps_str = "\n".join([f"步骤: {s}\n结果: {r}" for s, r in state.get("past_steps", [])])
    
    chain = replanner_prompt | llm | parser
    output = await chain.ainvoke({
        "objective": state["input"], 
        "past_steps": past_steps_str,
        "format_instructions": parser.get_format_instructions()
    })
    
    if output.get("response"):
        return {"response": output["response"], "plan": []}
    else:
        return {"plan": output.get("plan", [])}

