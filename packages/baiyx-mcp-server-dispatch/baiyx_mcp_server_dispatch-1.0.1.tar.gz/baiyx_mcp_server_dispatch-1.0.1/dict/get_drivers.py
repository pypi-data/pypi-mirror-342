from mcp_dispatch.utils.api import get_all_records
from mcp_dispatch.utils.config import Config
import os
from dotenv import load_dotenv

def get_drivers_data():
    """获取驾驶员/押运员数据并生成markdown文件"""
    # 加载环境变量
    load_dotenv()
    
    # 初始化配置
    base_url = os.getenv("MCP_BASE_URL")
    api_token = os.getenv("MCP_API_TOKEN")
    space_id = os.getenv("MCP_SPACE_ID")
    
    if not all([base_url, api_token, space_id]):
        print("错误: 请确保设置了所有必要的环境变量")
        return
        
    Config.init(base_url, api_token, space_id)
    
    # 驾驶员/押运员表ID
    table_id = "dstdYQzmdBN56tiPpA"
    
    # 获取所有记录
    success, records, error = get_all_records(table_id)
    
    if not success:
        print(f"获取数据失败: {error}")
        return
        
    if not records:
        print("未找到记录")
        return
        
    # 生成markdown内容
    markdown_content = "# 驾驶员/押运员信息\n\n"
    markdown_content += "| 记录ID | 姓名 | 手机号 | 身份证号 | 角色 | 所属公司 | 状态 |\n"
    markdown_content += "|---------|------|--------|----------|------|----------|------|\n"
    
    for record in records:
        fields = record.get('fields', {})
        record_id = record.get('recordId', 'N/A')
        name = fields.get('姓名', 'N/A')
        phone = fields.get('手机号', 'N/A')
        id_card = fields.get('身份证号', 'N/A')
        role = fields.get('角色', 'N/A')
        company = fields.get('所属公司', 'N/A')
        status = fields.get('状态', 'N/A')
        
        markdown_content += f"| {record_id} | {name} | {phone} | {id_card} | {role} | {company} | {status} |\n"
    
    # 保存到文件
    with open('drivers.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"已生成 drivers.md 文件，共包含 {len(records)} 条记录")

if __name__ == "__main__":
    get_drivers_data() 