# MCP 派车服务

这是一个基于 MCP (Model Context Protocol) 的派车服务，提供批量外部派车功能。

## 功能特点

- 支持批量外部派车操作
- 支持多组订单号、供应商和指派类型
- 自动处理错误和异常情况
- 提供详细的处理结果反馈

## 安装

```bash
pip install baiyx-mcp-server-dispatch
```

## 使用方法

1. 启动服务：

```bash
baiyx-mcp-server-dispatch
```

2. 调用示例：

```python
from mcp.client import Client

# 创建MCP客户端
client = Client()

# 准备派车数据
dispatch_groups = [
    {
        "order_numbers": ["订单1", "订单2"],
        "supplier_name": "供应商A",
        "dispatch_type": "提货"
    },
    {
        "order_numbers": ["订单3"],
        "supplier_name": "供应商B",
        "dispatch_type": "送货"
    }
]

# 调用批量派车功能
result = await client.batch_external_dispatch(dispatch_groups=dispatch_groups)
print(result)
```

## API说明

### batch_external_dispatch

批量处理外部派车请求。

参数：
- dispatch_groups: List[Dict] - 派车组列表，每个组包含：
  - order_numbers: List[str] - 订单号列表
  - supplier_name: str - 供应商名称
  - dispatch_type: str - 指派类型（"提货"/"送货"/"干线"）

返回值：
```python
{
    "success": bool,  # 是否成功
    "message": str,   # 处理结果消息
    "success_count": int,  # 成功处理的组数
    "failed_groups": List[Dict]  # 失败的组及原因
}
```

## 配置说明

服务使用以下环境变量进行配置：

- API_TOKEN: API访问令牌
- BASE_URL: API基础URL
- SPACE_ID: 空间ID 