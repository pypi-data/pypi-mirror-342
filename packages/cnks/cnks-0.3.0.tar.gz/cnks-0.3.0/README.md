# CNKS - 中国知网搜索与引文处理系统

## 简介

CNKS是一个用于搜索中国知网并提取引文数据的工具。该系统能够自动化搜索过程，提取文献信息，并以结构化的方式返回结果。

## 系统架构

CNKS采用服务器-客户端架构，包含以下主要组件：

1. **服务器 (Server)**: 
   - 处理来自客户端的请求
   - 按需调用Worker API处理关键词搜索
   - 管理搜索结果缓存

2. **工作模块 (Worker)**: 
   - 提供搜索和数据提取API
   - 使用Playwright自动浏览网页
   - 解析和提取引文数据
   - 不再作为独立进程运行，而是由服务器直接调用

3. **客户端 (Client)**:
   - 命令行界面，用于发送搜索请求
   - 接收并显示搜索结果

4. **引文处理器 (Citzer)**:
   - 解析和格式化引文数据
   - 支持多种引文格式

## 安装

### 要求

- Python 3.12 或更高版本
- Playwright
- MCP

### 安装步骤

1. 克隆仓库：
   ```
   git clone https://github.com/your-username/cnks.git
   cd cnks
   ```

2. 安装依赖：
   ```
   pip install -e .
   playwright install
   ```

## 使用方法

### 启动服务器

```
cnks
```
或
```
cnks-server
```

### 使用客户端发送请求

```
cnks-client "搜索关键词"
```

选项：
- `--timeout SECONDS`: 设置响应超时时间（默认为60秒）

### 直接测试Worker模块 (仅用于调试)

```
cnks-worker-test "搜索关键词"
```

## 配置

系统可通过以下环境变量进行配置：

- `CACHE_FILE`: 缓存文件路径，默认为 "cache.json"
- `SEARCH_URL`: 搜索URL，默认为中国知网搜索页面

可以创建`.env`文件设置这些环境变量。

## 许可证

[项目许可证信息]