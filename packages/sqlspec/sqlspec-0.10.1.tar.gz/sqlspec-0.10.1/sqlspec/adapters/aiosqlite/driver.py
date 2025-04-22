from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Optional, Union, cast, overload

import aiosqlite

from sqlspec.base import AsyncDriverAdapterProtocol
from sqlspec.mixins import SQLTranslatorMixin

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Sequence

    from sqlspec.typing import ModelDTOT, StatementParameterType, T

__all__ = ("AiosqliteConnection", "AiosqliteDriver")
AiosqliteConnection = aiosqlite.Connection


class AiosqliteDriver(
    SQLTranslatorMixin["AiosqliteConnection"],
    AsyncDriverAdapterProtocol["AiosqliteConnection"],
):
    """SQLite Async Driver Adapter."""

    connection: "AiosqliteConnection"
    dialect: str = "sqlite"

    def __init__(self, connection: "AiosqliteConnection") -> None:
        self.connection = connection

    @staticmethod
    async def _cursor(connection: "AiosqliteConnection", *args: Any, **kwargs: Any) -> "aiosqlite.Cursor":
        return await connection.cursor(*args, **kwargs)

    @asynccontextmanager
    async def _with_cursor(self, connection: "AiosqliteConnection") -> "AsyncGenerator[aiosqlite.Cursor, None]":
        cursor = await self._cursor(connection)
        try:
            yield cursor
        finally:
            await cursor.close()

    # --- Public API Methods --- #
    @overload
    async def select(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Sequence[dict[str, Any]]": ...
    @overload
    async def select(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "Sequence[ModelDTOT]": ...
    async def select(
        self,
        sql: str,
        parameters: Optional["StatementParameterType"] = None,
        /,
        *,
        connection: Optional["AiosqliteConnection"] = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Sequence[Union[ModelDTOT, dict[str, Any]]]":
        """Fetch data from the database.

        Returns:
            List of row data as either model instances or dictionaries.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            results = await cursor.fetchall()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if not results:
                return []
            column_names = [c[0] for c in cursor.description or []]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if schema_type is None:
                return [dict(zip(column_names, row)) for row in results]  # pyright: ignore[reportUnknownArgumentType]
            return [cast("ModelDTOT", schema_type(**dict(zip(column_names, row)))) for row in results]  # pyright: ignore[reportUnknownArgumentType]

    @overload
    async def select_one(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "dict[str, Any]": ...
    @overload
    async def select_one(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "ModelDTOT": ...
    async def select_one(
        self,
        sql: str,
        parameters: Optional["StatementParameterType"] = None,
        /,
        *,
        connection: Optional["AiosqliteConnection"] = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Union[ModelDTOT, dict[str, Any]]":
        """Fetch one row from the database.

        Returns:
            The first row of the query results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            result = await cursor.fetchone()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            result = self.check_not_found(result)
            column_names = [c[0] for c in cursor.description or []]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if schema_type is None:
                return dict(zip(column_names, result))  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
            return cast("ModelDTOT", schema_type(**dict(zip(column_names, result))))  # pyright: ignore[reportUnknownArgumentType]

    @overload
    async def select_one_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Optional[dict[str, Any]]": ...
    @overload
    async def select_one_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "Optional[ModelDTOT]": ...
    async def select_one_or_none(
        self,
        sql: str,
        parameters: Optional["StatementParameterType"] = None,
        /,
        *,
        connection: Optional["AiosqliteConnection"] = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[ModelDTOT, dict[str, Any]]]":
        """Fetch one row from the database.

        Returns:
            The first row of the query results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            result = await cursor.fetchone()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if result is None:
                return None
            column_names = [c[0] for c in cursor.description or []]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if schema_type is None:
                return dict(zip(column_names, result))  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
            return cast("ModelDTOT", schema_type(**dict(zip(column_names, result))))  # pyright: ignore[reportUnknownArgumentType]

    @overload
    async def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Any": ...
    @overload
    async def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "type[T]",
        **kwargs: Any,
    ) -> "T": ...
    async def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "Optional[type[T]]" = None,
        **kwargs: Any,
    ) -> "Union[T, Any]":
        """Fetch a single value from the database.

        Returns:
            The first value from the first row of results, or None if no results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            result = await cursor.fetchone()  # pyright: ignore[reportUnknownMemberType]
            result = self.check_not_found(result)
            if schema_type is None:
                return result[0]
            return schema_type(result[0])  # type: ignore[call-arg]

    @overload
    async def select_value_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Optional[Any]": ...
    @overload
    async def select_value_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "type[T]",
        **kwargs: Any,
    ) -> "Optional[T]": ...
    async def select_value_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "Optional[type[T]]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[T, Any]]":
        """Fetch a single value from the database.

        Returns:
            The first value from the first row of results, or None if no results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            result = await cursor.fetchone()  # pyright: ignore[reportUnknownMemberType]
            if result is None:
                return None
            if schema_type is None:
                return result[0]
            return schema_type(result[0])  # type: ignore[call-arg]

    async def insert_update_delete(
        self,
        sql: str,
        parameters: Optional["StatementParameterType"] = None,
        /,
        *,
        connection: Optional["AiosqliteConnection"] = None,
        **kwargs: Any,
    ) -> int:
        """Insert, update, or delete data from the database.

        Returns:
            Row count affected by the operation.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            return cursor.rowcount if hasattr(cursor, "rowcount") else -1  # pyright: ignore[reportUnknownVariableType, reportGeneralTypeIssues]

    @overload
    async def insert_update_delete_returning(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "dict[str, Any]": ...
    @overload
    async def insert_update_delete_returning(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[AiosqliteConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "ModelDTOT": ...
    async def insert_update_delete_returning(
        self,
        sql: str,
        parameters: Optional["StatementParameterType"] = None,
        /,
        *,
        connection: Optional["AiosqliteConnection"] = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[dict[str, Any], ModelDTOT]]":
        """Insert, update, or delete data from the database and return result.

        Returns:
            The first row of results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            results = list(await cursor.fetchall())  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if not results:  # Check if empty
                return None
            column_names = [c[0] for c in cursor.description or []]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**dict(zip(column_names, results[0]))))  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
            return dict(zip(column_names, results[0]))  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]

    async def execute_script(
        self,
        sql: str,
        parameters: Optional["StatementParameterType"] = None,
        /,
        *,
        connection: Optional["AiosqliteConnection"] = None,
        **kwargs: Any,
    ) -> str:
        """Execute a script.

        Returns:
            Status message for the operation.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            return "DONE"

    async def execute_script_returning(
        self,
        sql: str,
        parameters: Optional["StatementParameterType"] = None,
        /,
        *,
        connection: Optional["AiosqliteConnection"] = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[dict[str, Any], ModelDTOT]]":
        """Execute a script and return result.

        Returns:
            The first row of results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)  # pyright: ignore[reportUnknownMemberType]
            results = list(await cursor.fetchall())  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if not results:  # Check if empty
                return None
            column_names = [c[0] for c in cursor.description or []]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**dict(zip(column_names, results[0]))))  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
            return dict(zip(column_names, results[0]))  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
