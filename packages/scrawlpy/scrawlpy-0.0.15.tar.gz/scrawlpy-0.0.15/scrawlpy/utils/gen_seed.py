# -*- coding: utf-8 -*-
# @Time    : 2025/4/19 15:38
# @Author  : jayden

import json
import os.path
import time
import uuid

seed_template = {
    "worker_id": "spider_worker_python_172.20.6.44_9527",
    "worker_type": "python",
    "cur_task": {
        "urls": [
            '{"action":"action_ws_iphone_F0CBC7F5-DAB3-436E-B81F-EF34D50AA4AC_get_advs","id":928139396,"start_time":"2021-09-08 00:27:26","run_type":3,"interval_time":10800,"time_add":1631085080,"end_time":"2021-09-08 23:59:59","scheduler_id":"dispatch_956816439","city":999,"dispatch_id":956816439,"crontab_rule":"","device_id":"F0CBC7F5-DAB3-436E-B81F-EF34D50AA4AC","wave_space":600,"arglist":[{"arglist_name":"ws_iphone_get_list","exec_index":1,"arg_val":"{\\"argument\\":\\"vid=E23EEB7A-729C-3671-C4AE-51D9A7BAF95F\u0026pass-region=1\u0026app_name=aweme\u0026screen_width=750\u0026pass-route=1\u0026device_type=iPhone10,4\u0026js_sdk_version=1.3.0.1\u0026openudid=7a43331d480f5dee14585562974125c7157e8452\u0026aid=1128\u0026channel=App Store\u0026os_api=18\u0026build_number=34008\u0026os_version=13.6\u0026device_platform=iphone\u0026app_version=3.4.0\u0026ac=WIFI\u0026idfa=F0CBC7F5-DAB3-436E-B81F-EF34D50AA4AC\u0026version_code=3.4.0\u0026iid=1319867573869134\u0026device_id=62677636012\u0026count=6\u0026feed_style=0\u0026filter_warn=0\u0026max_cursor=0\u0026pull_type=0\u0026type=0\u0026volume=0.00\u0026min_cursor=0\u0026longitude=119.547036\u0026latitude=26.666818\\", \\"cookies\\": {\\"install_id\\": 1319867573869134, \\"ttreq\\": \\"1$ff0347fa63c7a992df3b67e5d4ce8e6b812c69e9\\"}, \\"headers\\": {\\"Accept\\": \\"*/*\\", \\"Accept-Encoding\\": \\"gzip, deflate\\", \\"X-SS-REQ-TICKET\\": \\"1544164053294\\", \\"sdk-version\\": \\"1\\", \\"Accept-Language\\": \\"zh-Hans;q=1\\", \\"User-Agent\\": \\"Aweme 3.4.0 rv:34008 (iPhone; iOS 13.6; zh_CN) Cronet\\"}}"}]}'
        ],
        "_sys_meta": {
            "spiders": "demo_spider",
            "code_type": "python",
            "code_url": "https://sp-1301995720.cos.ap-shanghai.myqcloud.com/kingsman_spider/v20210913-193616/kingsman-spider.tar.gz",
            "code_version": "v20210913-193616",
            "code_md5": uuid.uuid4().hex,
            "sensitivity": 0,
            "user": "test_user",
            "job_id": uuid.uuid4().hex,
            "job_cron_id": 4073,
            "priority": 0,
            "emergency": False,
            "schedule_type": 1,
            "input_type": 3,
            "output": {"type": 1, "topic": "data_output", "tdw_target": "web_file"},
            "scrapy_spider_parameters": {"scrapy_spider_name": "", "scrapy_spider_directory": "./"},
            "relations": {},
            "create_at": 1631532987,
        },
        "traces": [
            {  # 线上json模版
                "id": "Qgedh9XjAVdfpd5wqoXWzt",
                "job_id": uuid.uuid4().hex,
                "in_ts": int(time.time()),
                "scheduled_recv_ts": int(time.time()),
                "write_storage_ts": int(time.time()),
                "schedule_ts": int(time.time()),
                "already_retry_num": int(time.time()),
            }
        ],
    },
}


def write_seed_json_file(job, spider_name):
    base_file_path = f"{spider_name}_seeds.json"
    base_dir = "seed"
    if not os.path.isdir(base_dir):
        os.mkdir(base_dir)
    seeds_file_path = os.path.join(base_dir, base_file_path)
    if isinstance(job, str):
        seed_template["cur_task"]["urls"] = [job]
    elif isinstance(job, list):
        seed_template["cur_task"]["urls"] = job
    elif isinstance(job, dict):
        seed_template["cur_task"]["urls"] = [json.dumps(job)]
    else:
        raise Exception("seed format exception")

    job_id = str(seed_template["cur_task"]["_sys_meta"]["job_id"])

    # 3.9版本镜像，带trace
    seed_template["cur_task"]["traces"] = []
    for _ in range(len(seed_template["cur_task"]["urls"])):
        seed_template["cur_task"]["traces"].append(
            {
                "id": uuid.uuid4().hex[:6],
                "job_id": job_id,
                "in_ts": int(time.time()),
                "scheduled_recv_ts": int(time.time()),
                "write_storage_ts": int(time.time()),
                "schedule_ts": int(time.time()),
                "already_retry_num": 0,
            }
        )

    with open(seeds_file_path, "w") as f:
        f.write(json.dumps(seed_template))
    return seeds_file_path
