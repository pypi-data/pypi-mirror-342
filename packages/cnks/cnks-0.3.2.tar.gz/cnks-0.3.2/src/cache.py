#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
缓存模块（Cache Module）

这是一个用于管理关键词、链接和引文数据的缓存模块。
使用临时文件存储和管理结构化数据，以便高效访问和更新。

主要职责:
1. 存储关键词及其关联链接
2. 更新链接为处理后的引文数据
3. 为工作者或服务器提供数据检索
4. 根据服务器请求删除缓存文件
"""

import json
import logging
import os
from typing import Dict, List, Any, Optional, Union

# Configure logging
try:
    # Attempt to use absolute path
    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(os.path.dirname(log_dir), "cnks_cache.log")
    
    # Create handlers
    file_handler = logging.FileHandler(log_file, mode="a")
    console_handler = logging.StreamHandler()
    
    # Set format for both handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Get logger and add handlers
    logger = logging.getLogger("cnks.cache")
    logger.setLevel(logging.DEBUG)
    
    # Remove any existing handlers to avoid duplicates
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Print confirmation
    print(f"Cache logger initialized, logging to: {log_file}")
    logger.info(f"Cache logging to: {log_file}")
except Exception as e:
    # Fallback to basic console logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("cnks.cache")
    logger.error(f"Failed to set up file logging: {str(e)}")
    print(f"Error setting up cache file logging: {str(e)}")

# Cache file path
CACHE_FILE = os.environ.get("CACHE_FILE", "cache.json")

class Cache:
    """Cache class for managing search data."""
    
    def __init__(self):
        """初始化缓存，不需要参数，使用默认路径"""
        logger.debug(f"Cache initialized with default file: {CACHE_FILE}")
    
    def add_links(self, keyword: str, links: List[str]) -> bool:
        """
        添加关键词的链接到缓存
        
        Args:
            keyword: 要存储的关键词
            links: 关联的链接列表
            
        Returns:
            bool: 操作成功返回True，否则返回False
        """
        try:
            return self.store_keyword_and_links(keyword, links)
        except Exception as e:
            logger.error(f"Error adding links for keyword {keyword}: {str(e)}")
            return False
    
    def get(self, keyword: str) -> List[Dict]:
        """获取指定关键词的缓存结果"""
        try:
            if not os.path.exists(CACHE_FILE):
                logger.debug(f"Cache file not found: {CACHE_FILE}")
                return []
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            if cache_data.get("keyword") == keyword:
                results = cache_data.get("results", [])
                logger.info(f"Retrieved {len(results)} results for keyword: {keyword}")
                return results
            else:
                logger.debug(f"Keyword mismatch in cache: {cache_data.get('keyword')} != {keyword}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting cached results: {str(e)}")
            return []
    
    def set(self, keyword: str, results: List[Dict]) -> bool:
        """设置关键词的缓存结果"""
        try:
            cache_data = {
                "keyword": keyword,
                "results": results
            }
            
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(results)} results for keyword: {keyword}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving cache: {str(e)}")
            return False
    
    @staticmethod
    def store_keyword_and_links(keyword: str, links: List[str]):
        """Store keyword and associated links in cache."""
        cache_data = {
            "keyword": keyword,
            "links": links,
            "results": []  # Initially empty, will be replaced with processed citation data
        }
        
        try:
            # Ensure directory exists
            cache_dir = os.path.dirname(os.path.abspath(CACHE_FILE))
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
                logger.info(f"Created cache directory: {cache_dir}")
            
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Stored keyword and {len(links)} links in cache")
            print(f"Cache: stored keyword '{keyword}' with {len(links)} links")
            return True
        except Exception as e:
            logger.error(f"Error storing keyword and links: {str(e)}")
            print(f"Cache error: {str(e)}")
            return False
    
    @staticmethod
    def update_link_with_citation(link: str, citation_data: Dict):
        """Replace a link with processed citation data."""
        try:
            # 读取当前缓存
            if not os.path.exists(CACHE_FILE):
                logger.error("Cache file does not exist, cannot update citation data")
                return False
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            # 检查链接是否已有引文数据
            results = cache_data.get("results", [])
            links = cache_data.get("links", [])
            
            # 移除不需要存储的字段
            filtered_citation_data = citation_data.copy()
            for field in ["url", "journal", "year", "doi"]:
                if field in filtered_citation_data:
                    del filtered_citation_data[field]
            
            # 查找是否存在
            found = False
            for i, result in enumerate(results):
                if "url" in result and result["url"] == link:
                    # 更新现有记录（完全移除url字段）
                    results[i] = filtered_citation_data
                    found = True
                    break
            
            # 如果没找到，添加新记录
            if not found:
                results.append(filtered_citation_data)
                
                # 记录已处理的链接索引（但不在结果中存储url）
                if link in links and "processed_links" not in cache_data:
                    cache_data["processed_links"] = []
                if link in links and link not in cache_data.get("processed_links", []):
                    cache_data["processed_links"].append(link)
            
            # 更新缓存文件
            cache_data["results"] = results
            
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Updated citation data for link: {link}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating citation data: {str(e)}")
            return False
    
    @staticmethod
    def get_links():
        """Get the list of links to be processed."""
        try:
            if not os.path.exists(CACHE_FILE):
                logger.error("Cache file does not exist, cannot get links")
                return []
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            links = cache_data.get("links", [])
            logger.info(f"Retrieved {len(links)} links from cache")
            return links
        
        except Exception as e:
            logger.error(f"Error getting links: {str(e)}")
            return []
    
    @staticmethod
    def get_keyword():
        """Get the cached keyword."""
        try:
            if not os.path.exists(CACHE_FILE):
                logger.error("Cache file does not exist, cannot get keyword")
                return None
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            keyword = cache_data.get("keyword")
            logger.info(f"Retrieved keyword from cache: {keyword}")
            return keyword
        
        except Exception as e:
            logger.error(f"Error getting keyword: {str(e)}")
            return None
    
    @staticmethod
    def get_results():
        """Get all processed citation data."""
        try:
            if not os.path.exists(CACHE_FILE):
                logger.error("Cache file does not exist, cannot get results")
                return []
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            results = cache_data.get("results", [])
            logger.info(f"Retrieved {len(results)} results from cache")
            return results
        
        except Exception as e:
            logger.error(f"Error getting results: {str(e)}")
            return []
    
    @staticmethod
    def delete_cache():
        """Delete the cache file."""
        try:
            if os.path.exists(CACHE_FILE):
                os.remove(CACHE_FILE)
                logger.info(f"Cache file deleted: {CACHE_FILE}")
                return True
            else:
                logger.warning(f"Cache file does not exist, no need to delete: {CACHE_FILE}")
                return True
        
        except Exception as e:
            logger.error(f"Error deleting cache: {str(e)}")
            return False
            
    def has_keyword(self, keyword: str) -> bool:
        """
        检查缓存中是否存在指定关键词的数据
        
        Args:
            keyword: 要检查的关键词
            
        Returns:
            bool: 如果关键词存在于缓存中则返回True，否则返回False
        """
        try:
            if not os.path.exists(CACHE_FILE):
                logger.debug(f"Cache file not found: {CACHE_FILE}")
                return False
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            cached_keyword = cache_data.get("keyword")
            exists = cached_keyword == keyword
            
            if exists:
                logger.info(f"Keyword found in cache: {keyword}")
            else:
                logger.debug(f"Keyword not found in cache: {keyword} (found: {cached_keyword})")
            
            return exists
                
        except Exception as e:
            logger.error(f"Error checking keyword in cache: {str(e)}")
            return False
            
    def get_keyword_data(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        获取指定关键词的完整缓存数据，包括链接和结果
        
        Args:
            keyword: 要获取数据的关键词
            
        Returns:
            Optional[Dict]: 包含关键词数据的字典，如果不存在则返回None
        """
        try:
            if not os.path.exists(CACHE_FILE):
                logger.debug(f"Cache file not found: {CACHE_FILE}")
                return None
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            if cache_data.get("keyword") == keyword:
                logger.info(f"Retrieved complete data for keyword: {keyword}")
                return cache_data
            else:
                logger.debug(f"Keyword mismatch in cache: {cache_data.get('keyword')} != {keyword}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting keyword data from cache: {str(e)}")
            return None
    
    def get_unprocessed_link(self, keyword: str) -> Optional[str]:
        """
        获取一个未处理的链接
        
        Args:
            keyword: 关键词
            
        Returns:
            Optional[str]: 返回一个未处理的链接，如果没有则返回None
        """
        try:
            data = self.get_keyword_data(keyword)
            if not data:
                logger.warning(f"关键词 {keyword} 不存在于缓存中")
                return None
            
            all_links = data.get("links", [])
            processed_links = data.get("processed_links", [])
            
            # 找到第一个未处理的链接
            for link in all_links:
                if link not in processed_links:
                    logger.info(f"找到未处理的链接: {link}")
                    return link
            
            logger.info(f"关键词 {keyword} 的所有链接已处理")
            return None
        except Exception as e:
            logger.error(f"获取未处理链接时出错: {str(e)}")
            return None
    
    def add_result(self, link: str, result: Dict[str, Any]) -> bool:
        """
        添加处理结果到缓存
        
        Args:
            link: 已处理的链接
            result: 包含引用数据的结果
            
        Returns:
            bool: 操作成功返回True，否则返回False
        """
        try:
            return self.update_link_with_citation(link, result)
        except Exception as e:
            logger.error(f"添加结果时出错: {str(e)}")
            return False
    
    def mark_as_processed(self, link: str) -> bool:
        """
        标记链接为已处理
        
        Args:
            link: 要标记的链接
            
        Returns:
            bool: 操作成功返回True，否则返回False
        """
        try:
            if not os.path.exists(CACHE_FILE):
                logger.error("缓存文件不存在，无法标记链接为已处理")
                return False
            
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            # 确保有processed_links字段
            if "processed_links" not in cache_data:
                cache_data["processed_links"] = []
            
            # 如果链接尚未标记为已处理，则添加
            if link not in cache_data["processed_links"]:
                cache_data["processed_links"].append(link)
                
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
                logger.info(f"已标记链接为已处理: {link}")
            else:
                logger.info(f"链接已经被标记为已处理: {link}")
            
            return True
        except Exception as e:
            logger.error(f"标记链接为已处理时出错: {str(e)}")
            return False
    
    def get_all_results(self, keyword: str) -> List[Dict[str, Any]]:
        """
        获取关键词的所有处理结果
        
        Args:
            keyword: 关键词
            
        Returns:
            List[Dict[str, Any]]: 结果列表
        """
        try:
            data = self.get_keyword_data(keyword)
            if not data:
                logger.warning(f"关键词 {keyword} 不存在于缓存中")
                return []
            
            results = data.get("results", [])
            logger.info(f"获取到关键词 {keyword} 的 {len(results)} 个结果")
            return results
        except Exception as e:
            logger.error(f"获取所有结果时出错: {str(e)}")
            return [] 