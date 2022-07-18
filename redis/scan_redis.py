# -*- coding: utf-8 -*-

"""
腾讯云 redis scan 示例

有一些需求需要我们扫描 redis 的所有键值，如果用 keys 会阻塞redis 非常危险，推荐用 scan 命令。如果需要扫描一个hash/zset
等也有对应的 hscan, zscan 等命令可以使用。

- 返回的结果可能会有重复，需要客户端去重复，这点非常重要;
- 遍历的过程中如果有数据修改，改动后的数据能不能遍历到是不确定的;
- 单次返回的结果是空的并不意味着遍历结束，而要看返回的游标值是否为零;

参考：https://www.lixueduan.com/post/redis/redis-scan/ Redis Scan 原理解析与踩坑

pip install redis --user
"""

import redis  # pip install redis


def init_redis():
    HOST, PORT, PWD = "host", 6379, "pwd"  # 用你的 redis 配置替代，最好读取配置不要硬编码密码等保证安全
    return redis.Redis(host=HOST, port=PORT, password=PWD)


def get_all_node_ids(r):
    """ 获取所有的腾讯云 redis 集群 master node_id。扫描的需要覆盖所有 master 节点。如果scan 一个复合结构不需要扫所有节点
    u'ip:port@12028': {u'connected': True,                                                                                                                                                                                     [149/176]
                             u'epoch': u'17',
                             u'flags': u'master',
                             u'last_ping_sent': u'0',
                             u'last_pong_rcvd': u'1580544851000',
                             u'master_id': u'-',
                             u'node_id': u'XXXXXXXXXXXXX',
                             u'slots': [[u'8192', u'10239']]},
    """
    from collections import defaultdict
    node_dict = r.execute_command("cluster nodes")
    master_slaves = defaultdict(list)  # {master_id : [slave_ids]}
    for _addr_id, info in node_dict.items():
        if info.get("flags", "") == "slave":
            master_id = info["master_id"]
            master_slaves[master_id].append(info["node_id"])
    master_ids = list(master_slaves.keys())
    slave_ids = []  # 获取其中一个 slave id
    for _, slave_ids in master_slaves.items():
        slave_ids.append(slave_ids[0])
    return master_ids, slave_ids


def scan(r, node_id='', cursor=0, match=None, count=None):
    pieces = [cursor]
    if match is not None:
        pieces.extend([b'MATCH', match])
    if count is not None:
        pieces.extend([b'COUNT', count])
    if node_id:
        pieces.append(node_id)
    return r.execute_command('SCAN', *pieces)


def scan_playcount(r):  # r redis client
    _master_ids, slave_ids = get_all_node_ids(r)
    num = 0
    for node_id in slave_ids:  # scan 每一个 redis slave 节点
        cursor = 0  # reset cursor if error

        while True:
            cursor, keys = scan(r, node_id, cursor, "UR_*", 10000)  # 这里 match 设置你需要的前缀
            for key in set(keys):  # 注意如果不是幂等的，这里可能重复，需要去重
                print(key)  # 这里根据你的需求处理 key

            if cursor == 0:  # 这里说明没有多余数据了，退出
                break
    print("all nums:{}".format(num))


def main():
    redis_client = init_redis()
    scan_playcount(redis_client)


if __name__ == '__main__':
    main()
