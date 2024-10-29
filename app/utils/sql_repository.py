from abc import (
    ABC,
    abstractmethod,
)
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import (
    delete,
    insert,
    Result,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel as Model


class AbstractRepository(ABC):

    @abstractmethod
    async def fetch_all(
        self,
    ) -> Optional[list[BaseModel]]: ...

    @abstractmethod
    async def fetch_by_id(
        self,
        item_id: int,
    ) -> Optional[BaseModel]: ...

    @abstractmethod
    async def create(
        self,
        item_in: BaseModel,
    ) -> BaseModel: ...

    @abstractmethod
    async def update_by_id(
        self,
        item_id: int,
        item_in: BaseModel,
    ) -> BaseModel: ...

    @abstractmethod
    async def remove_by_id(
        self,
        item_id: int,
    ) -> None: ...


class SQLAlchemyRepository(AbstractRepository):
    model: Model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def fetch_all(self) -> Optional[list[BaseModel]]:
        stmt = select(self.model)
        result: Result = await self.session.execute(stmt)
        return [item.to_read_model() for item in list(result.scalars().all())]

    async def fetch_by_id(self, item_id: int) -> Optional[BaseModel]:
        item: Model = await self.session.get(self.model, item_id)

        if item:
            return item.to_read_model()

    async def create(self, item_in: BaseModel) -> BaseModel:
        stmt = insert(self.model).values(**item_in.model_dump()).returning(self.model)
        result: Result = await self.session.execute(stmt)
        await self.session.commit()
        item = result.scalars().first()
        return item.to_read_model()

    async def update_by_id(
        self,
        item_id: int,
        item_in: BaseModel,
    ) -> Optional[BaseModel]:
        stmt = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(item_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result: Result = await self.session.execute(stmt)
        await self.session.commit()
        updated_item: Model = result.scalars().first()

        if updated_item:
            return updated_item.to_read_model()

    async def remove_by_id(self, item_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == item_id)
        await self.session.execute(stmt)
        await self.session.commit()
