from typing import Dict, List, Any, Tuple
import os
from src.mcp_dispatch.utils.api import get_all_records

def get_vehicles() -> Tuple[bool, List[Dict[str, Any]], str]:
    """获取所有车辆信息
    
    Returns:
        Tuple[bool, List[Dict], str]: (是否成功, 车辆记录列表, 错误信息)
    """
    # 车辆表ID
    table_id = "tblxwIqPwWVoFYqW"
    
    return get_all_records(table_id)

def save_to_markdown(vehicles: List[Dict[str, Any]]) -> None:
    """将车辆信息保存为markdown文件
    
    Args:
        vehicles: 车辆记录列表
    """
    with open("dict/vehicles.md", "w", encoding="utf-8") as f:
        # 写入标题
        f.write("# 车辆信息\n\n")
        
        # 写入表头
        f.write("| 车牌号 | 记录ID |\n")
        f.write("|--------|--------|\n")
        
        # 写入数据行
        for vehicle in vehicles:
            fields = vehicle.get("fields", {})
            plate_number = fields.get("车牌号", "N/A")
            record_id = vehicle.get("recordId", "N/A")
            
            f.write(f"| {plate_number} | {record_id} |\n")

def main():
    # 获取车辆信息
    success, vehicles, error = get_vehicles()
    
    if not success:
        print(f"获取车辆信息失败: {error}")
        return
    
    # 保存为markdown文件
    save_to_markdown(vehicles)
    print(f"成功获取{len(vehicles)}条车辆记录并保存到vehicles.md")

if __name__ == "__main__":
    main() 