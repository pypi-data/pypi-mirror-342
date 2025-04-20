#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
引文工作者模块（Worker Module）

这是处理引文数据请求的主要模块，处理从服务器接收的关键词，
管理搜索和数据提取流程，并与缓存系统交互。

主要职责:
1. 协调缓存、搜索和内容提取模块之间的交互
2. 处理来自服务器的关键词请求
3. 管理缓存查询和更新
4. 控制处理流程和结果返回
"""

import asyncio
import json
import os
import traceback
import time
from typing import Dict, List, Any, Optional, Union

# 禁用日志记录
class DummyLogger:
    """空日志记录器，用于禁用日志输出"""
    def __init__(self, *args, **kwargs):
        pass
    
    def debug(self, *args, **kwargs):
        pass
    
    def info(self, *args, **kwargs):
        pass
    
    def warning(self, *args, **kwargs):
        pass
    
    def error(self, *args, **kwargs):
        pass
    
    def critical(self, *args, **kwargs):
        pass
    
    def addHandler(self, *args, **kwargs):
        pass
    
    def setLevel(self, *args, **kwargs):
        pass

# 使用空日志记录器
logger = DummyLogger()
print = lambda *args, **kwargs: None  # 禁用print函数

# 导入其他模块
try:
    from src.searcher import Searcher
    from src.citzer import Citzer
    from src.cache import Cache
except ImportError:
    try:
        from searcher import Searcher
        from citzer import Citzer
        from cache import Cache
    except ImportError:
        pass

class Worker:
    """
    工作者类，负责协调搜索、提取和缓存操作
    """
    
    def __init__(self):
        """初始化工作者"""
        # 先创建Searcher实例
        self.searcher = Searcher()
        # 创建Citzer实例，但不让它启动自己的浏览器
        self.citzer = Citzer()
        # 设置标志，以便在使用时借用Searcher的浏览器
        self.citzer.browser_started = False
        # 创建Cache实例
        self.cache = Cache()
    
    async def process_keyword(self, keyword: str) -> Dict[str, Any]:
        """
        处理关键词请求
        
        Args:
            keyword: 要搜索的关键词
            
        Returns:
            Dict[str, Any]: 包含处理结果的字典
        """
        try:
            # 检查缓存中是否有该关键词
            if not self.cache.has_keyword(keyword):
                # 使用searcher搜索关键词
                links = await self.searcher.search_keyword(keyword)
                
                # 将结果存入缓存
                self.cache.add_links(keyword, links)
            
            # 将Searcher的浏览器实例共享给Citzer
            if self.searcher.browser_started and not self.citzer.browser_started:
                self.citzer.context = self.searcher.context
                self.citzer.playwright = self.searcher.playwright
                self.citzer.browser_started = True
            
            # 处理缓存中未处理的链接
            while True:
                # 获取一个未处理的链接
                link = self.cache.get_unprocessed_link(keyword)
                
                if not link:
                    break
                
                # 使用citzer处理链接
                result = await self.citzer.process_link(link)
                
                if result:
                    # 将结果存入缓存
                    self.cache.add_result(link, result)
                
                # 标记链接为已处理
                self.cache.mark_as_processed(link)
            
            # 获取所有处理结果
            results = self.cache.get_all_results(keyword)
            
            return {
                "success": True,
                "keyword": keyword,
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "keyword": keyword,
                "error": str(e)
            }
        
        finally:
            # 只由Worker负责关闭浏览器，Citzer不再单独关闭
            try:
                # 确保Citzer不会再尝试使用浏览器
                self.citzer.browser_started = False
                # 关闭Searcher的浏览器
                await self.searcher.close_browser()
            except Exception:
                pass
    
    async def close(self):
        """关闭工作者资源"""
        try:
            # 确保Citzer不会再尝试使用浏览器
            self.citzer.browser_started = False
            self.citzer.context = None
            self.citzer.playwright = None
            
            # 关闭Searcher的浏览器
            await self.searcher.close_browser()
        except Exception:
            pass
        
# 如果作为主程序运行，提供测试功能
async def main():
    """主程序入口"""
    worker = Worker()
    
    try:
        # 测试关键词
        test_keyword = "人工智能"
        
        # 处理关键词
        result = await worker.process_keyword(test_keyword)
    finally:
        # 关闭资源
        await worker.close()

if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())