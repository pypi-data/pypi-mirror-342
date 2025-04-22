from datetime import datetime
from typing import Any

from pydantic import BaseModel

from ..enums import ConditionTypes


class Condition(BaseModel):
    type: ConditionTypes
    value: Any


def not_eq(val: Any) -> Condition:
    return Condition(
        type=ConditionTypes.NOT_EQ,
        value=val,
    )


def gt_eq(val: Any) -> Condition:
    return Condition(
        type=ConditionTypes.GT_EQ,
        value=val,
    )


def le_eq(val: Any) -> Condition:
    return Condition(
        type=ConditionTypes.LE_EQ,
        value=val,
    )


def gt(val: Any) -> Condition:
    return Condition(
        type=ConditionTypes.GT,
        value=val,
    )


def le(val: Any) -> Condition:
    return Condition(
        type=ConditionTypes.LE,
        value=val,
    )


def one_of(val: Any) -> Condition:
    return Condition(
        type=ConditionTypes.ONE_OF,
        value=val,
    )
