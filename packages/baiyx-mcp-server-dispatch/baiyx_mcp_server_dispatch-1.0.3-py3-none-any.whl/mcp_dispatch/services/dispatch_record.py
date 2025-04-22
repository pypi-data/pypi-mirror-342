from typing import List, Tuple, Dict
from ..utils.config import SUPPLIER_DISPATCH_TABLE
from ..utils.api import create_record, get_record_by_id
from .dispatch_query import get_supplier_by_name

def check_dispatch_status(dispatch_record_ids: List[str], supplier_name: str, dispatch_type: str) -> Tuple[bool, str]:
    """检查外部派车记录是否属于指定供应商和指派类型
    
    Args:
        dispatch_record_ids: 外部派车记录ID列表
        supplier_name: 供应商名称
        dispatch_type: 派车类型
        
    Returns:
        Tuple[bool, str]: (是否已指派给该供应商和类型, 错误信息)
    """
    # 获取供应商ID
    success, supplier_id, error = get_supplier_by_name(supplier_name)
    if not success:
        return False, error
        
    # 派车类型映射
    dispatch_type_map = {
        "提货": "W提货",
        "送货": "W送货",
        "干线": "W干线"
    }
    
    if dispatch_type not in dispatch_type_map:
        return False, f"无效的指派类型: {dispatch_type}"
        
    # 检查每个外部派车记录
    for dispatch_id in dispatch_record_ids:
        success, record, error = get_record_by_id(SUPPLIER_DISPATCH_TABLE, dispatch_id)
        if not success:
            continue
            
        # 检查供应商和派车类型是否匹配
        fields = record.get('fields', {})
        record_supplier_ids = fields.get('供应商', [])
        record_dispatch_type = fields.get('派车类型', [''])[0]
        
        if (record_supplier_ids and supplier_id in record_supplier_ids and 
            record_dispatch_type == dispatch_type_map[dispatch_type]):
            return True, f"已存在派车记录，供应商: {supplier_name}，派车类型: {dispatch_type}"
            
    return False, ""

def create_external_dispatch(supplier_name: str, dispatch_type: str, detail_record_ids: List[str]) -> Tuple[bool, str, str]:
    """创建外部派车记录
    
    Args:
        supplier_name: 供应商名称
        dispatch_type: 派车类型
        detail_record_ids: 货物明细记录ID列表
        
    Returns:
        Tuple[bool, str, str]: (是否成功, 记录ID, 错误信息)
    """
    print(f"\n创建派车记录:")
    print(f"供应商: {supplier_name}")
    print(f"派车类型: {dispatch_type}")
    print(f"货物明细ID: {detail_record_ids}")
    
    # 获取供应商ID
    success, supplier_id, error = get_supplier_by_name(supplier_name)
    if not success:
        print(f"获取供应商ID失败: {error}")
        return False, "", error
    
    print(f"供应商ID: {supplier_id}")
        
    # 创建派车记录
    dispatch_type_map = {
        "提货": "W提货",
        "送货": "W送货",
        "干线": "W干线"
    }
    
    if dispatch_type not in dispatch_type_map:
        return False, "", f"无效的指派类型: {dispatch_type}"
        
    fields = {
        "供应商": [supplier_id],
        "指派类型": [dispatch_type_map[dispatch_type]],
        "未派车货物明细": detail_record_ids
    }
    
    print(f"创建记录字段: {fields}")
    success, data, error = create_record(SUPPLIER_DISPATCH_TABLE, fields)
    if not success:
        print(f"创建记录失败: {error}")
        if isinstance(error, dict):
            print(f"错误详情: {error.get('message', '')}")
        return False, "", error
        
    records = data.get('records', [])
    if not records:
        return False, "", "创建派车记录失败：返回数据为空"
        
    record_id = records[0]['recordId']
    print(f"创建成功，记录ID: {record_id}")
    return True, record_id, "" 