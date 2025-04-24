# tools
一个便捷工具包
提供对应的functioncall 与 MCP 功能,硬的可以成包, 那么软的也可以成

## 常规操作

### 导出环境
```
uv export --format requirements-txt > requirements.txt
```
### 更新文档
```
p_updatedocs
mkdocs serve # 预览
mkdocs gh-deploy -d ../.temp # 同步到github网站
```
### 发布
```
p_build
uv publish
```
### 运行测试并同步到测试服务
```
p_test
```

