# MCP Server 打包发布指南

## 版本更新

1. 修改 `pyproject.toml` 中的版本号：
```toml
[project]
name = "baiyx-mcp-server-dispatch"
version = "x.x.x"  # 更新这里的版本号
```

## 打包步骤

1. 使用 hatch 构建包：
```bash
hatch build
```
这将在 `dist` 目录下生成两个文件：
- `baiyx_mcp_server_dispatch-x.x.x.tar.gz`
- `baiyx_mcp_server_dispatch-x.x.x-py3-none-any.whl`

## 上传步骤

1. 使用 twine 上传指定版本的包：
```bash
twine upload dist/*x.x.x*
```

2. 上传成功后，可以在 PyPI 查看：
https://pypi.org/project/baiyx-mcp-server-dispatch/

## 验证安装

1. 可以使用以下命令验证新版本：
```bash
pip install baiyx-mcp-server-dispatch==x.x.x
```

## 注意事项

1. 每次发布新版本前，确保：
   - 代码已经完成测试
   - 版本号已更新
   - CHANGELOG.md 已更新（如果有）

2. 版本号规范：
   - 主版本号：不兼容的 API 修改
   - 次版本号：向下兼容的功能性新增
   - 修订号：向下兼容的问题修正

3. 如果上传失败：
   - 检查版本号是否重复（最常见的问题）
   - 确认 PyPI token 是否有效
   - 检查网络连接状态

4. 常见问题处理：
   - 如果版本号重复，需要在 pyproject.toml 中更新版本号后重新构建
   - 如果有新的依赖更新，确保在 pyproject.toml 中更新了相应的版本要求 