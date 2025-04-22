from mcp_dispatch.utils.api import get_records_by_ids
from mcp_dispatch.utils.config import Config
import os
from dotenv import load_dotenv

def get_vehicle_details(record_ids):
    """获取指定车辆记录的详细信息"""
    # 加载环境变量
    load_dotenv()
    
    # 初始化配置
    base_url = os.getenv("MCP_BASE_URL")
    api_token = os.getenv("MCP_API_TOKEN")
    space_id = os.getenv("MCP_SPACE_ID")
    
    if not all([base_url, api_token, space_id]):
        print("错误: 请确保设置了所有必要的环境变量 (MCP_BASE_URL, MCP_API_TOKEN, MCP_SPACE_ID)")
        return
        
    Config.init(base_url, api_token, space_id)
    
    table_id = "dstLyE0xngEyjzAxP1"  # 车辆表ID
    success, data, error = get_records_by_ids(table_id, record_ids)
    
    if not success:
        print(f"获取车辆数据失败: {error}")
        return
        
    records = data.get('records', [])
    if not records:
        print("未找到车辆记录")
        return
        
    print("\n车辆详细信息:")
    print("-" * 50)
    
    for record in records:
        fields = record.get('fields', {})
        print(f"记录ID: {record['recordId']}")
        print(f"车牌号: {fields.get('车牌号', 'N/A')}")
        print(f"车型: {fields.get('车型', 'N/A')}")
        print(f"载重: {fields.get('载重', 'N/A')}")
        print(f"车长: {fields.get('车长', 'N/A')}")
        print(f"所属公司: {fields.get('所属公司', 'N/A')}")
        print(f"车辆状态: {fields.get('车辆状态', 'N/A')}")
        print("-" * 50)

if __name__ == "__main__":
    # 查询车牌号为"9593"的相关记录
    record_ids = [
        "recEp7c5Hp7G3",  # 9593
        "recFM7eftVG4R",  # 9593
        "recoU5bchzbCA"   # 沪E-D9593
    ]
    get_vehicle_details(record_ids) 