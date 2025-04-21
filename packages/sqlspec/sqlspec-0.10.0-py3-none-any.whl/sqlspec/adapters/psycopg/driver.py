import logging
from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, Any, Optional, Union, cast, overload

from psycopg import AsyncConnection, Connection
from psycopg.rows import dict_row

from sqlspec.base import AsyncDriverAdapterProtocol, SyncDriverAdapterProtocol
from sqlspec.exceptions import SQLParsingError
from sqlspec.mixins import SQLTranslatorMixin
from sqlspec.statement import PARAM_REGEX, SQLStatement

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator, Sequence

    from sqlspec.typing import ModelDTOT, StatementParameterType, T

logger = logging.getLogger("sqlspec")

__all__ = ("PsycopgAsyncConnection", "PsycopgAsyncDriver", "PsycopgSyncConnection", "PsycopgSyncDriver")

PsycopgSyncConnection = Connection
PsycopgAsyncConnection = AsyncConnection


class PsycopgDriverBase:
    dialect: str

    def _process_sql_params(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        **kwargs: Any,
    ) -> "tuple[str, Optional[Union[tuple[Any, ...], list[Any], dict[str, Any]]]]":
        """Process SQL and parameters, converting :name -> %(name)s if needed."""
        stmt = SQLStatement(sql=sql, parameters=parameters, dialect=self.dialect, kwargs=kwargs or None)
        processed_sql, processed_params = stmt.process()

        if isinstance(processed_params, dict):
            parameter_dict = processed_params
            processed_sql_parts: list[str] = []
            last_end = 0
            found_params_regex: list[str] = []

            for match in PARAM_REGEX.finditer(processed_sql):
                if match.group("dquote") or match.group("squote") or match.group("comment"):
                    continue

                if match.group("var_name"):
                    var_name = match.group("var_name")
                    found_params_regex.append(var_name)
                    start = match.start("var_name") - 1
                    end = match.end("var_name")

                    if var_name not in parameter_dict:
                        msg = (
                            f"Named parameter ':{var_name}' found in SQL but missing from processed parameters. "
                            f"Processed SQL: {processed_sql}"
                        )
                        raise SQLParsingError(msg)

                    processed_sql_parts.extend((processed_sql[last_end:start], f"%({var_name})s"))
                    last_end = end

            processed_sql_parts.append(processed_sql[last_end:])
            final_sql = "".join(processed_sql_parts)

            if not found_params_regex and parameter_dict:
                logger.warning(
                    "Dict params provided (%s), but no :name placeholders found. SQL: %s",
                    list(parameter_dict.keys()),
                    processed_sql,
                )
                return processed_sql, parameter_dict

            return final_sql, parameter_dict

        return processed_sql, processed_params


class PsycopgSyncDriver(
    PsycopgDriverBase,
    SQLTranslatorMixin["PsycopgSyncConnection"],
    SyncDriverAdapterProtocol["PsycopgSyncConnection"],
):
    """Psycopg Sync Driver Adapter."""

    connection: "PsycopgSyncConnection"
    dialect: str = "postgres"

    def __init__(self, connection: "PsycopgSyncConnection") -> None:
        self.connection = connection

    def _process_sql_params(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        **kwargs: Any,
    ) -> "tuple[str, Optional[Union[tuple[Any, ...], list[Any], dict[str, Any]]]]":
        stmt = SQLStatement(sql=sql, parameters=parameters, dialect=self.dialect, kwargs=kwargs or None)
        processed_sql, processed_params = stmt.process()

        if isinstance(processed_params, dict):
            parameter_dict = processed_params
            processed_sql_parts: list[str] = []
            last_end = 0
            found_params_regex: list[str] = []

            for match in PARAM_REGEX.finditer(processed_sql):
                if match.group("dquote") or match.group("squote") or match.group("comment"):
                    continue

                if match.group("var_name"):
                    var_name = match.group("var_name")
                    found_params_regex.append(var_name)
                    start = match.start("var_name") - 1
                    end = match.end("var_name")

                    if var_name not in parameter_dict:
                        msg = (
                            f"Named parameter ':{var_name}' found in SQL but missing from processed parameters. "
                            f"Processed SQL: {processed_sql}"
                        )
                        raise SQLParsingError(msg)

                    processed_sql_parts.extend((processed_sql[last_end:start], f"%({var_name})s"))
                    last_end = end

            processed_sql_parts.append(processed_sql[last_end:])
            final_sql = "".join(processed_sql_parts)

            if not found_params_regex and parameter_dict:
                logger.warning(
                    "Dict params provided (%s), but no :name placeholders found. SQL: %s",
                    list(parameter_dict.keys()),
                    processed_sql,
                )
                return processed_sql, parameter_dict

            return final_sql, parameter_dict

        return processed_sql, processed_params

    @staticmethod
    @contextmanager
    def _with_cursor(connection: "PsycopgSyncConnection") -> "Generator[Any, None, None]":
        cursor = connection.cursor(row_factory=dict_row)
        try:
            yield cursor
        finally:
            cursor.close()

    # --- Public API Methods --- #
    @overload
    def select(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Sequence[dict[str, Any]]": ...
    @overload
    def select(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "Sequence[ModelDTOT]": ...
    def select(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        connection: "Optional[PsycopgSyncConnection]" = None,
        **kwargs: Any,
    ) -> "Sequence[Union[ModelDTOT, dict[str, Any]]]":
        """Fetch data from the database.

        Returns:
            List of row data as either model instances or dictionaries.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            results = cursor.fetchall()
            if not results:
                return []

            if schema_type is not None:
                return [cast("ModelDTOT", schema_type(**row)) for row in results]  # pyright: ignore[reportUnknownArgumentType]
            return [cast("dict[str,Any]", row) for row in results]  # pyright: ignore[reportUnknownArgumentType]

    @overload
    def select_one(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "dict[str, Any]": ...
    @overload
    def select_one(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "ModelDTOT": ...
    def select_one(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Union[ModelDTOT, dict[str, Any]]":
        """Fetch one row from the database.

        Returns:
            The first row of the query results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            row = cursor.fetchone()
            row = self.check_not_found(row)
            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**cast("dict[str,Any]", row)))
            return cast("dict[str,Any]", row)

    @overload
    def select_one_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Optional[dict[str, Any]]": ...
    @overload
    def select_one_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "Optional[ModelDTOT]": ...
    def select_one_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[ModelDTOT, dict[str, Any]]]":
        """Fetch one row from the database.

        Returns:
            The first row of the query results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            row = cursor.fetchone()
            if row is None:
                return None
            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**cast("dict[str,Any]", row)))
            return cast("dict[str,Any]", row)

    @overload
    def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Any": ...
    @overload
    def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "type[T]",
        **kwargs: Any,
    ) -> "T": ...
    def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "Optional[type[T]]" = None,
        **kwargs: Any,
    ) -> "Union[T, Any]":
        """Fetch a single value from the database.

        Returns:
            The first value from the first row of results, or None if no results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            row = cursor.fetchone()
            row = self.check_not_found(row)
            val = next(iter(row.values())) if row else None
            val = self.check_not_found(val)
            if schema_type is not None:
                return schema_type(val)  # type: ignore[call-arg]
            return val

    @overload
    def select_value_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "Optional[Any]": ...
    @overload
    def select_value_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "type[T]",
        **kwargs: Any,
    ) -> "Optional[T]": ...
    def select_value_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "Optional[type[T]]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[T, Any]]":
        """Fetch a single value from the database.

        Returns:
            The first value from the first row of results, or None if no results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            row = cursor.fetchone()
            if row is None:
                return None
            val = next(iter(row.values())) if row else None
            if val is None:
                return None
            if schema_type is not None:
                return schema_type(val)  # type: ignore[call-arg]
            return val

    def insert_update_delete(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        **kwargs: Any,
    ) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return the number of affected rows.

        Returns:
            The number of rows affected by the operation.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            return getattr(cursor, "rowcount", -1)  # pyright: ignore[reportUnknownMemberType]

    @overload
    def insert_update_delete_returning(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: None = None,
        **kwargs: Any,
    ) -> "dict[str, Any]": ...
    @overload
    def insert_update_delete_returning(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "ModelDTOT": ...
    def insert_update_delete_returning(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[dict[str, Any], ModelDTOT]]":
        """Insert, update, or delete data from the database and return result.

        Returns:
            The first row of results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            result = cursor.fetchone()

            if result is None:
                return None

            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**result))  # pyright: ignore[reportUnknownArgumentType]
            return cast("dict[str, Any]", result)  # pyright: ignore[reportUnknownArgumentType,reportUnknownVariableType]

    def execute_script(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgSyncConnection]" = None,
        **kwargs: Any,
    ) -> str:
        """Execute a script.

        Returns:
            Status message for the operation.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        with self._with_cursor(connection) as cursor:
            cursor.execute(sql, parameters)
            return str(cursor.statusmessage) if cursor.statusmessage is not None else "DONE"


class PsycopgAsyncDriver(
    PsycopgDriverBase,
    SQLTranslatorMixin["PsycopgAsyncConnection"],
    AsyncDriverAdapterProtocol["PsycopgAsyncConnection"],
):
    """Psycopg Async Driver Adapter."""

    connection: "PsycopgAsyncConnection"
    dialect: str = "postgres"

    def __init__(self, connection: "PsycopgAsyncConnection") -> None:
        self.connection = connection

    @staticmethod
    @asynccontextmanager
    async def _with_cursor(connection: "PsycopgAsyncConnection") -> "AsyncGenerator[Any, None]":
        cursor = connection.cursor(row_factory=dict_row)
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
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
        connection: "Optional[PsycopgAsyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "Sequence[ModelDTOT]": ...
    async def select(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        **kwargs: Any,
    ) -> "Sequence[Union[ModelDTOT, dict[str, Any]]]":
        """Fetch data from the database.

        Returns:
            List of row data as either model instances or dictionaries.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)
        results: list[Union[ModelDTOT, dict[str, Any]]] = []

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)
            results = await cursor.fetchall()
            if not results:
                return []
            if schema_type is not None:
                return [cast("ModelDTOT", schema_type(**cast("dict[str,Any]", row))) for row in results]  # pyright: ignore[reportUnknownArgumentType]
            return [cast("dict[str,Any]", row) for row in results]  # pyright: ignore[reportUnknownArgumentType]

    @overload
    async def select_one(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
        connection: "Optional[PsycopgAsyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "ModelDTOT": ...
    async def select_one(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
            await cursor.execute(sql, parameters)
            row = await cursor.fetchone()
            row = self.check_not_found(row)
            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**cast("dict[str,Any]", row)))
            return cast("dict[str,Any]", row)

    @overload
    async def select_one_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
        connection: "Optional[PsycopgAsyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "Optional[ModelDTOT]": ...
    async def select_one_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        schema_type: "Optional[type[ModelDTOT]]" = None,
        connection: "Optional[PsycopgAsyncConnection]" = None,
        **kwargs: Any,
    ) -> "Optional[Union[ModelDTOT, dict[str, Any]]]":
        """Fetch one row from the database.

        Returns:
            The first row of the query results.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)
            row = await cursor.fetchone()
            if row is None:
                return None
            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**cast("dict[str,Any]", row)))
            return cast("dict[str,Any]", row)

    @overload
    async def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
        connection: "Optional[PsycopgAsyncConnection]" = None,
        schema_type: "type[T]",
        **kwargs: Any,
    ) -> "T": ...
    async def select_value(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
            await cursor.execute(sql, parameters)
            row = await cursor.fetchone()
            row = self.check_not_found(row)
            val = next(iter(row.values())) if row else None
            val = self.check_not_found(val)
            if schema_type is not None:
                return schema_type(val)  # type: ignore[call-arg]
            return val

    async def select_value_or_none(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
            await cursor.execute(sql, parameters)
            row = await cursor.fetchone()
            if row is None:
                return None
            val = next(iter(row.values())) if row else None
            if val is None:
                return None
            if schema_type is not None:
                return schema_type(val)  # type: ignore[call-arg]
            return val

    async def insert_update_delete(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
        **kwargs: Any,
    ) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return the number of affected rows.

        Returns:
            The number of rows affected by the operation.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)
            try:
                rowcount = int(cursor.rowcount)
            except (TypeError, ValueError):
                rowcount = -1
            return rowcount

    @overload
    async def insert_update_delete_returning(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
        connection: "Optional[PsycopgAsyncConnection]" = None,
        schema_type: "type[ModelDTOT]",
        **kwargs: Any,
    ) -> "ModelDTOT": ...
    async def insert_update_delete_returning(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
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
            await cursor.execute(sql, parameters)
            result = await cursor.fetchone()

            if result is None:
                return None

            if schema_type is not None:
                return cast("ModelDTOT", schema_type(**result))  # pyright: ignore[reportUnknownArgumentType]
            return cast("dict[str, Any]", result)  # pyright: ignore[reportUnknownArgumentType,reportUnknownVariableType]

    async def execute_script(
        self,
        sql: str,
        parameters: "Optional[StatementParameterType]" = None,
        /,
        *,
        connection: "Optional[PsycopgAsyncConnection]" = None,
        **kwargs: Any,
    ) -> str:
        """Execute a script.

        Returns:
            Status message for the operation.
        """
        connection = self._connection(connection)
        sql, parameters = self._process_sql_params(sql, parameters, **kwargs)

        async with self._with_cursor(connection) as cursor:
            await cursor.execute(sql, parameters)
            return str(cursor.statusmessage) if cursor.statusmessage is not None else "DONE"
