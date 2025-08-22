import base64
import hashlib
import hmac
import json
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

from dotenv import dotenv_values
from typing import Optional


def load_env_config(env_path: str = ".env") -> dict:
    """
    加载并返回 .env 文件中的所有配置
    Args:
        env_path (str): .env 文件的路径，默认为当前目录下的 .env 文件
    Returns:
        dict: 包含所有环境变量的字典
    """
    # 加载 .env 文件
    config = dotenv_values(env_path)
    
    return config





def create_headers(app_id, app_secret, host):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: {}\ndate: {}\n".format(host, date)

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(app_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization = f'hmac api_key={app_id}, algorithm=hmac-sha256, headers=host date request-line, signature={signature_sha_base64}'

        # 将请求的鉴权参数组合为字典
        headers = {
            "X-JZ-AUTHORIZATION": authorization,
            "X-JZ-DATE": date,
            "X-JZ-HOST": host,
			"X-JZ-APPID": app_id
        }

        return headers
		
		
# 入口函数
if __name__ == "__main__":
    # 应用管理 -> 应用详情 -> AppID(复制)
    app_id = "xxxxx"
    # 应用管理 -> 应用详情 -> App Secret Key(复制)
    app_secret = "xxxxx"
    # HOST
    host = "IP"
    # 初始化客户端
    headers = create_headers(app_id, app_secret, host)
    # 生成内容
    print(json.dumps(headers, indent=2))