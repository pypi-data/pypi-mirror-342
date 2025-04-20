#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
引文服务器模块（Server Module）

处理用户请求并直接调用Worker API进行处理，不再使用队列通信。
使用Cache存储和检索搜索结果。

Exposed Tools:
- search_keyword: 搜索指定关键词并获取相关引用
"""

import asyncio
import json
import os
import sys
import time
import uuid
from typing import Dict, List, Any, Optional

# 导入MCP服务器模块
try:
    from mcp.server.models import InitializationOptions
    import mcp.types as types
    from mcp.server import NotificationOptions, Server
    import mcp.server.stdio
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP不可用。请安装: pip install mcp-py")

# 尝试导入dotenv支持环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 导入Worker模块
try:
    from src.worker import Worker
except ImportError:
    try:
        from worker import Worker
    except ImportError:
        print("Worker模块不可用")
        raise ImportError("Worker模块不可用")

# 初始化MCP服务器
server = Server("CNKS Server")

# 创建全局Worker实例
worker_instance = Worker()

# 存储正在处理的请求
active_requests = {}

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    列出可用资源
    """
    return []

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """
    读取指定URI的资源内容
    """
    raise ValueError(f"不支持的URI方案: {uri}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    列出可用的提示模板
    """
    return []

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    获取指定名称的提示模板
    """
    raise ValueError(f"未知提示模板: {name}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出服务器提供的可用工具
    
    Returns:
        list: 可用工具列表及其参数描述
    """
    return [
        types.Tool(
            name="search_keyword",
            description="搜索指定关键词并获取相关引用",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "要搜索的关键词"}
                },
                "required": ["keyword"]
            }
        )
    ]

class ToolHandler:
    """
    工具处理器基类
    """
    def __init__(self):
        pass

    async def handle(self, name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        raise NotImplementedError("子类必须实现handle方法")

class SearchKeywordToolHandler(ToolHandler):
    async def handle(self, name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        keyword = arguments.get("keyword", "")
        
        if not keyword:
            return [types.TextContent(type="text", text="错误: 关键词不能为空")]
        
        message_id = str(uuid.uuid4())
        print(f"开始处理关键词: {keyword}")
        
        try:
            # 记录请求
            active_requests[message_id] = {
                "keyword": keyword,
                "status": "processing",
                "timestamp": time.time()
            }
            
            # 调用Worker API处理关键词
            result = await worker_instance.process_keyword(keyword)
            
            # 更新请求状态
            active_requests[message_id]["status"] = "completed"
            
            # 返回结果
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
        except Exception as e:
            error_msg = f"处理关键词 '{keyword}' 时出错: {str(e)}"
            print(error_msg)
            
            # 更新请求状态
            active_requests[message_id]["status"] = "error"
            active_requests[message_id]["error"] = str(e)
            
            return [types.TextContent(type="text", text=f"错误: {error_msg}")]

# 工具处理器映射表
tool_handlers = {
    "search_keyword": SearchKeywordToolHandler()
}

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    处理客户端工具调用请求
    
    Args:
        name: 工具名称
        arguments: 工具参数字典
    
    Returns:
        list: 包含文本或图像内容的响应
    """
    print(f"收到工具调用请求: {name}, 参数: {arguments}")
    
    if name in tool_handlers:
        return await tool_handlers[name].handle(name, arguments)
    else:
        print(f"未知工具: {name}")
        return [types.TextContent(type="text", text=f"错误: 未知工具: {name}")]

def cleanup_expired_requests():
    """清理过期的请求"""
    current_time = time.time()
    expired_ids = []
    
    for msg_id, request in active_requests.items():
        # 超过30分钟的请求视为过期
        if current_time - request["timestamp"] > 1800:
            expired_ids.append(msg_id)
    
    # 移除过期请求
    for msg_id in expired_ids:
        active_requests.pop(msg_id, None)
        print(f"已清理过期请求: {msg_id}")

async def handle_simple_request(reader, writer):
    """
    处理简单的JSON请求并返回结果
    
    这是一个简化的通信协议，用于在MCP协议不可用时提供服务
    """
    try:
        # 读取请求
        request_line = await reader.readline()
        if not request_line:
            print("收到空请求")
            return
            
        request_data = json.loads(request_line.decode('utf-8'))
        print(f"收到请求: {request_data}")
        
        # 处理请求
        if request_data.get("type") == "tool_call":
            tool_name = request_data.get("tool")
            params = request_data.get("params", {})
            
            if tool_name == "search_keyword":
                # 获取参数
                keyword = params.get("keyword", "")
                
                if not keyword:
                    response = {"status": "error", "message": "关键词不能为空"}
                else:
                    # 调用处理器
                    handler = tool_handlers.get("search_keyword")
                    
                    if handler:
                        result_content = await handler.handle("search_keyword", params)
                        if result_content and len(result_content) > 0:
                            # 从TextContent提取JSON字符串并解析
                            try:
                                result_data = json.loads(result_content[0].text)
                                response = {
                                    "status": "success", 
                                    "result": result_data
                                }
                            except json.JSONDecodeError:
                                response = {
                                    "status": "success", 
                                    "result": {"message": result_content[0].text}
                                }
                        else:
                            response = {"status": "error", "message": "处理器未返回结果"}
                    else:
                        response = {"status": "error", "message": "找不到工具处理器"}
            else:
                response = {"status": "error", "message": f"未知工具: {tool_name}"}
        else:
            response = {"status": "error", "message": f"未知请求类型: {request_data.get('type')}"}
        
        # 发送响应
        writer.write(json.dumps(response, ensure_ascii=False).encode('utf-8') + b'\n')
        await writer.drain()
        
    except json.JSONDecodeError:
        print("无法解析JSON请求")
        writer.write(json.dumps({"status": "error", "message": "无法解析JSON请求"}).encode('utf-8') + b'\n')
        await writer.drain()
    except Exception as e:
        print(f"处理请求时出错: {str(e)}")
        writer.write(json.dumps({"status": "error", "message": f"服务器错误: {str(e)}"}).encode('utf-8') + b'\n')
        await writer.drain()
    finally:
        writer.close()

async def run_simple_server():
    """运行简单的JSON请求-响应服务器"""
    # 获取配置
    host = os.environ.get("CNKS_HOST", "127.0.0.1")
    port = int(os.environ.get("CNKS_PORT", "8000"))
    
    server = await asyncio.start_server(
        handle_simple_request,
        host,
        port
    )
    
    addr = server.sockets[0].getsockname()
    print(f'简易服务器运行在 {addr}')
    
    async with server:
        await server.serve_forever()

async def main():
    """
    主函数，启动MCP服务器
    """
    try:
        print("正在启动CNKS服务器...")
        
        # 检查MCP是否可用
        if not MCP_AVAILABLE:
            print("MCP模块不可用，使用简单服务器替代")
            await run_simple_server()
            return
        
        # 检查是否从命令行直接运行或被导入
        if sys.stdin.isatty():
            # 命令行运行，启动简单服务器
            print("从命令行运行，启动简单服务器")
            await run_simple_server()
        else:
            # 标准输入/输出流可用，使用stdio模式运行MCP服务器
            print("检测到标准输入/输出流，启动MCP标准服务器")
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="CNKS-server",
                        server_version="0.1.0",
                        capabilities=server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                    ),
                )
            
    except KeyboardInterrupt:
        print("\n收到中断信号，服务器正在关闭...")
    except Exception as e:
        print(f"服务器启动失败: {str(e)}")
    finally:
        # 关闭Worker资源
        try:
            await worker_instance.close()
            print("Worker资源已关闭")
        except Exception as e:
            print(f"关闭Worker资源时出错: {str(e)}")

if __name__ == "__main__":
    # 启动主循环
    asyncio.run(main()) 