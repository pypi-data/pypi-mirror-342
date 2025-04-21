from mcp_dispatch.utils.api import get_all_records
from mcp_dispatch.utils.config import Config
import os
from dotenv import load_dotenv

def get_all_vehicles():
    """获取所有车辆数据"""
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
    success, records, error = get_all_records(table_id)
    
    if not success:
        print(f"获取车辆数据失败: {error}")
        return
    
    # 生成markdown内容
    markdown_content = "# 车辆列表\n\n"
    markdown_content += "| 车牌号 | Record ID |\n"
    markdown_content += "|--------|------------|\n"
    
    for record in records:
        plate_number = record['fields'].get('车牌号', 'N/A')
        record_id = record['recordId']
        markdown_content += f"| {plate_number} | {record_id} |\n"
    
    # 保存到文件
    with open('vehicles.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"成功获取 {len(records)} 个车辆记录")
    print("已保存到 vehicles.md 文件")

if __name__ == "__main__":
    get_all_vehicles() 