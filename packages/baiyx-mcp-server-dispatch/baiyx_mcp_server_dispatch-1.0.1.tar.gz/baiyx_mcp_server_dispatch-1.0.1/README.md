# MCP Excel Server

一个基于 Model Context Protocol (MCP) 的 Excel 处理服务器，提供以下功能：

1. 获取 Excel 工作簿信息
   - 读取所有工作表名称
   - 获取每个工作表的表头
   - 获取数据范围信息

2. 读取 Excel 数据
   - 支持按范围读取数据
   - 支持读取公式

3. 写入 Excel 数据
   - 支持按范围写入数据
   - 支持写入公式

## 安装

```bash
pip install baiyx-mcp-server-excel
```

## 使用方法

启动服务器：

```bash
baiyx-mcp-server-excel
```

## 功能说明

### 1. 获取工作簿信息

```python
get_workbook_info(file_path: str) -> WorkbookInfo
```

返回工作簿中所有工作表的信息，包括表名、表头和数据范围。

### 2. 读取数据

```python
read_sheet_data(file_path: str, sheet_name: str, range: Optional[str] = None) -> ExcelData
```

从指定工作表读取数据，可以指定读取范围（例如："A1:C10"）。

### 3. 读取公式

```python
read_sheet_formula(file_path: str, sheet_name: str, range: Optional[str] = None) -> ExcelFormula
```

从指定工作表读取公式，可以指定读取范围。

### 4. 写入数据

```python
write_sheet_data(file_path: str, sheet_name: str, range: str, data: List[List[Any]]) -> bool
```

向指定工作表写入数据，需要指定写入范围。

### 5. 写入公式

```python
write_sheet_formula(file_path: str, sheet_name: str, range: str, formulas: List[str]) -> bool
```

向指定工作表写入公式，需要指定写入范围。

## 示例

```python
# 获取工作簿信息
workbook_info = get_workbook_info("example.xlsx")
print(f"Found {len(workbook_info.sheets)} sheets")

# 读取数据
data = read_sheet_data("example.xlsx", "Sheet1", "A1:C10")
print(f"Read {len(data.data)} rows")

# 写入数据
success = write_sheet_data("example.xlsx", "Sheet1", "A1", [[1, 2, 3], [4, 5, 6]])
print(f"Write {'successful' if success else 'failed'}")
```

## 依赖

- Python >= 3.10
- mcp >= 1.6.0
- pandas >= 2.0.0
- openpyxl >= 3.1.2

## 许可证

MIT

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

## 开发

1. 克隆代码：

```bash
git clone https://github.com/yourusername/baiyx-mcp-server-dispatch.git
```

2. 安装依赖：

```bash
pip install -e ".[dev]"
```

3. 运行测试：

```bash
pytest
```

## 许可证

MIT

## 作者

baiyx (baiyx@example.com)
