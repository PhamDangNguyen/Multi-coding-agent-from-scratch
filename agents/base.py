from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

class BaseAgent(Generic[InputT, OutputT]):
    async def run(self, task: InputT, context) -> OutputT:
        ...