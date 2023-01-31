from typing import Any, Optional


class Result:
    item: Optional[Any]
    message: str

    def __init__(self, message: str, item: Optional[Any]) -> None:
        self.message = message
        self.item = item

    @staticmethod
    def success(message: str, item: Optional[Any]) -> "Result":
        return Result(message=message, item=item)

    @staticmethod
    def fail(message: str) -> "Result":
        return Result(message=message, item=None)
