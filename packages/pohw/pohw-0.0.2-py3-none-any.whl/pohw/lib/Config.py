# -*- coding: UTF-8 -*-

import toml
from loguru import logger

from pohw.lib.Const import DEFAULT_CONFIG_PATH_NAME, DEFAULT_CONFIG_NAME, TUTORIA_VIDEO


class pohwConfig():
    """
    通过配置文件来验证id和key，现在已经弃用。改为通过函数里传参：id，key
    """

    def __init__(self):
        self.config_info = None

    def get_config(self, configPath):
        """
        解析配置文件
        :param configPath: 配置文件路径
        :return: 加载后的信息
        """
        try:
            if configPath is None:
                self.config_info = toml.load(DEFAULT_CONFIG_PATH_NAME)
            else:
                self.config_info = toml.load(configPath)
            logger.info(f'配置文件【{DEFAULT_CONFIG_NAME}】读取成功')
            return self.config_info
        except:
            logger.info(f'配置文件【{DEFAULT_CONFIG_NAME}】读取失败，请查看视频，进行配置：{TUTORIA_VIDEO}')
