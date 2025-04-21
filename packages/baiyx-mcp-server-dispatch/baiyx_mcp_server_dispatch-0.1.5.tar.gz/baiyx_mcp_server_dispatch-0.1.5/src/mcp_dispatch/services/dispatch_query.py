from typing import List, Tuple, Dict
from ..utils.config import GOODS_DETAIL_TABLE, SUPPLIER_TABLE, SUPPLIER_VIEW, PENDING_DISPATCH_VIEW
from ..utils.api import get_records, get_records_by_ids

async def get_pending_dispatch_details() -> Dict:
    """获取待指派的货物明细
    
    Returns:
        Dict: {
            "success": bool,  # 是否成功
            "records": List[Dict],  # 记录列表
            "error": str  # 错误信息
        }
    """
    all_records = []
    page_num = 1
    
    while True:
        success, data, error = get_records(
            GOODS_DETAIL_TABLE,
            view_id=PENDING_DISPATCH_VIEW,
            page_size=1000,
            page_num=page_num
        )
        
        if not success:
            return {
                "success": False,
                "records": [],
                "error": error
            }
            
        records = data.get('records', [])
        if not records:
            break
            
        all_records.extend(records)
        total = data.get('total', 0)
        
        if len(all_records) >= total:
            break
            
        page_num += 1
        
    return {
        "success": True,
        "records": all_records,
        "error": ""
    }

def find_records_by_order_numbers(records: List[Dict], order_numbers: List[str]) -> Tuple[List[Dict], List[str], List[str]]:
    """从待指派明细中找到指定订单号对应的记录
    
    Args:
        records: 待指派明细记录列表
        order_numbers: 订单号列表
        
    Returns:
        Tuple[List[Dict], List[str], List[str]]: (匹配的记录列表, 派车记录ID列表, 未找到的订单号列表)
    """
    matched_records = []
    dispatch_record_ids = []
    missing_orders = []
    
    # 检查所有订单号是否都能找到
    for order_number in order_numbers:
        found = False
        for record in records:
            if order_number in record.get('fields', {}).get('订单编号引用', []):
                found = True
                break
        if not found:
            missing_orders.append(order_number)
    
    # 如果有找不到的订单号，直接返回
    if missing_orders:
        return [], [], missing_orders
    
    # 收集所有匹配的记录和派车记录ID
    for record in records:
        order_refs = record.get('fields', {}).get('订单编号引用', [])
        for order_number in order_numbers:
            if order_number in order_refs:
                matched_records.append(record)
                dispatch_ids = record.get('fields', {}).get('供应商派车', [])
                dispatch_record_ids.extend(dispatch_ids)
                break
    
    return matched_records, list(set(dispatch_record_ids)), []

def get_supplier_by_name(supplier_name: str) -> Tuple[bool, str, str]:
    """根据供应商名称查询供应商记录ID
    
    Args:
        supplier_name: 供应商名称
        
    Returns:
        Tuple[bool, str, str]: (是否成功, 供应商ID, 错误信息)
    """
    success, data, error = get_records(
        SUPPLIER_TABLE,
        view_id=SUPPLIER_VIEW,
        filter_formula=f"供应商名称 = '{supplier_name}'",
    )
    
    if not success:
        return False, "", error
        
    records = data.get('records', [])
    if not records:
        return False, "", f"未找到供应商: {supplier_name}"
        
    return True, records[0]['recordId'], "" 