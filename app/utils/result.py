from typing import Optional, Any


class Result:
    item: Optional[Any]
    message: str

    def __init__(self, message: str, item: Any):
        self.message = message
        self.item = item

    @staticmethod
    def success(message: str, item: Any):
        return Result(message=message, item=item)

    @staticmethod
    def fail(message: str):
        return Result(message=message, item=None)
