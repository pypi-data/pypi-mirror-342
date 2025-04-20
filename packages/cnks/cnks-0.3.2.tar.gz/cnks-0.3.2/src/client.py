#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MCP Client Module

该模块提供一个简单的命令行客户端，用于与CNKS MCP服务器交互。
使用子进程和stdin/stdout方式与服务器通信。
"""

import argparse
import json
import logging
import sys
import time
import asyncio
import subprocess
import os
from typing import Dict, Any, Optional

# 配置客户端基本日志
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [客户端] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)] # 输出日志到控制台
)
logger = logging.getLogger("mcp.client")

async def run_client(keyword: str, force_refresh: bool = False, timeout: float = 600.0):
    """
    运行客户端并调用服务器工具
    
    通过TCP连接到本地服务器并发送请求
    """
    logger.info(f"尝试连接到CNKS服务器...")
    
    reader = None
    writer = None
    
    try:
        # 连接到服务器
        reader, writer = await asyncio.open_connection('127.0.0.1', 8000)
        logger.info("已连接到服务器")
        
        # 构建请求
        request = {
            "type": "tool_call",
            "tool": "search_keyword",
            "params": {
                "keyword": keyword,
                "force_refresh": force_refresh
            }
        }
        
        # 发送请求
        logger.info(f"发送请求: {json.dumps(request)}")
        writer.write(json.dumps(request).encode() + b"\n")
        await writer.drain()
        
        # 等待响应
        start_time = time.time()
        logger.info(f"等待响应（最长 {timeout} 秒）...")
        
        try:
            response_line = await asyncio.wait_for(reader.readline(), timeout=timeout)
            if response_line:
                response_data = json.loads(response_line.decode().strip())
                
                processing_time = time.time() - start_time
                logger.info(f"收到响应，处理耗时: {processing_time:.2f}秒")
                
                # 检查状态
                if response_data.get("status") == "error":
                    logger.error(f"服务器返回错误: {response_data.get('message', '未知错误')}")
                    return
                
                # 打印响应
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
                
                # 尝试提取统计信息(如果有)
                result = response_data.get("result", {})
                processed = result.get("processed_count", 0) 
                unprocessed = result.get("unprocessed_count", 0)
                newly_processed = result.get("newly_processed", 0)
                
                if processed or unprocessed or newly_processed:
                    logger.info(f"已处理: {processed}, 未处理: {unprocessed}, 新处理: {newly_processed}")
            else:
                logger.error("服务器关闭连接，未收到响应")
                
        except asyncio.TimeoutError:
            logger.error(f"等待响应超时（{timeout}秒）")
        
    except ConnectionRefusedError:
        logger.error("无法连接到服务器。请确保服务器已运行。")
        print("错误: 无法连接到服务器。请先运行服务器（python src/server.py）")
    except Exception as e:
        logger.error(f"客户端操作过程中发生错误: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # 关闭连接
        if writer:
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass

def main():
    """
    客户端的主函数。解析命令行参数
    并与CNKS服务器交互。
    """
    parser = argparse.ArgumentParser(description="向CNKS服务器发送搜索请求。")
    parser.add_argument("keyword", help="要搜索的关键词。")
    parser.add_argument(
        "--timeout",
        type=float,
        default=600.0, # 默认超时600秒
        help="等待服务器响应的超时时间（秒）。"
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="强制刷新缓存，忽略已缓存的内容。"
    )

    args = parser.parse_args()
    
    # 运行异步客户端
    asyncio.run(run_client(args.keyword, args.force_refresh, args.timeout))

if __name__ == "__main__":
    main()