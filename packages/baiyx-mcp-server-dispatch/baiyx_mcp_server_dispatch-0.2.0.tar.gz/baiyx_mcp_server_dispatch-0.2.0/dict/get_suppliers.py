from mcp_dispatch.utils.api import get_all_records
from mcp_dispatch.utils.config import Config
import os
from dotenv import load_dotenv
from collections import defaultdict

def clean_supplier_name(name):
    """清理供应商名称
    - 去除首尾空格
    - 去除中间多余空格
    - 过滤无效值
    """
    if not name:
        return None
        
    # 转换为字符串并清理空格
    name = str(name).strip()
    # 将多个空格替换为单个空格
    name = ' '.join(name.split())
    
    # 定义无效值列表
    invalid_values = ['NA', 'N/A', '无', '空', '-', '--']
    
    # 检查是否为无效值
    if name.upper() in [v.upper() for v in invalid_values]:
        return None
        
    return name

def get_all_suppliers():
    """获取所有供应商数据"""
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
    
    table_id = "dstdGpLM8MeLRDp8dG"
    success, records, error = get_all_records(table_id)
    
    if not success:
        print(f"获取供应商数据失败: {error}")
        return
    
    # 生成HTML内容
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>供应商列表（去重）</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            h1 {
                color: #333;
            }
            .record-ids {
                font-size: 0.9em;
                color: #666;
                word-break: break-all;
            }
        </style>
    </head>
    <body>
        <h1>供应商列表（去重）</h1>
        <table>
            <tr>
                <th>供应商名称</th>
                <th>Record ID列表</th>
                <th>记录数量</th>
            </tr>
    """
    
    # 使用字典进行去重和分组
    supplier_dict = defaultdict(list)
    for record in records:
        name = clean_supplier_name(record['fields'].get('供应商名称'))
        if name:  # 只添加有效的供应商名称
            supplier_dict[name].append(record['recordId'])
    
    # 转换为列表并排序
    supplier_list = [(name, record_ids) for name, record_ids in supplier_dict.items()]
    supplier_list.sort(key=lambda x: x[0])  # 按供应商名称排序
    
    # 生成HTML表格内容
    for name, record_ids in supplier_list:
        record_ids_str = '<br>'.join(record_ids)
        html_content += f"""            <tr>
                <td>{name}</td>
                <td class="record-ids">{record_ids_str}</td>
                <td>{len(record_ids)}</td>
            </tr>\n"""
    
    html_content += """        </table>
        <p>统计信息：</p>
        <ul>
            <li>供应商总数（去重后）：{}</li>
            <li>记录总数：{}</li>
        </ul>
    </body>
    </html>
    """.format(len(supplier_list), sum(len(ids) for _, ids in supplier_list))
    
    # 保存到文件
    with open('suppliers.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功获取 {len(supplier_list)} 个不同供应商")
    print(f"总记录数：{sum(len(ids) for _, ids in supplier_list)}")
    print("已保存到 suppliers.html 文件")

if __name__ == "__main__":
    get_all_suppliers() 