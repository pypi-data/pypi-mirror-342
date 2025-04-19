import enum

__all__ = ['Sql_Status', 'Commit_Status', 'Isolation_Status']

class Sql_Status(enum.Enum):
    unconnected = 1
    disconnected = 2
    connected = 3

class Isolation_Status(enum.Enum):
    read_uncommitted = 1
    read_committed = 2
    repeatable_read = 3
    serializable = 4

class Commit_Status(enum.Enum):
    manual_commit = 0
    auto_commit = 1
