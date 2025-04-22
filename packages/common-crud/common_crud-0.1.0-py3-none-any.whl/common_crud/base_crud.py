from typing import Optional, List, Any, Dict, Sequence
from datetime import datetime
import logging
from sqlalchemy import (
    insert,
    select,
    update as sqlalchemy_update,
    delete as sqlalchemy_delete
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import (
    CRUDError,
    ModelNotSetError,
    InvalidFilterError,
    DatabaseError
)


class BaseCRUD:
    model: Any = None
    filter_fields: Dict[str, str] = {}
    logger = logging.getLogger(__name__)

    @classmethod
    def _check_model(cls):
        if cls.model is None:
            raise ModelNotSetError(
                "Model attribute must be set in the subclass"
            )

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        **filter_by: Any
    ) -> List[Any]:
        cls._check_model()
        try:
            query = select(cls.model)
            for key, value in filter_by.items():
                if (key in cls.filter_fields and
                        cls.filter_fields[key] == "ilike"):
                    query = query.filter(
                        getattr(cls.model, key).ilike(f"%{value}%")
                    )
                else:
                    query = query.filter_by(**{key: value})

            result = await session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            cls.logger.error(
                f"Database error finding all for {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise DatabaseError(
                f"Error finding all: {str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error finding all for {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise CRUDError(
                f"Error finding all: {str(e)}",
                cause=e
            )

    @classmethod
    async def find_one_or_none_by_id(
        cls,
        data_id: int,
        session: AsyncSession
    ) -> Optional[Any]:
        cls._check_model()
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            cls.logger.error(
                f"Database error finding by id for {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise DatabaseError(
                f"Error finding by id={data_id}: {str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error finding by id for {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise CRUDError(
                f"Error finding by id={data_id}: {str(e)}",
                cause=e
            )

    @classmethod
    async def find_one_or_none_by_filter(
        cls,
        session: AsyncSession,
        **filter_by: Any
    ) -> Optional[Any]:
        cls._check_model()
        try:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            cls.logger.error(
                f"Database error finding by filter for "
                f"{cls.model.__tablename__}: {str(e)}"
            )
            raise DatabaseError(
                f"Error finding by filter={filter_by}: {str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error finding by filter for "
                f"{cls.model.__tablename__}: {str(e)}"
            )
            raise CRUDError(
                f"Error finding by filter={filter_by}: {str(e)}",
                cause=e
            )

    @classmethod
    async def add(cls, session: AsyncSession, **values: Any) -> Any:
        cls._check_model()
        try:
            new_instance = cls.model(**values)
            session.add(new_instance)
            await session.commit()
            await session.refresh(new_instance)
            return new_instance
        except SQLAlchemyError as e:
            await session.rollback()
            cls.logger.error(
                f"Database error adding to {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise DatabaseError(
                f"Error adding: {str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error adding to {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise CRUDError(
                f"Error adding: {str(e)}",
                cause=e
            )

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        filter_by: Dict[str, Any],
        **values: Any
    ) -> int:
        cls._check_model()
        if not filter_by:
            raise InvalidFilterError(
                "At least one filter parameter is required for update"
            )
        try:
            query = (
                sqlalchemy_update(cls.model)
                .where(*[getattr(cls.model, k) == v
                       for k, v in filter_by.items()])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            cls.logger.error(
                f"Database error updating {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise DatabaseError(
                f"Error updating: {str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error updating {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise CRUDError(
                f"Error updating: {str(e)}",
                cause=e
            )

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        delete_all: bool = False,
        **filter_by: Any
    ) -> int:
        cls._check_model()
        if not delete_all and not filter_by:
            raise InvalidFilterError(
                "At least one filter parameter is required for deletion"
            )
        try:
            query = sqlalchemy_delete(cls.model)
            if not delete_all:
                query = query.filter_by(**filter_by)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            cls.logger.error(
                f"Database error deleting from {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise DatabaseError(
                f"Error deleting: {str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error deleting from {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise CRUDError(
                f"Error deleting: {str(e)}",
                cause=e
            )

    @classmethod
    async def find_all_in_time_range(
        cls,
        session: AsyncSession,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        param: str = "created_at",
        **filter_by: Any
    ) -> Sequence[Any]:
        cls._check_model()
        try:
            query = select(cls.model).filter_by(**filter_by)
            if start_time:
                query = query.where(getattr(cls.model, param) >= start_time)
            if end_time:
                query = query.where(getattr(cls.model, param) <= end_time)
            result = await session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            cls.logger.error(
                f"Database error finding in time range for "
                f"{cls.model.__tablename__}: {str(e)}"
            )
            raise DatabaseError(
                f"Error finding in time range {start_time} to {end_time}:"
                f"{str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error finding in time range for "
                f"{cls.model.__tablename__}: {str(e)}"
            )
            raise CRUDError(
                f"Error finding in time range {start_time} to {end_time}:"
                f"{str(e)}",
                cause=e
            )

    @classmethod
    async def bulk_insert(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]]
    ) -> int:
        cls._check_model()
        if not data:
            raise InvalidFilterError(
                "Data list cannot be empty for bulk insert"
            )
        try:
            query = insert(cls.model).values(data)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            cls.logger.error(
                f"Database error bulk inserting to {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise DatabaseError(
                f"Error bulk inserting: {str(e)}",
                cause=e
            )
        except Exception as e:
            cls.logger.error(
                f"Error bulk inserting to {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise CRUDError(
                f"Error bulk inserting: {str(e)}",
                cause=e
            )
