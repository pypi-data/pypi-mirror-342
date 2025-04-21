from typing import Tuple, Dict, Any, List
import requests
from .config import Config

def make_request(method: str, url: str, **kwargs) -> Tuple[bool, Dict[str, Any], str]:
    """发送API请求的通用方法
    
    Args:
        method: 请求方法 (GET, POST等)
        url: 请求URL
        **kwargs: 请求参数
        
    Returns:
        Tuple[bool, Dict, str]: (是否成功, 响应数据, 错误信息)
    """
    try:
        headers = kwargs.pop('headers', Config.get_headers())
        print(f"\nAPI请求:")
        print(f"方法: {method}")
        print(f"URL: {url}")
        print(f"参数: {kwargs}")
        
        response = requests.request(method, url, headers=headers, **kwargs)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        if response.status_code not in [200, 201]:
            return False, {}, f"HTTP请求失败: {response.status_code}"
            
        data = response.json()
        if not data.get('success'):
            return False, {}, f"API调用失败: {data.get('message', '未知错误')}"
            
        return True, data.get('data', {}), ""
        
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return False, {}, f"请求异常: {str(e)}"

def get_records(table_id: str, view_id: str = None, filter_formula: str = None, 
                page_size: int = 1000, page_num: int = 1) -> Tuple[bool, Dict[str, Any], str]:
    """获取记录的通用方法
    
    Args:
        table_id: 数据表ID
        view_id: 视图ID
        filter_formula: 过滤公式
        page_size: 每页记录数
        page_num: 页码
        
    Returns:
        Tuple[bool, Dict, str]: (是否成功, 响应数据, 错误信息)
    """
    url = f"{Config().base_url}/datasheets/{table_id}/records"
    params = {
        "pageSize": page_size,
        "pageNum": page_num
    }
    
    if view_id:
        params["viewId"] = view_id
    if filter_formula:
        params["filterByFormula"] = filter_formula
        
    return make_request("GET", url, params=params)

def create_record(table_id: str, fields: Dict) -> Tuple[bool, Dict[str, Any], str]:
    """创建记录的通用方法
    
    Args:
        table_id: 数据表ID
        fields: 记录字段数据
        
    Returns:
        Tuple[bool, Dict, str]: (是否成功, 响应数据, 错误信息)
    """
    url = f"{Config().base_url}/datasheets/{table_id}/records"
    data = {"records": [{"fields": fields}]}
    return make_request("POST", url, json=data)

def update_record(table_id: str, record_id: str, fields: Dict) -> Tuple[bool, Dict[str, Any], str]:
    """更新记录的通用方法
    
    Args:
        table_id: 数据表ID
        record_id: 记录ID
        fields: 要更新的字段数据
        
    Returns:
        Tuple[bool, Dict, str]: (是否成功, 响应数据, 错误信息)
    """
    url = f"{Config().base_url}/datasheets/{table_id}/records"
    data = {"records": [{"recordId": record_id, "fields": fields}]}
    return make_request("PATCH", url, json=data)

def get_records_by_ids(table_id: str, record_ids: List[str]) -> Tuple[bool, Dict[str, Any], str]:
    """通过记录ID获取记录的方法
    
    Args:
        table_id: 数据表ID
        record_ids: 记录ID列表
        
    Returns:
        Tuple[bool, Dict, str]: (是否成功, 响应数据, 错误信息)
    """
    url = f"{Config().base_url}/datasheets/{table_id}/records"
    params = {
        "recordIds": record_ids,
        "fieldKey": "name"
    }
    return make_request("GET", url, params=params)

def get_record_by_id(dst_id: str, record_id: str) -> Tuple[bool, Dict, str]:
    """根据数据表ID和记录ID查询单条记录
    
    Args:
        dst_id: 数据表ID
        record_id: 记录ID
        
    Returns:
        Tuple[bool, Dict, str]: (是否成功, 记录数据, 错误信息)
    """
    success, data, error = get_records_by_ids(dst_id, [record_id])
    
    if not success:
        return False, {}, error
        
    records = data.get('records', [])
    if not records:
        return False, {}, f"未找到记录ID: {record_id}"
        
    return True, records[0], ""

def get_all_records(table_id: str, view_id: str = None, filter_formula: str = None) -> Tuple[bool, List[Dict[str, Any]], str]:
    """获取表格中的所有记录（自动处理分页）
    
    Args:
        table_id: 数据表ID
        view_id: 视图ID
        filter_formula: 过滤公式
        
    Returns:
        Tuple[bool, List[Dict], str]: (是否成功, 所有记录列表, 错误信息)
    """
    all_records = []
    page_size = 1000
    page_num = 1
    
    while True:
        success, data, error = get_records(
            table_id=table_id,
            view_id=view_id,
            filter_formula=filter_formula,
            page_size=page_size,
            page_num=page_num
        )
        
        if not success:
            return False, [], error
            
        records = data.get('records', [])
        if not records:
            break
            
        all_records.extend(records)
        total = data.get('total', 0)
        
        if len(all_records) >= total:
            break
            
        page_num += 1
        
    return True, all_records, "" 