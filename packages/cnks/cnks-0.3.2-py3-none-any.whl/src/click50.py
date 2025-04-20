#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
结果显示条数设置模块 (Page Results Display Count Selector)

这个模块负责设置知网搜索结果页面中每页显示的条目数量。
在搜索结果加载后，通过模拟用户点击设置每页显示50条结果。

主要职责:
1. 定位页面中的显示数量控制区域
2. 点击下拉菜单
3. 选择"50"条每页选项
"""

import logging
import traceback
import asyncio
from typing import Dict, Any

# 获取logger
logger = logging.getLogger("cnks.click50")

async def set_results_per_page(page, attempts=5) -> Dict[str, Any]:
    """
    在搜索结果页面中设置每页显示50条结果
    
    Args:
        page: Playwright页面对象
        attempts: 尝试次数，默认5次
        
    Returns:
        Dict: 包含操作结果的字典，包括是否成功、消息等
    """
    logger.info("开始设置每页显示50条结果")
    result = {
        "success": False,
        "message": "",
        "setting_applied": False
    }
    
    # 循环尝试，最多尝试指定次数
    for attempt in range(attempts):
        try:
            logger.info(f"第{attempt+1}次尝试设置每页显示50条结果")
            
            # 1. 使用JavaScript查找并识别下拉菜单元素
            dropdown_js = """
            () => {
                // 尝试多种可能的选择器来查找显示数量控制区域
                const dropdownSelectors = [
                    // 直接通过显示文本相关选择器
                    '#id_grid_display_num',
                    '.page-show-count',
                    'div[id*="display_num"]',
                    'div[id*="pageSize"]',
                    'div[class*="page-show"]',
                    'div[class*="perPage"]',
                    'div[class*="sort"]', // 通常在排序区域附近
                    
                    // 更通用的下拉菜单选择器
                    'div.dropdown', 
                    'select.form-control',
                    '.dropdown-toggle'
                ];
                
                // 通过文本内容查找
                const textBasedSelectors = [
                    'span:has-text("显示:")',
                    'div:has-text("每页显示")'
                ];
                
                // 尝试找到下拉菜单元素
                for (const selector of [...dropdownSelectors, ...textBasedSelectors]) {
                    const element = document.querySelector(selector);
                    if (element) {
                        // 检查是否含有数字，如显示后面的数字
                        if (element.textContent && /\\d+/.test(element.textContent)) {
                            return {
                                found: true,
                                selector: selector,
                                id: element.id || "",
                                text: element.textContent.trim(),
                                tagName: element.tagName.toLowerCase(),
                                hasDropdown: !!element.querySelector('.dropdown-menu, select, option')
                            };
                        }
                    }
                }
                
                // 查找可能包含"显示:"文本的任何元素
                const anyDisplayElements = document.evaluate(
                    '//*[contains(text(), "显示:") or contains(text(), "每页") or contains(text(), "条目")]', 
                    document, 
                    null, 
                    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, 
                    null
                );
                
                for (let i = 0; i < anyDisplayElements.snapshotLength; i++) {
                    const element = anyDisplayElements.snapshotItem(i);
                    return {
                        found: true,
                        xpath: true,
                        text: element.textContent.trim(),
                        tagName: element.tagName.toLowerCase()
                    };
                }
                
                // 尝试查找包含具体数字选项的元素
                const options50 = document.querySelectorAll('li[data-val="50"], option[value="50"], a:has-text("50")');
                if (options50.length > 0) {
                    return {
                        found: true,
                        option50Found: true,
                        count: options50.length
                    };
                }
                
                return { found: false };
            }
            """
            
            display_info = await page.evaluate(dropdown_js)
            logger.info(f"显示控制区域信息: {display_info}")
            
            if not display_info.get('found', False):
                logger.warning("未找到显示控制区域，尝试使用备用方法")
                
                # 2. 找到特定的data-val="50"的元素进行直接点击
                direct_click_js = """
                () => {
                    // 直接查找并点击data-val为50的元素
                    const item50 = document.querySelector('li[data-val="50"], a[onclick*="50"]');
                    if (item50) {
                        const rect = item50.getBoundingClientRect();
                        return {
                            found: true,
                            x: rect.left + rect.width/2,
                            y: rect.top + rect.height/2,
                            text: item50.textContent.trim(),
                            tagName: item50.tagName.toLowerCase()
                        };
                    }
                    return { found: false };
                }
                """
                
                item50_info = await page.evaluate(direct_click_js)
                if item50_info.get('found', False):
                    logger.info(f"找到50选项元素: {item50_info}")
                    await page.mouse.click(item50_info['x'], item50_info['y'])
                    logger.info("已直接点击50选项元素")
                    
                    # 等待页面更新
                    await page.wait_for_load_state("networkidle", timeout=10000)
                    result["success"] = True
                    result["setting_applied"] = True
                    result["message"] = "成功直接点击50选项"
                    return result
            
            # 3. 如果找到显示控制区域，先点击它打开下拉菜单
            # 查找与"显示:"相关的下拉框元素
            show_dropdown_js = """
            () => {
                // 查找下拉菜单触发元素
                const dropdownTriggers = [
                    // ID选择器
                    '#id_grid_display_num',
                    '#pageSize',
                    
                    // 带有显示字样的span或div
                    'span:has-text("显示")',
                    'div.page-show-count',
                    'div[class*="sort"]',
                    
                    // 通过父子关系查找
                    '.toolbar-opt span',
                    '.sort-default',
                    '.dropdown-toggle'
                ];
                
                // 尝试查找下拉触发器
                for (const selector of dropdownTriggers) {
                    const element = document.querySelector(selector);
                    if (element) {
                        const rect = element.getBoundingClientRect();
                        return {
                            found: true,
                            selector: selector,
                            x: rect.left + rect.width/2,
                            y: rect.top + rect.height/2,
                            text: element.textContent.trim(),
                            tagName: element.tagName.toLowerCase()
                        };
                    }
                }
                
                // 使用XPath查找更复杂的模式
                const displayElements = document.evaluate(
                    '//*[contains(text(), "显示")]/ancestor::*[contains(@class, "dropdown") or contains(@class, "sort")]', 
                    document, 
                    null, 
                    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, 
                    null
                );
                
                if (displayElements.snapshotLength > 0) {
                    const element = displayElements.snapshotItem(0);
                    const rect = element.getBoundingClientRect();
                    return {
                        found: true,
                        x: rect.left + rect.width/2,
                        y: rect.top + rect.height/2,
                        text: element.textContent.trim(),
                        xpath: true
                    };
                }
                
                return { found: false };
            }
            """
            
            dropdown_info = await page.evaluate(show_dropdown_js)
            logger.info(f"下拉菜单触发元素信息: {dropdown_info}")
            
            if dropdown_info.get('found', False):
                # 点击下拉菜单触发元素
                logger.info(f"点击下拉菜单触发元素: {dropdown_info.get('text', '')}")
                await page.mouse.click(dropdown_info['x'], dropdown_info['y'])
                
                # 等待下拉菜单展开
                await asyncio.sleep(1)
                
                # 4. 查找并点击"50"选项
                option50_js = """
                () => {
                    // 查找值为50的选项
                    const options = [
                        'li[data-val="50"]',
                        'option[value="50"]',
                        'a:has-text("50")',
                        '.dropdown-menu li:has-text("50")', 
                        'ul[class*="sort-list"] li:nth-child(3)',
                        '.dropdown-item:has-text("50")'
                    ];
                    
                    for (const selector of options) {
                        const option = document.querySelector(selector);
                        if (option) {
                            const rect = option.getBoundingClientRect();
                            return {
                                found: true,
                                selector: selector,
                                x: rect.left + rect.width/2,
                                y: rect.top + rect.height/2,
                                text: option.textContent.trim(),
                                tagName: option.tagName.toLowerCase()
                            };
                        }
                    }
                    
                    // 使用XPath查找包含50的选项
                    const option50Elements = document.evaluate(
                        '//li[text()="50" or contains(text(), "50条")]', 
                        document, 
                        null, 
                        XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, 
                        null
                    );
                    
                    if (option50Elements.snapshotLength > 0) {
                        const option = option50Elements.snapshotItem(0);
                        const rect = option.getBoundingClientRect();
                        return {
                            found: true,
                            x: rect.left + rect.width/2,
                            y: rect.top + rect.height/2,
                            text: option.textContent.trim(),
                            xpath: true
                        };
                    }
                    
                    return { found: false };
                }
                """
                
                option50_info = await page.evaluate(option50_js)
                logger.info(f"50选项信息: {option50_info}")
                
                if option50_info.get('found', False):
                    # 点击50选项
                    logger.info(f"点击50选项: {option50_info.get('text', '')}")
                    await page.mouse.click(option50_info['x'], option50_info['y'])
                    
                    # 等待页面更新
                    await page.wait_for_load_state("networkidle", timeout=10000)
                    
                    result["success"] = True
                    result["setting_applied"] = True
                    result["message"] = "成功设置每页显示50条结果"
                    return result
                else:
                    logger.warning("未找到50选项")
            else:
                logger.warning("未找到下拉菜单触发元素")
            
            # 如果找不到标准元素，尝试使用更通用的方法
            # 5. 尝试基于图片中看到的HTML结构进行精确定位
            specific_structure_js = """
            () => {
                try {
                    // 从您图片中看到的HTML结构精确定位
                    const dropdown = document.querySelector('div[id="id_grid_display_num"]');
                    if (dropdown) {
                        const dropdownRect = dropdown.getBoundingClientRect();
                        const dropdownInfo = {
                            found: true,
                            dropdown: {
                                x: dropdownRect.left + dropdownRect.width/2,
                                y: dropdownRect.top + dropdownRect.height/2,
                                text: dropdown.textContent.trim() 
                            }
                        };
                        
                        // 尝试找到data-val="50"的li元素
                        const option50 = document.querySelector('li[data-val="50"]');
                        if (option50) {
                            const optionRect = option50.getBoundingClientRect();
                            dropdownInfo.option50 = {
                                found: true,
                                x: optionRect.left + optionRect.width/2,
                                y: optionRect.top + optionRect.height/2,
                                text: option50.textContent.trim()
                            };
                        }
                        
                        return dropdownInfo;
                    }
                    
                    // 尝试找到包含"javascript:void(0)"和"50"的a元素
                    const javascriptLink = document.querySelector('a[href*="javascript:void(0)"][data-val="50"]');
                    if (javascriptLink) {
                        const rect = javascriptLink.getBoundingClientRect();
                        return {
                            found: true,
                            jsLink: {
                                x: rect.left + rect.width/2,
                                y: rect.top + rect.height/2,
                                text: javascriptLink.textContent.trim()
                            }
                        };
                    }
                } catch (e) {
                    return { found: false, error: e.toString() };
                }
                
                return { found: false };
            }
            """
            
            specific_info = await page.evaluate(specific_structure_js)
            logger.info(f"特定结构信息: {specific_info}")
            
            if specific_info.get('found', False):
                # 如果找到了下拉菜单
                if 'dropdown' in specific_info:
                    logger.info(f"点击特定下拉菜单: {specific_info['dropdown'].get('text', '')}")
                    await page.mouse.click(
                        specific_info['dropdown']['x'], 
                        specific_info['dropdown']['y']
                    )
                    
                    # 等待下拉菜单展开
                    await asyncio.sleep(1)
                    
                    # 如果找到了50选项
                    if 'option50' in specific_info and specific_info['option50'].get('found', False):
                        logger.info(f"点击特定50选项: {specific_info['option50'].get('text', '')}")
                        await page.mouse.click(
                            specific_info['option50']['x'], 
                            specific_info['option50']['y']
                        )
                        
                        # 等待页面更新
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        
                        result["success"] = True
                        result["setting_applied"] = True
                        result["message"] = "通过特定结构成功设置每页显示50条结果"
                        return result
                
                # 如果找到了javascript链接
                if 'jsLink' in specific_info:
                    logger.info(f"点击JavaScript链接: {specific_info['jsLink'].get('text', '')}")
                    await page.mouse.click(
                        specific_info['jsLink']['x'], 
                        specific_info['jsLink']['y']
                    )
                    
                    # 等待页面更新
                    await page.wait_for_load_state("networkidle", timeout=10000)
                    
                    result["success"] = True
                    result["setting_applied"] = True
                    result["message"] = "通过JavaScript链接成功设置每页显示50条结果"
                    return result
            
            # 6. 最后尝试直接执行JavaScript修改页面
            logger.info("尝试使用JavaScript直接修改每页显示数量")
            direct_js = """
            () => {
                try {
                    // 尝试各种可能的方式修改页面显示设置
                    
                    // 方法1: 尝试触发点击事件
                    const option50 = document.querySelector('li[data-val="50"], a[data-val="50"]');
                    if (option50) {
                        option50.click();
                        return { success: true, method: "click" };
                    }
                    
                    // 方法2: 尝试执行可能的JavaScript函数
                    if (typeof changePageSize === 'function') {
                        changePageSize(50);
                        return { success: true, method: "changePageSize" };
                    }
                    
                    if (typeof setPageSize === 'function') {
                        setPageSize(50);
                        return { success: true, method: "setPageSize" };
                    }
                    
                    if (typeof setDisplayCount === 'function') {
                        setDisplayCount(50);
                        return { success: true, method: "setDisplayCount" };
                    }
                    
                    // 方法3: 尝试触发有特定值的元素的点击事件
                    const clickables = document.querySelectorAll('[onclick*="50"]');
                    if (clickables.length > 0) {
                        clickables[0].click();
                        return { success: true, method: "onclick", element: clickables[0].tagName };
                    }
                    
                    return { success: false };
                } catch (e) {
                    return { success: false, error: e.toString() };
                }
            }
            """
            
            direct_result = await page.evaluate(direct_js)
            logger.info(f"直接JavaScript执行结果: {direct_result}")
            
            if direct_result.get('success', False):
                # 等待页面更新
                await page.wait_for_load_state("networkidle", timeout=10000)
                
                result["success"] = True
                result["setting_applied"] = True
                result["message"] = f"使用JavaScript方法'{direct_result.get('method')}'成功设置每页显示条数"
                return result
            
            # 如果当前尝试失败，等待一秒再试
            logger.warning(f"第{attempt+1}次尝试失败，等待后重试")
            await asyncio.sleep(1)
            
        except Exception as e:
            error_msg = f"设置每页显示条数时出错: {str(e)}"
            logger.warning(error_msg)
            logger.warning(traceback.format_exc())
            
            # 如果发生错误，等待一秒再试
            await asyncio.sleep(1)
    
    # 如果所有尝试都失败
    result["success"] = False
    result["message"] = "多次尝试后未能设置每页显示50条结果"
    return result

# 用于独立测试的函数
async def test_set_results_per_page(page_url):
    """
    独立测试设置每页显示条数功能
    
    Args:
        page_url: 要测试的页面URL
    """
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            await page.goto(page_url, wait_until="domcontentloaded")
            await page.wait_for_load_state("networkidle")
            
            result = await set_results_per_page(page)
            print(f"测试结果: {result}")
            
            # 截图保存结果
            await page.screenshot(path="results_per_page_test.png")
            print("已保存测试结果截图")
            
            # 等待查看结果
            await asyncio.sleep(5)
            
        finally:
            await browser.close()

# 如果直接运行脚本
if __name__ == "__main__":
    import sys
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # 获取命令行参数或使用默认URL
    url = sys.argv[1] if len(sys.argv) > 1 else "https://kns.cnki.net/kns8s/search"
    
    print(f"测试在页面 {url} 上设置每页显示50条结果")
    asyncio.run(test_set_results_per_page(url)) 