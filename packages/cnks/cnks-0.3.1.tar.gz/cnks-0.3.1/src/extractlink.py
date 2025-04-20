#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
链接提取模块（Extract Link Module）

这是一个独立处理链接提取的模块，专门负责从知网搜索结果中提取有效的文章链接。
使用多种选择器和模式匹配技术提取文章链接，确保提取到实际文章页面而非导航页。

主要职责:
1. 分析知网搜索结果页面结构
2. 提取文章详情和摘要链接
3. 过滤非文章链接
4. 返回有效的文章链接列表
"""

import logging
import traceback
import re
from typing import List, Dict, Any

# 设置日志记录器
logger = logging.getLogger("cnks.extractlink")

async def extract_links_from_page(page) -> List[str]:
    """
    从知网搜索结果页面提取文章链接
    
    Args:
        page: Playwright页面对象
        
    Returns:
        List[str]: 提取到的文章链接列表
    """
    logger.info("开始从页面提取文章链接")
    
    try:
        # 首先尝试使用更精确的选择器直接查找文章链接
        specific_selectors = [
            # 知网常见文章链接选择器
            '.result-table-list .result-table-item .left a.fz14',  # 新版知网结果列表
            '.search-result .dl_li .t_title a',                    # 部分旧版结果列表
            '.result-list .article-item h3 a',                     # 另一版本
            '.searchresult .list_item .title a',                   # 再一版本
            '.resultlist .item_title a',                           # 另一种可能格式
            'a[href*="/detail/abstract?"]',                        # 包含abstract的链接
            'a[href*="/article/detail?"]',                         # 包含article/detail的链接
            'a[href*="dbcode="]',                                  # 包含dbcode参数的链接
        ]
        
        # 使用JavaScript执行提取逻辑
        js_extract = """
        (selectors) => {
            const results = {
                links: [],
                debug: {}
            };
            
            // 收集各选择器匹配数量作为调试信息
            for (const selector of selectors) {
                const elements = document.querySelectorAll(selector);
                results.debug[selector] = elements.length;
                
                for (const el of elements) {
                    const href = el.getAttribute('href');
                    if (href && !href.includes('javascript:') && !href.includes('mailto:')) {
                        // 收集链接和相关文本信息帮助验证
                        results.links.push({
                            url: href,
                            text: el.textContent.trim(),
                            selector: selector
                        });
                    }
                }
            }
            
            // 如果上述选择器没有找到任何链接，尝试一个更通用但不太精确的方法
            if (results.links.length === 0) {
                // 查找所有链接并分析
                const allLinks = document.querySelectorAll('a');
                results.debug['allLinks'] = allLinks.length;
                
                for (const link of allLinks) {
                    const href = link.getAttribute('href');
                    const text = link.textContent.trim();
                    
                    // 检查链接是否可能是文章链接
                    if (href && 
                        !href.includes('javascript:') && 
                        !href.includes('mailto:') &&
                        (href.includes('/detail/') || 
                         href.includes('/article/') || 
                         href.includes('cnki.net') && href.includes('dbcode=') ||
                         text.length > 10 && !link.querySelector('img') && // 长文本且不包含图片可能是标题
                         !href.includes('/index') && // 排除导航链接
                         !href.includes('/search') && // 排除搜索链接
                         !href.includes('/help'))) {  // 排除帮助链接
                        
                        results.links.push({
                            url: href,
                            text: text,
                            selector: 'generic'
                        });
                    }
                }
            }
            
            // 如果仍然没有找到链接，记录页面结构用于调试
            if (results.links.length === 0) {
                results.debug.html = document.body.innerHTML.substring(0, 5000); // 前5000字符
            }
            
            return results;
        }
        """
        
        # 执行JavaScript获取链接
        extract_result = await page.evaluate(js_extract, specific_selectors)
        
        # 分析提取结果
        if not extract_result.get('links'):
            logger.warning("未找到任何文章链接")
            # 记录选择器匹配情况
            for selector, count in extract_result.get('debug', {}).items():
                if selector != 'html':  # 不打印HTML内容
                    logger.debug(f"选择器 '{selector}' 匹配到 {count} 个元素")
            
            # 进行截图以便分析
            screenshot_path = "search_results.png"
            await page.screenshot(path=screenshot_path)
            logger.info(f"已保存搜索结果页面截图到 {screenshot_path}")
            
            # 如果提供了HTML调试信息
            if 'html' in extract_result.get('debug', {}):
                logger.debug("页面结构片段:\n" + extract_result['debug']['html'][:500] + "...")
            
            return []
        
        # 从返回的对象中提取URL
        raw_links = [item['url'] for item in extract_result['links']]
        logger.info(f"初步提取到 {len(raw_links)} 个链接")
        
        # 确保所有链接是绝对URL
        page_url = page.url
        processed_links = []
        for link in raw_links:
            # 如果是相对链接，转换为绝对链接
            if not link.startswith('http'):
                if link.startswith('/'):
                    # 从页面URL获取基本域名
                    match = re.match(r'(https?://[^/]+)', page_url)
                    if match:
                        base_url = match.group(1)
                        absolute_link = base_url + link
                        processed_links.append(absolute_link)
                        continue
                # 如果无法处理，跳过
                logger.warning(f"无法处理相对链接: {link}")
                continue
            
            processed_links.append(link)
        
        # 过滤处理后的链接
        filtered_links = filter_article_links(processed_links)
        logger.info(f"过滤后保留 {len(filtered_links)} 个有效文章链接")
        
        # 打印样本链接进行分析
        if filtered_links:
            sample_size = min(5, len(filtered_links))
            sample_links = filtered_links[:sample_size]
            logger.info(f"样本链接分析:")
            for i, link in enumerate(sample_links):
                logger.info(f"样本 {i+1}: {link}")
        
        return filtered_links
        
    except Exception as e:
        logger.error(f"提取链接时出错: {str(e)}")
        logger.error(traceback.format_exc())
        return []

def filter_article_links(links: List[str]) -> List[str]:
    """
    过滤链接列表，只保留可能的知网文章链接
    
    Args:
        links: 需要过滤的链接列表
        
    Returns:
        List[str]: 过滤后的文章链接列表
    """
    # 知网文章URL的常见模式
    article_patterns = [
        # 常见知网文章地址模式
        r'kns\.cnki\.net/([^/]+/)+detail/abstract',
        r'kns\.cnki\.net/([^/]+/)*article/detail',
        r'cnki\.net/kcms/detail/detail\.aspx',
        r'cnki\.net/KCMS/detail/detail\.aspx',
        r'cnki\.net/.*?dbcode=',
        r'academic\.cnki\.net/.*?doi=',
        r'cnki\.com\.cn/Article/CJFDTotal-',
        # 排除明确不是文章的链接
        r'kns\.cnki\.net/.*?/article/',
        r'.*dblp=.*',  # 包含dblp参数
        r'.*dbta=.*'   # 包含dbta参数
    ]
    
    # 编译正则表达式提高效率
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in article_patterns]
    
    # 过滤链接
    filtered_links = []
    for link in links:
        # 跳过明显的非文章链接
        if any(x in link.lower() for x in [
            'index.html', 'help.cnki.net', 'service.cnki.net', 
            'piccache.cnki.net', 'login', 'register', 'my.cnki', 
            'homepage', 'download.aspx', 'member.cnki'
        ]):
            continue
            
        # 检查是否匹配任何文章模式
        is_article = False
        for pattern in patterns:
            if pattern.search(link):
                is_article = True
                break
                
        if is_article:
            filtered_links.append(link)
    
    # 确保链接唯一
    return list(set(filtered_links))

# 独立测试函数
async def test_extract_links(page):
    """
    测试链接提取功能
    
    Args:
        page: Playwright页面对象
        
    Returns:
        Dict: 测试结果
    """
    try:
        links = await extract_links_from_page(page)
        return {
            "success": True,
            "links": links,
            "count": len(links)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "提取链接测试失败"
        }

# 如果直接执行此脚本
if __name__ == "__main__":
    print("链接提取模块 - 必须通过其他模块调用") 