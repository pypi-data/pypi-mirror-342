import os
import volcenginesdkcore
import volcenginesdkescloud
from dotenv import load_dotenv


def create_cloudsearch_client(region_id: str) -> volcenginesdkescloud.ESCLOUDApi:
    """创建火山引擎云搜索服务客户端"""
    load_dotenv()
    config = {
        "ak": os.getenv("VOLC_ACCESSKEY"),
        "sk": os.getenv("VOLC_SECRETKEY"),
    }
    if region_id is not None:
        config["region"] = region_id

    configuration = volcenginesdkcore.Configuration()
    configuration.ak = config["ak"]
    configuration.sk = config["sk"]
    configuration.region = config["region"]
    configuration.client_side_validation = True
    return volcenginesdkescloud.ESCLOUDApi(volcenginesdkcore.ApiClient(configuration))
