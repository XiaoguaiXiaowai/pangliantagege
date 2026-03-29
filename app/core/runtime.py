import sys


SUPPORTED_MIN = (3, 11)
SUPPORTED_MAX_EXCLUSIVE = (3, 14)


def ensure_supported_python() -> None:
    current = sys.version_info[:2]
    if SUPPORTED_MIN <= current < SUPPORTED_MAX_EXCLUSIVE:
        return

    minimum = ".".join(str(value) for value in SUPPORTED_MIN)
    maximum = ".".join(str(value) for value in SUPPORTED_MAX_EXCLUSIVE)
    current_text = ".".join(str(value) for value in current)
    raise RuntimeError(
        f"当前 Python 版本为 {current_text}，该项目阶段一依赖仅支持 Python {minimum} 至 "
        f"{maximum} 之前的版本。请使用 Python 3.11、3.12 或 3.13 重新创建虚拟环境。"
    )
