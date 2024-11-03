import random
from abc import (
    ABC,
    abstractmethod,
)


class AbstractModerationService(ABC):

    @abstractmethod
    async def check_content(self, *args) -> dict: ...

    @abstractmethod
    async def get_moderation_result(content: str) -> dict: ...


class AIModerationService(AbstractModerationService):

    async def check_content(self, *args) -> dict:
        full_content = "\n".join(filter(None, args))
        return await self.get_moderation_result(full_content)

    async def get_moderation_result(self, content: str) -> dict:
        # ai actions
        is_blocked = random.choice([True, False, False])  # noqa
        reasons = ["swearing", "bad language"]
        reason = random.choice(reasons) if is_blocked else ""  # noqa
        return {"is_blocked": is_blocked, "blocked_reason": reason}
