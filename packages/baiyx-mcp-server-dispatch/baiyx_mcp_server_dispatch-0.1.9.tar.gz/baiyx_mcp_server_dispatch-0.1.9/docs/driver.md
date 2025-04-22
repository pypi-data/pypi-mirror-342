# 驾驶员管理

## 功能说明

提供驾驶员信息的管理功能，包括：

- 驾驶员基本信息管理
- 驾驶员状态查询
- 驾驶员工作记录
- 驾驶证管理

## API接口

### 1. 获取驾驶员列表

```python
get_drivers(
    page: int = 1,
    page_size: int = 20,
    status: str = None,
    name: str = None
) -> Dict
```

**参数说明：**
- page: 页码
- page_size: 每页数量
- status: 驾驶员状态（可选）
- name: 驾驶员姓名（可选）

**返回示例：**
```python
{
    "total": 50,
    "items": [
        {
            "id": "d_123",
            "name": "张三",
            "phone": "13800138000",
            "status": "在岗",
            "license_type": "A2",
            "years_of_experience": 5
        }
    ]
}
```

### 2. 获取驾驶员详情

```python
get_driver_details(driver_id: str) -> Dict
```

**参数说明：**
- driver_id: 驾驶员ID

**返回示例：**
```python
{
    "id": "d_123",
    "name": "张三",
    "phone": "13800138000",
    "status": "在岗",
    "license_type": "A2",
    "years_of_experience": 5,
    "license_info": {
        "number": "1234567890",
        "valid_until": "2025-12-31",
        "issued_by": "北京市车管所"
    },
    "work_records": [
        {
            "date": "2024-03-15",
            "order_number": "O123456",
            "route": "北京-上海",
            "vehicle": "京A12345"
        }
    ],
    "qualifications": [
        {
            "type": "危险品运输资格证",
            "issued_date": "2022-01-01",
            "valid_until": "2025-12-31"
        }
    ]
}
```

## 使用示例

```python
from mcp.client import Client

# 创建客户端
client = Client()

# 获取驾驶员列表
drivers = client.get_drivers(
    page=1,
    page_size=10,
    status="在岗"
)

# 获取驾驶员详情
driver = client.get_driver_details("d_123") 