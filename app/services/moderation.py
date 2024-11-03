import json
from abc import (
    ABC,
    abstractmethod,
)

from openai import AsyncOpenAI

from app.core.settings import settings
from app.exceptions.moderation import ModerationResponseError
from app.utils.prompts.moderate_system_prompt import MODERATE_SYSTEM_PROMPT


class AbstractModerationService(ABC):

    @abstractmethod
    async def check_content(self, *args) -> dict: ...

    @abstractmethod
    async def prompt(content: str, system_content: str) -> dict: ...


class AIModerationService(AbstractModerationService):

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.chat_gpt.api_key)

    async def check_content(self, *args) -> dict | None:
        full_content = "\n".join(filter(None, args))
        response = await self.prompt(full_content)
        return await self.parse_response(response)

    async def parse_response(self, response_text: str) -> dict | None:
        try:
            moderation_result = json.loads(response_text)
        except json.JSONDecodeError:
            raise ModerationResponseError()

        if moderation_result:
            return {
                "is_blocked": moderation_result["is_blocked"],
                "blocked_reason": moderation_result["blocked_reason"],
            }

    async def prompt(
        self,
        content: str,
        system_content: str = MODERATE_SYSTEM_PROMPT,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=settings.chat_gpt.model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": content},
            ],
        )
        return response.choices[0].message.content
