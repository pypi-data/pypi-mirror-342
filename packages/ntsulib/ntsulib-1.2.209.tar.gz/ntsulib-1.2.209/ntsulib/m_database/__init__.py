from .n_postgre import *
from .n_dbstatus import *

# 部分.pyd文件打包前需要额外处理
import psycopg2
import psycopg2.sql
import psycopg2.pool