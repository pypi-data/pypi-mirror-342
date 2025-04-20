from typing import Literal, cast

LlmType = Literal["DEFAULT", "MINI", "PREMIUM"]

LLM_TYPE_VALUES: set[LlmType] = {
    "DEFAULT",
    "MINI",
    "PREMIUM",
}


def check_llm_type(value: str) -> LlmType:
    if value in LLM_TYPE_VALUES:
        return cast(LlmType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LLM_TYPE_VALUES!r}")
