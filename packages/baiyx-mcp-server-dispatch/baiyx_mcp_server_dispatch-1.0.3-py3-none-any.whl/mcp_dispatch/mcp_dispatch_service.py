from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
from pydantic import BaseModel
import os
from .utils import Config
from .services import (
    get_pending_dispatch_details,
    find_records_by_order_numbers,
    check_dispatch_status,
    create_external_dispatch
)
import uuid
from datetime import datetime

# 创建MCP服务实例
mcp = FastMCP("dispatch-mcp-server", log_level="INFO")

def init_config(base_url: str, api_token: str, space_id: str):
    """初始化配置"""
    Config.init(base_url, api_token, space_id)

@mcp.tool(description="获取待指派的货物明细")
async def mcp_details() -> Dict:
    """获取待指派的货物明细，支持分页查询所有记录
    
    Returns:
        Dict: {
            "success": bool,  # 是否成功
            "records": List[Dict],  # 记录列表
            "error": str  # 错误信息
        }
    """
    return await get_pending_dispatch_details()

@mcp.tool(description="获取当前时间")
async def get_current_time() -> Dict[str, Any]:
    """获取当前时间
    
    Returns:
        Dict[str, Any]: {
            "current_time": str,  # 当前时间，格式：YYYY-MM-DD HH:mm:ss
            "timestamp": int      # 时间戳
        }
    """
    now = datetime.now()
    return {
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(now.timestamp())
    }

class DispatchGroup(BaseModel):
    orderNo: str  # 订单号列表，逗号分隔的字符串
    supplier: str  # 供应商名称
    dispatchType: str  # 指派类型

@mcp.tool(description="批量外部派车，支持多组订单号、供应商和指派类型 1.01")
async def batch_external_dispatch(
    dispatch_groups: List[DispatchGroup]
) -> Dict[str, Any]:
    """批量处理外部派车请求，支持同时处理多个订单组。

    Args:
        dispatch_groups: 派车信息列表，每组包含：
            orderNo (str): 订单号列表，逗号分隔，例如："5000985910,5000985911"
            supplier (str): 供应商名称，例如："上海万创"
            dispatchType (str): 指派类型，可选值："提货"、"送货"、"干线"
            
    Returns:
        Dict[str, Any]: 符合JSON-RPC 2.0规范的响应，包含：
            jsonrpc (str): 版本号，固定为"2.0"
            id (str): 请求ID
            result (Dict): 处理结果，包含：
                success (bool): 是否成功
                message (str): 处理结果消息
                success_count (int): 成功处理的组数
                failed_groups (List[Dict]): 失败的组信息列表
            
    Example:
        >>> dispatch_groups = [
        ...     {
        ...         "orderNo": "5000985910,5000985911",
        ...         "supplier": "上海万创",
        ...         "dispatchType": "提货"
        ...     }
        ... ]
        >>> result = await batch_external_dispatch(dispatch_groups)
    """
    # success_count = 0
    # failed_groups = []
    
    # # 获取所有待指派明细
    # result = await get_pending_dispatch_details()
    # success = result.get("success", False)
    # all_records = result.get("records", [])
    # error = result.get("error", "")
    
    # if not success:
    #     return {
    #         "jsonrpc": "2.0",
    #         "id": str(uuid.uuid4()),
    #         "result": {
    #             "success": False,
    #             "message": f"获取待指派明细失败: {error}",
    #             "success_count": 0,
    #             "failed_groups": dispatch_groups
    #         }
    #     }
    
    # # 处理每组派车请求
    # for group in dispatch_groups:
    #     try:
    #         order_numbers = group.orderNo.split(",") if group.orderNo else []
    #         supplier_name = group.supplier
    #         dispatch_type = group.dispatchType
            
    #         # 参数验证
    #         if not order_numbers or not supplier_name or not dispatch_type:
    #             failed_groups.append({
    #                 **group.dict(),
    #                 "error": "参数不完整"
    #             })
    #             continue
            
    #         # 查找相关记录
    #         matched_records, dispatch_record_ids, missing_orders = find_records_by_order_numbers(
    #             all_records, order_numbers
    #         )
            
    #         # 检查是否所有订单都找到了
    #         if missing_orders:
    #             failed_groups.append({
    #                 **group.dict(),
    #                 "error": f"未找到订单: {', '.join(missing_orders)}"
    #             })
    #             continue
            
    #         # 检查是否已经派车给该供应商
    #         is_dispatched, error = check_dispatch_status(dispatch_record_ids, supplier_name, dispatch_type)
    #         if is_dispatched:
    #             failed_groups.append({
    #                 **group.dict(),
    #                 "error": error
    #             })
    #             continue
            
    #         # 创建派车记录
    #         success, record_id, error = create_external_dispatch(
    #             supplier_name,
    #             dispatch_type,
    #             [record["recordId"] for record in matched_records]
    #         )
            
    #         if not success:
    #             failed_groups.append({
    #                 **group.dict(),
    #                 "error": error
    #             })
    #             continue
            
    #         success_count += 1
            
    #     except Exception as e:
    #         failed_groups.append({
    #             **group.dict(),
    #             "error": f"处理异常: {str(e)}"
    #         })
    
    now = datetime.now()
    return {
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(now.timestamp())
    }

if __name__ == "__main__":
    # 启动MCP服务
    mcp.run(transport="stdio") 