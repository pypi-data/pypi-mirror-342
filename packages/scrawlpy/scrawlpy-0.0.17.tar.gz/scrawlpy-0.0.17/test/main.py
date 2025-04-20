# -*- coding: utf-8 -*-
# @Time   : 2024/5/1 01:47
import argparse
import importlib

spider_dict = {

}


def spider_entry():
    """
    seed_file_path: seed 文件路径
    spiders: spiders 名称, 有两种方式，一是带模块路径，如 spiders._demo.tls_spider（自动找包），二是不带模块路径，如 tls_spider（手动导入)
    is_debug: 是否开启 debug 模式

    例如
    python3 main.py spiders/_demo/seed/tls_spider_seeds.json _demo.tls_spider 1
    python3 main.py spiders/_demo/seed/tls_spider_seeds.json tls_spider 1

    Args:
        spider:
        seed_file_path:
        is_debug:
        **kwargs:

    Returns:

    """
    params = argparse.ArgumentParser(description="sql执行参数")
    params.add_argument("-s", "--spider", action="store", help="环境", metavar="")
    params.add_argument("-a", "--append", action="append", help="环境", metavar="")
    params.add_argument("-e", "--env", help="环境", metavar="")
    params.add_argument("-d", "--day", help="日期", metavar="")
    params.add_argument("--hour", type=int, help="小时", metavar="")
    params.add_argument("-j", "--job_id", type=str, help="任务id", metavar="")
    params.add_argument("-k", "--url_kind", type=int, help="结果类型", metavar="", default=0)
    # params.add_argument("-t", "--query_type", type=str, help=f"查询类型 {', '.join(query_type_list)}", metavar="")
    params.add_argument("-l", "--limit", type=int, help="查询限制数", metavar="", default=10)
    params.add_argument("-b", "--bot", type=int, help="是否告警", metavar="", default=1)
    args = params.parse_args()
    # if args.append:
    #     print("哈哈哈哈哈")
    #     setattr(Settings, "Append", args.append)
    # logger.info(f"获取 {seed_file_path} file 执行 project {spider} ")
    # if spider_dict.get(spider):
    #     spider_dict.get(spider)(seed_file_path, is_debug)

    spider = args.spider
    print(spider)
    if "." in args.spider:
        _module = "spiders"

        def execute_run_spider(_file_path):
            """
            file_path: spiders._demo.tls_spider
            执行 run_spider 方法
            """
            print(_file_path)
            module = importlib.import_module(_file_path)
            # 统一由 run_spider 方法执行
            run_spider_method = getattr(module, "run_spider")
            # run_spider_method(seed_file_path, is_debug, **kwargs)

        file_path = f"spiders.{spider}"
        if file_path:
            execute_run_spider(file_path)
        else:
            raise Exception(f"spiders {spider} 模块不存在")

    else:
        raise Exception(f"spiders {spider} 未定义")


if __name__ == '__main__':
    # spider_entry("spiders._demo.tls_spider", "spiders/_demo/seed/tls_spider_seeds.json", 1)
    # fire.Fire(spider_entry)
    spider_entry()
