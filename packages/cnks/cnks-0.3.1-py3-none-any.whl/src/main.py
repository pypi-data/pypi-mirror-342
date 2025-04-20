#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNKS主入口模块

启动服务器组件。在新的通信模式下，worker将被server按需调用，不再作为独立进程运行。
"""

import signal
import sys
import logging
import asyncio

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="cnks_main.log",
    filemode="a"
)
logger = logging.getLogger("cnks.main")

def signal_handler(sig, frame):
    """处理终止信号"""
    logger.info(f"接收到信号 {sig}，正在停止系统...")
    print(f"接收到信号 {sig}，正在停止系统...")
    sys.exit(0)

def main():
    """
    主入口函数，启动服务器
    
    在新的设计中，服务器会按需调用worker的API，
    不再需要单独的worker进程。
    """
    # 捕获终止信号
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("正在启动CNKS系统...")
        print("正在启动CNKS系统...")
        
        # 导入服务器模块
        try:
            from src.server import main as server_main
        except ImportError:
            # 尝试替代导入路径
            from server import main as server_main
        
        logger.info("服务器导入成功，正在启动...")
        
        # 启动服务器 - 使用asyncio.run运行异步函数
        asyncio.run(server_main())
        
    except KeyboardInterrupt:
        logger.info("接收到键盘中断，正在停止系统...")
        print("\n接收到键盘中断，正在停止系统...")
    except Exception as e:
        logger.error(f"系统错误: {str(e)}")
        print(f"系统错误: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        logger.info("系统已停止")
        print("系统已停止")

if __name__ == "__main__":
    main()