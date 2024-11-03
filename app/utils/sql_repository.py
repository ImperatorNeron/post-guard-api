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
from app.utils.exceptions import FieldNotFoundError


class AbstractRepository(ABC):
    """Abstract repository defining essential CRUD operations.

    Each method must be implemented by concrete repository classes.

    """

    @abstractmethod
    async def fetch_all(
        self,
    ) -> list[BaseModel]:
        """Retrieve all items from the repository.

        Returns:
            list[BaseModel]: A list of all items in
            the repository as a pydantic BaseModel instances.

        """
        ...

    @abstractmethod
    async def fetch_by_id(
        self,
        item_id: int,
    ) -> Optional[BaseModel]:
        """Fetch a single item by its id.

        Args:
            item_id (int): The id of the item to fetch.

        Returns:
            Optional[BaseModel]: The item as a pydantic BaseModel
            instance if found; otherwise, None.

        """
        ...

    @abstractmethod
    async def fetch_by_attributes(
        self,
        filters: dict,
    ) -> list[BaseModel]:
        """Retrieve all items matching specific attributes.

        Args:
            filters (dict): A dictionary of attribute names and
            values to filter the query.

        Returns:
            list[BaseModel]: A list of items as a pydantic BaseModel
            instances that match the filters.

        """
        ...

    @abstractmethod
    async def fetch_one_by_attributes(
        self,
        name: str,
        filters: dict,
    ) -> Optional[BaseModel]:
        """Retrieve a single item matching specified attributes.

        Args:
            filters (dict): A dictionary of attribute
            names and values to filter the query.

        Returns:
            Optional[BaseModel]: The first item that matches
            the filters, as a pydantic BaseModel instance, or None if not found.

        """
        ...

    @abstractmethod
    async def create(
        self,
        item_in: BaseModel,
    ) -> BaseModel:
        """Create a new item in the repository.

        Args:
            item_in (BaseModel): The data for the
            new item as a pydantic BaseModel instance.

        Returns:
            BaseModel: The created item as a pydantic BaseModel instance.

        """
        ...

    @abstractmethod
    async def update_by_id(
        self,
        item_id: int,
        item_in: BaseModel,
    ) -> BaseModel:
        """Update an existing item by its id.

        Args:
            item_id (int): The id of the item to update.
            item_in (BaseModel): The updated data for the
            item as a pydantic BaseModel instance.

        Returns:
            BaseModel: The updated item as a pydantic BaseModel instance.

        """
        ...

    @abstractmethod
    async def remove_by_id(
        self,
        item_id: int,
    ) -> None:
        """Remove an item by its id.

        Args:
            item_id (int): The id of the item to remove.

        Returns:
            None

        """
        ...


class SQLAlchemyRepository(AbstractRepository):
    """SQLAlchemy-based repository."""

    model: Model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def fetch_all(self) -> list[BaseModel]:
        stmt = select(self.model)
        result: Result = await self.session.execute(stmt)
        return [item.to_read_model() for item in list(result.scalars().all())]

    async def fetch_by_id(self, item_id: int) -> Optional[BaseModel]:
        item: Model = await self.session.get(self.model, item_id)
        return item.to_read_model() if item else None

    async def fetch_by_attributes(
        self,
        **filters: dict,
    ) -> list[BaseModel]:

        stmt = select(self.model)

        for name, value in filters.items():
            field = getattr(self.model, name, None)

            if field is None:
                raise FieldNotFoundError(
                    field_name=name,
                    model_name=self.model,
                )

            stmt = stmt.where(field == value)

        result = await self.session.execute(stmt)

        return [item.to_read_model() for item in result.scalars().all()]

    async def fetch_one_by_attributes(self, **filters: dict) -> Optional[BaseModel]:
        results = await self.fetch_by_attributes(**filters)
        return results[0] if results else None

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
        return updated_item.to_read_model() if updated_item else None

    async def remove_by_id(self, item_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == item_id)
        await self.session.execute(stmt)
        await self.session.commit()
