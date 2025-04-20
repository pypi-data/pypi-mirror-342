# -*- coding: utf-8 -*-
"""
-*- coding: utf-8 -*-
@Time    : 2025/4/20 10:37
@Author  : jayden
"""


import os
import shutil


class CreateSetting:
    def create(self):
        if os.path.exists("setting.py"):
            confirm = input("配置文件已存在 是否覆盖 (y/n).  ")
            if confirm != "y":
                print("取消覆盖  退出")
                return

        template_file_path = os.path.abspath(
            os.path.join(__file__, "../../../templates/project_template/setting.py")
        )
        shutil.copy(template_file_path, "./", follow_symlinks=False)
        print("配置文件生成成功")
