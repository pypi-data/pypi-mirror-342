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
import logging
import os
import traceback
import time
from typing import Dict, List, Any, Optional, Union

# 配置日志记录
try:
    # 尝试使用绝对路径
    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(os.path.dirname(log_dir), "cnks_worker.log")
    
    # 创建处理器
    file_handler = logging.FileHandler(log_file, mode="a")
    console_handler = logging.StreamHandler()
    
    # 设置格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 获取日志记录器并添加处理器
    logger = logging.getLogger("cnks.worker")
    logger.setLevel(logging.DEBUG)
    
    # 移除现有处理器以避免重复
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # 打印确认信息
    print(f"Worker logger initialized, logging to: {log_file}")
    logger.info(f"Worker logging to: {log_file}")
except Exception as e:
    # 回退到基本控制台日志记录
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("cnks.worker")
    logger.error(f"Failed to set up file logging: {str(e)}")
    print(f"Error setting up worker file logging: {str(e)}")

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
        logger.warning("无法导入searcher、citzer或cache模块，功能将受限")

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
        logger.info("Worker初始化完成")
    
    async def process_keyword(self, keyword: str) -> Dict[str, Any]:
        """
        处理关键词请求
        
        Args:
            keyword: 要搜索的关键词
            
        Returns:
            Dict[str, Any]: 包含处理结果的字典
        """
        logger.info(f"处理关键词请求: {keyword}")
        
        try:
            # 检查缓存中是否有该关键词
            if not self.cache.has_keyword(keyword):
                logger.info(f"缓存中没有关键词 {keyword}，执行搜索")
                
                # 使用searcher搜索关键词
                links = await self.searcher.search_keyword(keyword)
                logger.info(f"搜索到 {len(links)} 个链接")
                
                # 将结果存入缓存
                self.cache.add_links(keyword, links)
                logger.info(f"已将关键词 {keyword} 的链接存入缓存")
            else:
                logger.info(f"缓存中已有关键词 {keyword}")
            
            # 将Searcher的浏览器实例共享给Citzer
            if self.searcher.browser_started and not self.citzer.browser_started:
                self.citzer.context = self.searcher.context
                self.citzer.playwright = self.searcher.playwright
                self.citzer.browser_started = True
                logger.info("已将Searcher的浏览器实例共享给Citzer")
            
            # 处理缓存中未处理的链接
            while True:
                # 获取一个未处理的链接
                link = self.cache.get_unprocessed_link(keyword)
                
                if not link:
                    logger.info(f"关键词 {keyword} 的所有链接已处理完毕")
                    break
                
                logger.info(f"处理链接: {link}")
                
                # 使用citzer处理链接
                result = await self.citzer.process_link(link)
                
                if result:
                    # 将结果存入缓存
                    self.cache.add_result(link, result)
                    logger.info(f"已将链接 {link} 的处理结果存入缓存")
                
                # 标记链接为已处理
                self.cache.mark_as_processed(link)
                logger.info(f"已标记链接 {link} 为已处理")
            
            # 获取所有处理结果
            results = self.cache.get_all_results(keyword)
            logger.info(f"关键词 {keyword} 的处理结果数量: {len(results)}")
            
            return {
                "success": True,
                "keyword": keyword,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"处理关键词 {keyword} 时出错: {str(e)}")
            logger.error(traceback.format_exc())
            
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
            except Exception as e:
                logger.warning(f"关闭浏览器时出错: {str(e)}")
    
    async def close(self):
        """关闭工作者资源"""
        try:
            # 确保Citzer不会再尝试使用浏览器
            self.citzer.browser_started = False
            self.citzer.context = None
            self.citzer.playwright = None
            
            # 关闭Searcher的浏览器
            await self.searcher.close_browser()
            logger.info("已关闭工作者资源")
        except Exception as e:
            logger.error(f"关闭工作者资源时出错: {str(e)}")
            logger.error(traceback.format_exc())
        
# 如果作为主程序运行，提供测试功能
async def main():
    """主程序入口"""
    worker = Worker()
    
    try:
        # 测试关键词
        test_keyword = "人工智能"
        print(f"测试处理关键词: {test_keyword}")
        
        # 处理关键词
        result = await worker.process_keyword(test_keyword)
        
        # 打印结果
        print(f"处理结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        # 关闭资源
        await worker.close()

if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())