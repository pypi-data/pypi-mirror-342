#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CSSCI筛选模块 (China Social Sciences Citation Index Filter)

这个模块负责在知网等学术搜索页面中查找并勾选CSSCI来源类别筛选选项。
CSSCI（中文社会科学引文索引）是一个重要的中文社科类期刊评价体系。

主要职责:
1. 在搜索结果页面中定位来源类别筛选区域
2. 查找并勾选CSSCI复选框
3. 应用筛选并等待结果加载
"""

import logging
import traceback
import asyncio
from typing import Dict, Any

# 获取logger
logger = logging.getLogger("cnks.cssci")

js_button_finder = """
() => {
    try {
        // 首先尝试找到带有"CSSCI"文本的链接
        let foundElement = null;
        
        // 尝试查找带有title="CSSCI"的链接
        const cssciLinks = document.querySelectorAll('a[title="CSSCI"]');
        if (cssciLinks.length > 0) {
            foundElement = cssciLinks[0];
            return {
                found: true,
                x: foundElement.getBoundingClientRect().left + foundElement.getBoundingClientRect().width/2,
                y: foundElement.getBoundingClientRect().top + foundElement.getBoundingClientRect().height/2,
                method: 'title_link',
                message: "找到带有title='CSSCI'的链接元素"
            };
        }
        
        // 尝试查找包含CSSCI文本的链接
        const allLinks = document.querySelectorAll('a');
        for (const link of allLinks) {
            if (link.textContent && link.textContent.trim() === 'CSSCI') {
                foundElement = link;
                return {
                    found: true,
                    x: foundElement.getBoundingClientRect().left + foundElement.getBoundingClientRect().width/2,
                    y: foundElement.getBoundingClientRect().top + foundElement.getBoundingClientRect().height/2,
                    method: 'text_link',
                    message: "找到文本为'CSSCI'的链接元素"
                };
            }
        }
        
        // 尝试查找包含CSSCI文本的任何元素
        const allElements = document.querySelectorAll('*');
        for (const element of allElements) {
            if (element.textContent && 
                element.textContent.includes('CSSCI') && 
                element.getBoundingClientRect().width > 0 &&
                element.getBoundingClientRect().height > 0) {
                foundElement = element;
                return {
                    found: true,
                    x: foundElement.getBoundingClientRect().left + foundElement.getBoundingClientRect().width/2,
                    y: foundElement.getBoundingClientRect().top + foundElement.getBoundingClientRect().height/2,
                    method: 'any_element',
                    message: "找到包含'CSSCI'的元素"
                };
            }
        }
        
        // 未找到任何相关元素
        return {
            found: false,
            message: "未找到任何包含'CSSCI'的可点击元素"
        };
    } catch (error) {
        // 发生错误，返回错误信息
        return {
            found: false,
            error: error.toString(),
            message: "查找CSSCI元素时发生错误: " + error.toString()
        };
    }
}
"""

async def apply_cssci_filter(page) -> Dict[str, Any]:
    """
    在搜索结果页面中应用CSSCI筛选
    
    Args:
        page: Playwright页面对象
        
    Returns:
        Dict: 包含操作结果的字典，包括是否成功、消息等
    """
    logger.info("开始应用CSSCI筛选")
    result = {
        "success": True,  # 默认为True，即使没找到也算成功（跳过继续处理）
        "message": "",
        "filter_applied": False
    }
    
    try:
        # 使用JavaScript查找CSSCI元素
        cssci_result = await page.evaluate(js_button_finder)
        logger.info(f"CSSCI元素查找结果: {cssci_result}")
        
        if cssci_result.get('found', False):
            logger.info(f"通过方法 '{cssci_result.get('method', 'unknown')}' 找到CSSCI元素，准备点击")
            
            # 使用鼠标点击坐标来模拟点击
            x, y = cssci_result.get('x'), cssci_result.get('y')
            await page.mouse.click(x, y)
            logger.info(f"已点击坐标 ({x}, {y}) 处的CSSCI元素")
            
            # 点击后等待短暂时间让页面响应，但不主动刷新
            await page.wait_for_timeout(1000)  # 等待1秒，让页面有时间响应
            
            result["filter_applied"] = True
            result["message"] = f"成功点击CSSCI元素（{cssci_result.get('method', 'unknown')}方法），由页面自行处理更新"
        else:
            # 如果没找到CSSCI元素，记录消息但仍然继续处理
            result["message"] = cssci_result.get('message', "未找到CSSCI元素，跳过筛选步骤")
            logger.info(result["message"])
        
        return result
        
    except Exception as e:
        logger.error(f"应用CSSCI筛选时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        
        result["message"] = f"应用CSSCI筛选时发生错误: {str(e)}"
        return result

async def _click_apply_button(page):
    """
    尝试点击筛选按钮以应用筛选
    
    Args:
        page: Playwright页面对象
    """
    # 等待一秒，确保页面状态已更新
    await asyncio.sleep(1)
    
    apply_buttons = [
        '.filter-button', 
        '.apply-filter', 
        'button[text="筛选"]',
        'button[text="应用"]',
        'button[text="确定"]',
        'input[type="button"][value="确定"]',
        '.btn-primary',
        '#btn_search'
    ]
    
    for btn_selector in apply_buttons:
        try:
            button = await page.query_selector(btn_selector)
            if button:
                logger.info(f"点击筛选应用按钮: {btn_selector}")
                await button.click()
                await page.wait_for_load_state("networkidle", timeout=10000)
                return True
        except Exception as e:
            logger.warning(f"点击按钮 '{btn_selector}' 失败: {str(e)}")
    
    # 如果没有找到标准按钮，尝试通过JavaScript应用筛选
    logger.info("尝试通过JavaScript应用筛选")
    apply_js = """
    () => {
        try {
            // 尝试找到并点击筛选应用按钮
            const buttons = document.querySelectorAll('button, input[type="button"], a.btn');
            for (const button of buttons) {
                if (button.textContent && 
                    (button.textContent.includes('筛选') || 
                     button.textContent.includes('应用') || 
                     button.textContent.includes('确定') ||
                     button.textContent.includes('搜索'))) {
                    button.click();
                    return { clicked: true, text: button.textContent.trim() };
                }
            }
            
            // 尝试查找搜索按钮
            const searchBtn = document.querySelector('#btn_search, .search-button, button[onclick*="search"]');
            if (searchBtn) {
                searchBtn.click();
                return { clicked: true, type: 'search' };
            }
            
            // 尝试提交表单
            const form = document.querySelector('form');
            if (form) {
                form.submit();
                return { clicked: true, type: 'form' };
            }
            
            return { clicked: false };
        } catch (e) {
            return { clicked: false, error: e.toString() };
        }
    }
    """
    
    apply_result = await page.evaluate(apply_js)
    if apply_result.get('clicked', False):
        logger.info(f"通过JavaScript应用筛选成功: {apply_result}")
        await page.wait_for_load_state("networkidle", timeout=10000)
        return True
    
    logger.warning("未找到应用筛选的按钮")
    return False


# 用于独立测试的函数
async def test_cssci_filter(page_url):
    """
    独立测试CSSCI筛选功能
    
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
            
            result = await apply_cssci_filter(page)
            print(f"测试结果: {result}")
            
            # 截图保存结果
            await page.screenshot(path="cssci_filter_test.png")
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
    
    print(f"测试在页面 {url} 上应用CSSCI筛选")
    asyncio.run(test_cssci_filter(url)) 