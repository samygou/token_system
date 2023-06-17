import argparse
import logging
import os
import pathlib
import time

import sys
sys.path.append('api/v1')

from internal.modules.logx import Logger
from internal.modules import redisx
from internal.modules import lockx
from internal.modules import schedulerx
from internal.server import new_grpc_server
from internal.service.service import new_service
from internal.biz import new_token_system_use_case
from internal.data import new_token_system_repo
from internal.data import orm
from config import Config

"""
python -m grpc_tools.protoc -I=./api/v1 --python_out=./api/v1 --grpc_python_out=./api/v1 --pyi_out=./api/v1 ./api/v1/pb_token_
system.proto
"""


def _config_logger():
    Logger(
        pathlib.Path(os.path.join(os.path.dirname(__file__), 'logs')).as_posix(),
        'token_system.log'
    ).init()


def _init_redis():
    conf = Config.REDIS()
    redisx.redis = redisx.new_client(**conf.dict())


def _init_distributed_lock(pool: int = 10):
    lockx.lock_pool = lockx.LockPool(pool)
    for _ in range(pool):
        lockx.lock_pool.put(lockx.Lock(redisx.Lock(client=redisx.redis)))


def _init_scheduler():
    schedulerx.cli = schedulerx.new_scheduler()

    if not schedulerx.cli.running:
        schedulerx.cli.start()


def _init_new_modules():
    _config_logger()
    _init_redis()
    _init_distributed_lock()
    _init_scheduler()


def _register_server(port: int):
    """注册rpc服务"""
    # ----------- biz -------------
    token_system_use_case = new_token_system_use_case(new_token_system_repo())

    # ------------ service ------------
    api_svc = new_service(token_system_use_case)

    # ----------- grpc TSL/SSL mode ------------
    with open('./secret-key/server.key', 'rb') as f:
        private_key = f.read()

    with open('./secret-key/server.crt', 'rb') as f:
        certificate = f.read()

    rpc = new_grpc_server(
        port,
        api_svc,
        workers=10,
        options=[('grpc.max_receive_message_length', 30 * 1024 * 1024)],
        private_key=private_key,
        certificate=certificate
    )

    rpc.serve()

    logging.info(f'grpc server register successful, port: {port}')

    try:
        while True:
            time.sleep(Config.ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        rpc.server.stop(0)


def main():
    """main server"""
    parse = argparse.ArgumentParser()
    parse.add_argument('--svc_port', type=int)
    parse.add_argument('--db_ep', type=str, default='127.0.0.1:3306')
    parse.add_argument('--db_auth', type=str, default='root:123456')
    parse.add_argument('--db_name', type=str, default='token_system_db')

    args = parse.parse_args()

    # ------------- init modules -------------
    _init_new_modules()

    # --------------- init db ----------------
    orm.db = orm.new_database_handler(
        db_ep=args.db_ep,
        db_auth=args.db_auth,
        db_name=args.db_name,
        charset='utf8mb4'
    )

    # --------- register rpc server ----------
    _register_server(args.svc_port)


if __name__ == '__main__':
    main()
