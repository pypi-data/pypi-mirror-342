import os

# 表ID配置
SUPPLIER_DISPATCH_TABLE = "dst4wWd4usqcuQ0K2i"  # 供应商派车表
GOODS_DETAIL_TABLE = "dst7S8RQUovuUPSMuD"  # 货物明细表
SUPPLIER_TABLE = "dstdGpLM8MeLRDp8dG"  # 供应商表
SUPPLIER_VIEW = "viw8Uu737vJTD"  # 供应商视图
PENDING_DISPATCH_VIEW = "viwznDHpD5u3T"  # 待指派视图

# 缓存文件配置
CACHE_FILE = "table_fields_cache.json"
RECORD_CACHE_FILE = "record_cache.json"

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.base_url = os.getenv("MCP_BASE_URL")
            cls._instance.api_token = os.getenv("MCP_API_TOKEN")
            cls._instance.space_id = os.getenv("MCP_SPACE_ID")
        return cls._instance
    
    @classmethod
    def init(cls, base_url: str, api_token: str, space_id: str):
        instance = cls()
        instance.base_url = base_url
        instance.api_token = api_token
        instance.space_id = space_id
    
    @classmethod
    def get_headers(cls):
        instance = cls()
        return {
            "Authorization": f"Bearer {instance.api_token}",
            "Content-Type": "application/json"
        } 