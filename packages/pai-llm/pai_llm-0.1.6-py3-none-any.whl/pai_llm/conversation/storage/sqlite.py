import json
import os
import sqlite3
import typing
from datetime import datetime
from pathlib import Path

from commons_lang import object_utils
from loguru import logger

from pai_llm.conversation.exceptions import DatabaseOperationError
from pai_llm.conversation.models import Conversation, Message
from pai_llm.conversation.storage.base import BaseStorage
from pai_llm.exceptions import DataConvertError


class SQLiteSchema:
    CREATE_CONVERSATION_TABLE = """
        CREATE TABLE IF NOT EXISTS conversation (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            user_id TEXT NOT NULL,
            metadata TEXT,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    """

    CREATE_MESSAGE_TABLE = """
        CREATE TABLE IF NOT EXISTS message (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT,
            token_count INTEGER,
            message_index INTEGER,
            created_at TIMESTAMP NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES CONVERSATION(id) ON DELETE CASCADE
        )
    """

    INSERT_CONVERSATION = """
        INSERT OR REPLACE INTO conversation (id, name, user_id, metadata, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    GET_CONVERSATION = """
        SELECT * FROM conversation WHERE id = ?
    """

    GET_CONVERSATIONS = """
        SELECT * FROM conversation WHERE user_id = ? ORDER BY updated_at DESC
    """

    LIST_CONVERSATIONS = """
        SELECT * FROM conversation WHERE user_id = ? ORDER BY updated_at DESC LIMIT ? OFFSET ?
    """

    RENAME_CONVERSATION = """
        UPDATE conversation SET name = ? WHERE id = ?
    """

    DELETE_CONVERSATION = """
       DELETE FROM conversation WHERE id = ?
   """

    INSERT_MESSAGE = """
        INSERT INTO message (id, conversation_id, role, content, metadata, token_count, message_index, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    GET_MESSAGE = """
        SELECT * FROM message WHERE id = ?
    """

    GET_MESSAGES = """
        SELECT * FROM message WHERE conversation_id = ? ORDER BY message_index ASC
    """

    LIST_MESSAGES = """
        SELECT * FROM message WHERE conversation_id = ? ORDER BY message_index ASC LIMIT ?
    """

    DELETE_MESSAGES = """
        DELETE FROM message WHERE conversation_id = ?
    """


class SQLiteStorage(BaseStorage):

    def __init__(self, db_file_path: str | Path, max_messages: typing.Optional[int] = 100):
        super().__init__()

        assert db_file_path, "Database file path cannot be empty"
        assert max_messages is None or max_messages > 0, "Max messages must be greater than 0"

        self.db_file_path = db_file_path or ":memory:"
        self.max_messages = max_messages
        logger.debug(f"Initializing SQLiteStorage with db_file_path: {db_file_path}")

        if self.db_file_path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(self.db_file_path)), exist_ok=True)

        try:
            self.conn = self._get_connection()
            self._init_db(self.conn)
            self.conn.close()
        except sqlite3.Error as e:
            logger.error(f"SQLiteStorage initialization failed: {e}")
            raise DatabaseOperationError(f"SQLiteStorage initialization failed: {e}") from e

    def _init_db(self, conn: sqlite3.Connection):
        try:
            conn.execute(SQLiteSchema.CREATE_CONVERSATION_TABLE)
            conn.execute(SQLiteSchema.CREATE_MESSAGE_TABLE)
            conn.commit()
            logger.debug(f"SQLiteStorage initialized at {self.db_file_path}")
        except sqlite3.Error as e:
            logger.error(f"SQLiteStorage initialization failed: {e}")
            raise DatabaseOperationError(f"SQLiteStorage initialization failed: {e}") from e

    def _get_connection(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.db_file_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to SQLite database: {e}")
            raise DatabaseOperationError(f"Failed to connect to SQLite database: {e}") from e

    @staticmethod
    def _serialize_metadata(metadata: typing.Dict[str, typing.Any]) -> str:
        try:
            return json.dumps(metadata)
        except Exception as e:
            logger.error(f"Failed to serialize metadata: {e}")
            raise DataConvertError(f"Failed to serialize metadata: {e}") from e

    @staticmethod
    def _deserialize_metadata(metadata_str: str) -> typing.Dict[str, typing.Any]:
        try:
            return json.loads(metadata_str)
        except Exception as e:
            logger.error(f"Failed to deserialize metadata: {e}")
            raise DataConvertError(f"Failed to deserialize metadata: {e}") from e

    def _conversation_to_row(self, conversation: Conversation) -> typing.Tuple:
        assert conversation is not None, "Conversation cannot be None"
        assert conversation.id is not None, "Conversation id cannot be None"

        try:
            return (
                conversation.id,
                conversation.name,
                conversation.user_id,
                self._serialize_metadata(conversation.metadata),
                conversation.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                conversation.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
            )
        except Exception as e:
            logger.error(f"Failed to convert conversation to row: {e}")
            raise DataConvertError(f"Failed to convert conversation to row: {e}") from e

    def _row_to_conversation(self, row: sqlite3.Row, messages: typing.List[Message]) -> Conversation:
        try:
            return Conversation(
                id=row["id"],
                name=row["name"],
                user_id=row["user_id"],
                messages=messages,
                metadata=self._deserialize_metadata(row["metadata"]),
                created_at=datetime.strptime(row["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
                updated_at=datetime.strptime(row["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            )
        except Exception as e:
            logger.error(f"Failed to convert row to conversation: {e}")
            raise DataConvertError(f"Failed to convert row to conversation: {e}") from e

    def _message_to_row(self, message: Message, conversation_id: str, message_index: int) -> typing.Tuple:
        assert message is not None, "Message cannot be None"
        assert conversation_id is not None, "Conversation id cannot be None"
        assert message_index >= 0, "MessageIndex must be greater than or equal to 0"

        try:
            return (
                message.id,
                conversation_id,
                message.role,
                message.content,
                self._serialize_metadata(message.metadata),
                message.token_count,
                message_index,
                message.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
            )
        except Exception as e:
            logger.error(f"Failed to convert message to row: {e}")
            raise DataConvertError(f"Failed to convert message to row: {e}") from e

    def _row_to_message(self, row: sqlite3.Row) -> Message:
        assert row is not None, "Row cannot be None"
        try:
            return Message(
                id=row["id"],
                role=row["role"],
                content=row["content"],
                metadata=self._deserialize_metadata(row["metadata"]),
                token_count=row["token_count"],
                created_at=datetime.strptime(row["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            )
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to convert row to message: {e}")
            raise DataConvertError(f"Failed to convert row to message: {e}") from e

    def save_conversation(self, conversation: Conversation):
        assert conversation is not None, "Conversation cannot be None"
        assert conversation.id is not None, "Conversation id cannot be None"

        conn: sqlite3.Connection | None = None
        try:
            conn = self._get_connection()
            conn.execute("BEGIN TRANSACTION")

            conversation_row = self._conversation_to_row(conversation)
            conn.execute(SQLiteSchema.INSERT_CONVERSATION, conversation_row)
            conn.execute(SQLiteSchema.DELETE_MESSAGES, (conversation.id,))

            messages = conversation.messages
            if object_utils.is_not_empty(messages) and (len(messages) > self.max_messages):
                messages = messages[-self.max_messages:]

            for i, message in enumerate(messages):
                message_row = self._message_to_row(message, conversation.id, i)
                conn.execute(SQLiteSchema.INSERT_MESSAGE, message_row)

            conn.commit()
            logger.debug(f"SQLiteStorage saved conversation {conversation.id}")
        except sqlite3.IntegrityError as e:
            if conn:
                conn.rollback()
            logger.error(f"Database integrity error while saving conversation {conversation.id}: {e}")
            raise DatabaseOperationError(
                f"Database integrity error while saving conversation {conversation.id}: {e}"
            ) from e
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error while saving conversation {conversation.id}: {e}")
            raise DatabaseOperationError(
                f"Database error while saving conversation {conversation.id}: {e}"
            ) from e
        except ValueError as e:
            if conn:
                conn.rollback()
            logger.error(f"Value error while saving conversation {conversation.id}: {e}")
            raise DatabaseOperationError(
                f"Value error while saving conversation {conversation.id}: {e}"
            ) from e
        finally:
            if conn:
                conn.close()

    def get_conversation(
            self,
            conversation_id: str,
            messages_limit: typing.Optional[int] = None
    ) -> typing.Optional[Conversation]:
        assert conversation_id is not None, "Conversation id cannot be None"
        assert messages_limit is None or messages_limit >= 0, "Messages limit must be greater than or equal to 0"

        conn: sqlite3.Connection | None = None
        try:
            conn = self._get_connection()
            conversation_row = conn.execute(SQLiteSchema.GET_CONVERSATION, (conversation_id,)).fetchone()
            if not conversation_row:
                logger.debug(f"SQLiteStorage got conversation {conversation_id} not found")
                return None

            if messages_limit is not None:
                message_rows = conn.execute(
                    SQLiteSchema.LIST_MESSAGES,
                    (conversation_id, messages_limit)
                ).fetchall()
            else:
                message_rows = conn.execute(
                    SQLiteSchema.GET_MESSAGES,
                    (conversation_id,)
                ).fetchall()

            messages = [self._row_to_message(row) for row in message_rows]
            return self._row_to_conversation(conversation_row, messages)
        except sqlite3.Error as e:
            logger.error(f"Database error while getting conversation {conversation_id}: {e}")
            raise DatabaseOperationError(
                f"Database error while getting conversation {conversation_id}: {e}"
            ) from e
        finally:
            if conn:
                conn.close()

    def list_conversations(self, user_id: str, page_no: int = 1, page_size: int = 10) -> typing.List[Conversation]:
        assert page_no >= 1, "Page number must be greater than or equal to 1"
        assert page_size >= 1, "Page size must be greater than or equal to 1"

        conn: sqlite3.Connection | None = None
        conversations = []
        try:
            offset = (page_no - 1) * page_size
            limit = page_size
            conn = self._get_connection()
            rows = conn.execute(
                SQLiteSchema.LIST_CONVERSATIONS,
                (user_id, limit, offset)
            ).fetchall()
            conversations = [self._row_to_conversation(row, []) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Database error while listing conversations: {e}")
            raise DatabaseOperationError(f"Database error while listing conversations: {e}") from e
        finally:
            if conn:
                conn.close()
            return conversations

    def rename_conversation(self, conversation_id: str, new_name: str) -> bool:
        assert conversation_id is not None, "Conversation id cannot be None"
        assert new_name is not None, "New name cannot be None"

        conn: sqlite3.Connection | None = None
        ret = True
        try:
            conn = self._get_connection()
            conn.execute(SQLiteSchema.RENAME_CONVERSATION, (new_name, conversation_id))
            conn.commit()
            logger.debug(f"SQLiteStorage renamed conversation {conversation_id} to {new_name}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error while renaming conversation {conversation_id} to {new_name}: {e}")
            ret = False
            raise DatabaseOperationError(f"Database error while listing conversations: {e}") from e
        finally:
            if conn:
                conn.close()
            return ret

    def delete_conversation(self, conversation_id: str) -> bool:
        assert conversation_id is not None, "Conversation id cannot be None"

        conn: sqlite3.Connection | None = None
        ret = True
        try:
            conn = self._get_connection()
            conn.execute(SQLiteSchema.DELETE_CONVERSATION, (conversation_id,))
            conn.commit()
            logger.debug(f"SQLiteStorage deleted conversation {conversation_id}")
        except sqlite3.Error as e:
            logger.error(f"Database error while deleting conversation {conversation_id}: {e}")
            ret = False
            raise DatabaseOperationError(f"Database error while listing conversations: {e}") from e
        finally:
            if conn:
                conn.close()
            return ret

    def search_conversations(self, query: typing.Dict[str, any]) -> typing.List[Conversation]:
        # TODO 支持语义搜索
        assert query is not None, "Query cannot be None"

        conn: sqlite3.Connection | None = None
        conversations = []
        conditions = []
        params = []
        try:
            if "metadata" in query:
                if not isinstance(query["metadata"], dict):
                    raise ValueError("Metadata search criteria must be a dictionary")
                for key, value in query["metadata"].items():
                    conditions.append(f"json_extract(metadata, '$.{key}') = ?")
                    params.append(value)

            if "content" in query:
                if not isinstance(query["content"], str):
                    raise ValueError("Content search criteria must be a string")
                conditions.append(
                    """
                    id IN (
                        SELECT DISTINCT conversation_id
                        from message
                        WHERE content LIKE ?
                    )
                    """
                )
                params.append(f"%{query['content']}%")
            if not conditions:
                return []

            sql = f"""
            SELECT * FROM conversation
            WHERE {" AND ".join(conditions)}
            ORDER BY updated_at DESC
            """

            conn = self._get_connection()
            rows = conn.execute(sql, params).fetchall()

            for row in rows:
                conversations.append(self._row_to_conversation(row, []))
        except sqlite3.Error as e:
            logger.error(f"Database error while searching conversations: {e}")
            raise DatabaseOperationError(f"Database error while listing conversations: {e}") from e
        finally:
            if conn:
                conn.close()
            return conversations

    def get_message(self, message_id: str) -> Message | None:
        assert message_id is not None, "Message id cannot be None"
        conn: sqlite3.Connection | None = None
        try:
            conn = self._get_connection()
            message_row = conn.execute(SQLiteSchema.GET_MESSAGE, (message_id,)).fetchone()
            if message_row is None:
                logger.debug(f"SQLiteStorage message {message_id} not found")
                return None
            return self._row_to_message(message_row)
        except sqlite3.Error as e:
            logger.error(f"Database error while getting message {message_id}: {e}")
            raise DatabaseOperationError(f"Database error while getting message {message_id}: {e}") from e
        finally:
            if conn:
                conn.close()
