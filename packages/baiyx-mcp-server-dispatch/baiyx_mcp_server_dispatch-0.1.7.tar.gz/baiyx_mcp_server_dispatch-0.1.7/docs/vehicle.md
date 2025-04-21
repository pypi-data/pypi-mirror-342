# 车辆管理

## 功能说明

提供车辆信息的管理功能，包括：

- 车辆基本信息管理
- 车辆状态查询
- 车辆调度记录
- 车辆维护记录

## API接口

### 1. 获取车辆列表

```python
get_vehicles(
    page: int = 1,
    page_size: int = 20,
    status: str = None,
    plate_number: str = None
) -> Dict
```

**参数说明：**
- page: 页码
- page_size: 每页数量
- status: 车辆状态（可选）
- plate_number: 车牌号（可选）

**返回示例：**
```python
{
    "total": 100,
    "items": [
        {
            "id": "v_123",
            "plate_number": "京A12345",
            "vehicle_type": "厢式货车",
            "status": "空闲",
            "current_location": "北京市朝阳区",
            "load_capacity": 5000  # 载重（kg）
        }
    ]
}
```

### 2. 获取车辆详情

```python
get_vehicle_details(vehicle_id: str) -> Dict
```

**参数说明：**
- vehicle_id: 车辆ID

**返回示例：**
```python
{
    "id": "v_123",
    "plate_number": "京A12345",
    "vehicle_type": "厢式货车",
    "status": "空闲",
    "current_location": "北京市朝阳区",
    "load_capacity": 5000,
    "length": 4.2,  # 车长（米）
    "width": 2.1,   # 车宽（米）
    "height": 2.3,  # 车高（米）
    "maintenance_records": [
        {
            "date": "2024-03-01",
            "type": "定期保养",
            "description": "更换机油"
        }
    ],
    "dispatch_records": [
        {
            "date": "2024-03-15",
            "order_number": "O123456",
            "route": "北京-上海"
        }
    ]
}
```

## 使用示例

```python
from mcp.client import Client

# 创建客户端
client = Client()

# 获取车辆列表
vehicles = client.get_vehicles(
    page=1,
    page_size=10,
    status="空闲"
)

# 获取车辆详情
vehicle = client.get_vehicle_details("v_123") 