import operator
from typing import Annotated, List, Tuple, TypedDict

class PlanExecuteState(TypedDict):
    """
    Plan-and-Execute 状态机
    
    Attributes:
        input: 用户原始请求。
        plan: 当前未执行的步骤清单。
        past_steps: 已执行的步骤及结果，使用 operator.add 自动追加。
        response: 最终输出的答案。
    """
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple[str, str]], operator.add]
    response: str
