from enum import StrEnum


class ConditionTypes(StrEnum):
    NOT_EQ = "not_eq"
    GT_EQ = "gt_eq"
    LE_EQ = "le_eq"
    GT = "gt"
    LE = "le"
    ONE_OF = "one_of"