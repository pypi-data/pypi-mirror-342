import concurrent
import enum
import json
import re
import socket
import time
import itertools
import a2s
import requests

__all__ = ["n_valveServerQuery","query_type"]

class NtsuQueryError(Exception):
    pass

class query_type(enum.Enum):
    SteamAPI = 0
    A2S = 1

# 用于查询V社的游戏服务器状态
class n_valveServerQuery:
    # 内部类 存储服务器的具体信息
    class server_info:
        def __init__(
                self,
                server_ip: str,
                server_port: int,
                server_name: str = None,
                server_onlineplayer_count: int = None,
                server_maxplayer_count: int = None,
                server_mapname: str = None,
                game: str = None,
                timeout: int = None,
                gametype = None,
                querystatus: bool = False
        ):
            self.server_ip = server_ip
            self.server_port = server_port
            self.server_name = server_name
            self.server_transname = None
            self.server_onlineplayer_count = server_onlineplayer_count
            self.server_maxplayer_count = server_maxplayer_count
            self.server_mapname = server_mapname
            self.game = game
            self.timeout = timeout
            self.gametype = gametype
            self.querystatus = querystatus

        def is_error(self):
            return not self.querystatus
        def __str__(self):
            return str(
                'ip: ' + self.server_ip +
                ' port: ' + str(self.server_port) +
                ' gamentype: ' + str(self.gametype) +
                ' name: ' + (self.server_name if self.server_name else 'N/A') +
                ' transname: ' + (self.server_transname if self.server_transname else 'N/A') +
                ' onlineplayer_count: ' + (
                    str(self.server_onlineplayer_count) if self.server_onlineplayer_count is not None else 'N/A') +
                ' maxplayer_count: ' + (
                    str(self.server_maxplayer_count) if self.server_maxplayer_count is not None else 'N/A') +
                ' mapname: ' + (self.server_mapname if self.server_mapname else 'N/A') +
                ' game: ' + (self.game if self.game else 'N/A') +
                ' timeout: ' + (str(self.timeout) if self.timeout is not None else 'N/A') +
                ' specmode: ' + str(self.specmode) +
                ' querystatus: ' + str(self.querystatus)
            )
    """
    简单用法
        nvsq = n_valveServerQuery(5,'utf-8', "your_steamWebApikey")
        info = nvsq.query_servers([('202.189.10.206',27001),('202.189.10.14',27001)], query_type.A2S)
        print(info[0].server_name)
        print(info[1].server_name)
    """
    def __init__(self, timeout:float,encoding:str, steamwebapikey:str,retrytimes=0):
        self.timeout = timeout
        self.retrytimes = retrytimes
        self.encoding = encoding
        requests.adapters.DEFAULT_RETRIES = 2
        requests.packages.urllib3.disable_warnings()
        self.header = {'Connection': 'close'}
        self.session = requests.session()
        self.steamwebapikey = steamwebapikey
    # 用于解析域名
    @classmethod
    def resolve_domain_to_ip(cls, domain):
        # 分离域名和端口
        if ':' in domain:
            domain, port = domain.split(':')
        else:
            port = None
        # 获取域名的 IP 地址
        ip = socket.gethostbyname(domain)
        if port:
            return f"{ip}:{port}"
        else:
            return ip
    def _a2s_toServerInfoClass(self, response_string:str) -> server_info:
        ip_port_pattern = re.compile(r"Server: \('([^']*)', (\d+)\)")
        ip_port_match = ip_port_pattern.search(response_string)
        if ip_port_match:
            ip = ip_port_match.group(1)
            port = int(ip_port_match.group(2))
        else:
            raise NtsuQueryError('查询的字符串有误')
        try:
            server_name_pattern = re.compile(r"server_name='(.*?)'")
            player_count_pattern = re.compile(r"player_count=(\d+)")
            max_players_pattern = re.compile(r"max_players=(\d+)")
            map_name_pattern = re.compile(r"map_name='(.*?)'")
            ping_pattern = re.compile(r"ping=([\d\.]+)")
            game_pattern = re.compile(r"game='(.*?)'")
            server_name = server_name_pattern.search(response_string).group(1)
            server_onlineplayer_count = player_count_pattern.search(response_string).group(1)
            server_maxplayer_count = max_players_pattern.search(response_string).group(1)
            origin_mapname = map_name_pattern.search(response_string).group(1)
            server_mapname = origin_mapname
            game = game_pattern.search(response_string).group(1)
            timeout = ping_pattern.search(response_string).group(1)
            serverinfo = self.server_info(ip,
                                          port,
                                          server_name,
                                          server_onlineplayer_count,
                                          server_maxplayer_count,
                                          server_mapname,
                                          game,
                                          timeout,
                                          querystatus=True)
            return serverinfo
        except:
            error_serverinfo = self.server_info(ip,port)
            return error_serverinfo
    def _a2s_query_server(self, server_address):
        try:
            server_info = a2s.info(address=server_address, timeout=self.timeout, encoding=self.encoding)
            return f"Server: {server_address}, Info: {server_info}"
        except Exception as e:
            # 重试次数
            retrytimes = self.retrytimes
            while retrytimes >= 0:
                retrytimes = retrytimes -1
                if retrytimes < 0:
                    return f"Server: {server_address}, Error: {e}"
                else:
                    try:
                        server_info = a2s.info(address=server_address, timeout=self.timeout, encoding=self.encoding)
                        return f"Server: {server_address}, Info: {server_info}"
                    except:
                        continue
    #解析并处理steamapi查询的结果
    def _steam_toServerInfoClass(self, response_string:str) -> server_info:
        ip_port_pattern = re.compile(r"Server: \('([^']*)', (\d+)\)")
        ip_port_match = ip_port_pattern.search(response_string)
        if ip_port_match:
            ip = ip_port_match.group(1)
            port = int(ip_port_match.group(2))
        else:
            raise NtsuQueryError('查询的字符串有误')
        try:
            # 提取后半段json
            # 部分暂时没有用到
            match = re.search(r"Info: ({.*})$", response_string)
            if match:
                json_str = match.group(1)
                # 使用 eval 将字符串转换为 Python 字典
                info_data = eval(json_str)
                s_info = info_data['response']['servers'][0]
                # 清单
                r_name = s_info['name']
                r_product = s_info['product']
                r_players = s_info['players']
                r_max_players = s_info['max_players']
                r_map = s_info['map']
                r_gametype = s_info['gametype']
                serverinfo = self.server_info(ip,
                                              port,
                                              r_name,
                                              r_players,
                                              r_max_players,
                                              r_map,
                                              r_product,
                                              0,
                                              gametype=r_gametype,
                                              querystatus=True)
                # print('查询: ', ip_address, ":", port, "成功")
                return serverinfo
            # 如果正则表达式匹配不到json 可能是服务器没开启 或者网络问题
            else:
                # print('[SteamWebAPI] 查询: ', ip, ":", port, "失败, 可能是网络问题或服务器未开启")
                raise NtsuQueryError(msg='查询失败,没有匹配到符合的json数据')
        # 无法查询 域名 检测正则表达式与域名的匹配
        except:
            error_serverinfo = self.server_info(server_ip=ip, server_port=port)
            return error_serverinfo
    # 使用steamapi查询 并返回网页结果
    def _steam_query_server(self, server_address) -> str:
        u_ip = self.resolve_domain_to_ip(server_address[0])

        url = (
               f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?"
               f"key={self.steamwebapikey}"
               f"&filter=\\appid\\730\\gameaddr\\{u_ip}:{server_address[1]}\\&limit=1"
        )

        try:
            req = self.session.get(url, headers=self.header, verify=False, timeout=5)
            req.close()
            datas = json.loads(req.text)
            return f"Server: {server_address}, Info: {datas}"
        except Exception as e:
            return f"Server: {server_address}, Error: {e}"

    def _batched(self, iterable, n):
        """将可迭代对象分割成长度为n的批次"""
        it = iter(iterable)
        while True:
            batch = list(itertools.islice(it, n))
            if not batch:  # 如果批次为空，终止循环
                break
            yield batch

    def query_servers(self, addresses: list, q_type: query_type, max_workers=5, group=2, interval: float = 0.1) -> \
    list[server_info]:
        # 根据查询类型选择适当的处理函数
        if q_type == query_type.SteamAPI:
            query_func = self._steam_query_server
            convert_func = self._steam_toServerInfoClass
        elif q_type == query_type.A2S:
            query_func = self._a2s_query_server
            convert_func = lambda x: self._a2s_toServerInfoClass(x)
        else:
            raise NtsuQueryError('query_type 传入错误')

        result = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            if group <= 0:
                # group=0或负数时，不使用分组机制
                futures = {executor.submit(query_func, address): address for address in addresses}
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result.append(convert_func(future.result()))
                    except Exception as e:
                        continue
            else:
                # 分组处理
                for group in self._batched(addresses, group):
                    # 提交当前组的任务
                    futures = {executor.submit(query_func, address): address for address in group}
                    # 等待当前组所有任务完成
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            result.append(convert_func(future.result()))
                        except Exception as e:
                            continue
                    # 如果不是最后一组，则等待间隔时间
                    if len(result) < len(addresses):
                        time.sleep(interval)
        return result