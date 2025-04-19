import enum
from _typeshed import Incomplete

__all__ = ['n_valveServerQuery', 'query_type']

class NtsuQueryError(Exception): ...

class query_type(enum.Enum):
    SteamAPI = 0
    A2S = 1

class n_valveServerQuery:
    class server_info:
        server_ip: Incomplete
        server_port: Incomplete
        server_name: Incomplete
        server_transname: Incomplete
        server_onlineplayer_count: Incomplete
        server_maxplayer_count: Incomplete
        server_mapname: Incomplete
        game: Incomplete
        timeout: Incomplete
        gametype: Incomplete
        querystatus: Incomplete
        def __init__(self, server_ip: str, server_port: int, server_name: str = None, server_onlineplayer_count: int = None, server_maxplayer_count: int = None, server_mapname: str = None, game: str = None, timeout: int = None, gametype: Incomplete | None = None, querystatus: bool = False) -> None: ...
        def is_error(self): ...
    timeout: Incomplete
    retrytimes: Incomplete
    encoding: Incomplete
    header: Incomplete
    session: Incomplete
    steamwebapikey: Incomplete
    def __init__(self, timeout: float, encoding: str, steamwebapikey: str, retrytimes: int = 0) -> None: ...
    @classmethod
    def resolve_domain_to_ip(cls, domain): ...
    def query_servers(self, addresses: list, q_type: query_type, max_workers: int = 5, group: int = 2, interval: float = 0.1) -> list[server_info]: ...
