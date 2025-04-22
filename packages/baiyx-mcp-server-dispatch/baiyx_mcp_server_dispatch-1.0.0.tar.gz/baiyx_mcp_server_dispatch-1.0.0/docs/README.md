# MCP 服务文档

这是一个基于 Model Context Protocol (MCP) 的服务集合，包含以下服务：

## 服务列表

1. [Excel 处理服务](./excel_service.md)
   - Excel 工作簿信息获取
   - Excel 数据读写
   - Excel 公式处理

2. [派车服务](./dispatch_service.md)
   - 批量外部派车
   - 多组订单处理
   - 错误处理和结果反馈

## 快速开始

### 安装

```bash
# 安装 Excel 服务
pip install baiyx-mcp-server-excel

# 安装派车服务
pip install baiyx-mcp-server-dispatch
```

### 配置

所有服务都需要配置以下环境变量：

```bash
export API_TOKEN=your_api_token
export BASE_URL=your_base_url
export SPACE_ID=your_space_id
```

## 许可证

MIT

## 作者

baiyx (baiyx@example.com) 