#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
验证检测模块（IfVerify Module）

这个模块用于检测页面是否需要人工验证（如CAPTCHA、验证码等）。
可以被工作者模块和其他需要验证检测的模块引用。

主要职责:
1. 分析页面内容，检测可能的验证元素
2. 辅助交互自动化流程中的人工验证步骤
"""

import logging
import traceback
from typing import Dict, Any

# 获取logger
logger = logging.getLogger("cnks.ifverify")

async def check_verification_needed(page) -> bool:
    """
    检查页面是否需要人工验证
    
    Args:
        page: Playwright页面对象
        
    Returns:
        bool: 是否需要人工验证
    """
    try:
        # 检查是否存在验证相关元素
        verification_elements = [
            # 验证码图片
            'img[src*="captcha"]',
            'img[src*="verify"]',
            # 验证码输入框
            'input[name*="captcha"]',
            'input[placeholder*="验证码"]',
            # 验证提示文本
            'div:has-text("请输入验证码")',
            'div:has-text("安全验证")',
            'div:has-text("请完成验证")'
        ]
        
        for selector in verification_elements:
            element = await page.query_selector(selector)
            if element:
                logger.info(f"检测到验证元素: {selector}")
                return True
            
        # 检查页面标题或URL是否包含验证相关关键词
        title = await page.title()
        url = page.url
        verification_keywords = ["verification", "verify", "captcha", "验证", "安全检查"]
        
        for keyword in verification_keywords:
            if keyword.lower() in title.lower() or keyword.lower() in url.lower():
                logger.info(f"页面标题或URL包含验证关键词: {keyword}")
                return True
        
        logger.info("未检测到需要人工验证的元素")
        return False
        
    except Exception as e:
        logger.warning(f"检查验证页面时出错: {str(e)}")
        logger.warning(traceback.format_exc())
        # 如果出错，保险起见认为需要验证
        return True

async def handle_verification(page, wait_time: int = 10000) -> bool:
    """
    处理可能的人工验证需求
    
    Args:
        page: Playwright页面对象
        wait_time: 等待人工验证的时间（毫秒）
        
    Returns:
        bool: 是否成功处理验证
    """
    try:
        # 检查是否需要验证
        needs_verification = await check_verification_needed(page)
        
        if needs_verification:
            logger.info(f"检测到需要人工验证，等待{wait_time/1000}秒钟...")
            # 等待指定时间让用户进行验证
            await page.wait_for_timeout(wait_time)
            
            # 再次检查是否仍需验证
            still_needs_verification = await check_verification_needed(page)
            if still_needs_verification:
                logger.warning("验证可能尚未完成，但等待时间已到")
                return False
            else:
                logger.info("验证已完成，继续执行")
                return True
        else:
            logger.info("无需人工验证")
            return True
            
    except Exception as e:
        logger.error(f"处理验证过程中出错: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def test_verification_selectors() -> Dict[str, Any]:
    """
    返回用于验证检测的元素选择器列表，
    可用于测试或扩展验证检测能力
    
    Returns:
        Dict: 包含各类验证元素选择器的字典
    """
    return {
        "image_selectors": [
            'img[src*="captcha"]',
            'img[src*="verify"]'
        ],
        "input_selectors": [
            'input[name*="captcha"]',
            'input[placeholder*="验证码"]'
        ],
        "text_selectors": [
            'div:has-text("请输入验证码")',
            'div:has-text("安全验证")',
            'div:has-text("请完成验证")'
        ],
        "verification_keywords": [
            "verification", "verify", "captcha", "验证", "安全检查"
        ]
    } 