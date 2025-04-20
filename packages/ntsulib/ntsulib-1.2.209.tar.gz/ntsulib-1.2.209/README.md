# ntsulib

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-GPL-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`ntsulib` 是一个多功能工具库，提供异步处理、C 语言交互、加密、PostgreSQL、IO 操作等常用功能封装。

## 功能模块

| 模块               | 描述          | Logo |
|------------------|-------------|------|
| **nasyncthread** | 异步处理工具      | ![AsyncIO](https://img.shields.io/badge/-Asyncio-3776AB?logo=python&logoColor=white) |
| **c**            | C语言交互接口     | ![C](https://img.shields.io/badge/-C-A8B9CC?logo=c&logoColor=white) |
| **nencry**       | 加密解密工具      | ![Crypto](https://img.shields.io/badge/-Cryptography-6DB33F?logo=gnu&logoColor=white) |
| **ndatabase**    | 数据库操作封装     | ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?logo=postgresql&logoColor=white) |
| **serverquery**  | 服务器查询工具     | ![Network](https://img.shields.io/badge/-Network-2496ED?logo=internet-explorer&logoColor=white) |
| **nlogger**      | 日志记录工具      | ![Logging](https://img.shields.io/badge/-Logging-000000?logo=loggly&logoColor=white) |

## 安装

```bash
pip install ntsulib
```

## 使用

```python
# 1
import ntsulib as nl
# 2
from ntsulib import *
```

