#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
关键词搜索模块（Searcher Module）

这是一个专门负责关键词搜索的模块，使用Playwright执行搜索并提取结果链接。
主要职责:
1. 接收关键词并执行搜索
2. 应用CSSCI筛选条件
3. 设置每页显示结果数
4. 提取搜索结果链接
5. 返回链接列表给工作者
"""

import os
import asyncio
import platform
import time
from typing import List, Dict, Any, Optional

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

# 导入必要的模块
try:
    from playwright.async_api import async_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# 尝试导入其他模块
try:
    from src.ifverify import check_verification_needed, handle_verification
    from src.click50 import set_results_per_page
    from src.extractlink import extract_links_from_page
except ImportError:
    try:
        from ifverify import check_verification_needed, handle_verification
        from click50 import set_results_per_page
        from extractlink import extract_links_from_page
    except ImportError:
        pass

# 默认搜索URL
SEARCH_URL = os.environ.get("SEARCH_URL", "https://kns.cnki.net/kns8s/search")

# CSSCI筛选的JavaScript函数
js_cssci_button_finder = """
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

class Searcher:
    """
    关键词搜索类，负责执行搜索并提取结果链接
    """
    
    def __init__(self):
        """初始化Searcher类"""
        self.playwright = None
        self.browser = None
        self.context = None
        self.browser_started = False
        
        # 不创建调试截图目录
        self.debug_dir = "/dev/null" if platform.system() != "Windows" else "NUL"
    
    async def start_browser(self) -> bool:
        """
        启动Playwright浏览器
        
        Returns:
            bool: 浏览器是否成功启动
        """
        if self.browser_started:
            return True
            
        if not PLAYWRIGHT_AVAILABLE:
            return False
            
        try:
            # 创建Playwright实例
            self.playwright = await async_playwright().start()
            
            # 创建用户数据目录（如果不存在）
            user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_data")
            os.makedirs(user_data_dir, exist_ok=True)
            
            # 设置Chrome参数
            browser_args = [
                '--start-maximized',
                '--disable-popup-blocking'
            ]
            
            # 查找Chrome可执行文件
            chrome_path = self._find_chrome_executable()
            
            # 使用持久上下文启动浏览器
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                executable_path=chrome_path if chrome_path else None,
                headless=False,
                args=browser_args
            )
            
            # 创建一个初始页面确保上下文已激活
            init_page = await self.context.new_page()
            await init_page.goto("about:blank")
            await init_page.close()
            
            # 标记浏览器已启动
            self.browser_started = True
            return True
            
        except Exception:
            # 清理资源
            await self.close_browser()
            return False
    
    async def close_browser(self) -> bool:
        """
        关闭Playwright浏览器和相关资源
        
        Returns:
            bool: 是否成功关闭
        """
        try:
            # 关闭浏览器上下文
            if self.context:
                await self.context.close()
                self.context = None
            
            # 停止Playwright
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            # 重置浏览器状态
            self.browser_started = False
            return True
            
        except Exception:
            self.browser_started = False
            return False
    
    def _find_chrome_executable(self) -> Optional[str]:
        """
        查找本地Chrome可执行文件路径
        
        Returns:
            Optional[str]: Chrome可执行文件路径，未找到则为None
        """
        system = platform.system()
        
        if system == "Windows":
            # Windows路径
            candidates = [
                os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
            ]
        elif system == "Darwin":  # macOS
            candidates = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            ]
        else:  # Linux
            candidates = [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser"
            ]
        
        # 检查每个候选路径
        for path in candidates:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path) and os.access(expanded_path, os.X_OK):
                return expanded_path
        
        return None
    
    async def open_page(self, url: str) -> Optional[Page]:
        """
        打开新标签页并导航到指定URL
        
        Args:
            url: 要导航到的URL
            
        Returns:
            Optional[Page]: Playwright页面对象，失败则为None
        """
        if not self.browser_started:
            success = await self.start_browser()
            if not success:
                return None
        
        try:
            # 创建新标签页
            page = await self.context.new_page()
            
            # 导航到指定URL
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # 检查是否需要验证
            verification_needed = await check_verification_needed(page)
            if verification_needed:
                await page.wait_for_timeout(10000)  # 等待10秒
            
            # 等待页面完全加载
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            return page
            
        except Exception:
            return None
    
    async def apply_cssci_filter(self, page) -> Dict[str, Any]:
        """
        在搜索结果页面中应用CSSCI筛选
        
        Args:
            page: Playwright页面对象
            
        Returns:
            Dict: 包含操作结果的字典，包括是否成功、消息等
        """
        result = {
            "success": True,  # 默认为True，即使没找到也算成功（跳过继续处理）
            "message": "",
            "filter_applied": False
        }
        
        try:
            # 首先检查页面上是否已经存在选中的CSSCI复选框
            cssci_checked = await page.evaluate("""
                () => {
                    const checkbox = document.querySelector('input[type="checkbox"][value="P0209"][title="CSSCI"][checked="checked"]');
                    return !!checkbox;
                }
            """)
            
            if cssci_checked:
                # 即使已选中也点击应用按钮确保筛选生效
                apply_result = await self.click_apply_button(page)
                result["filter_applied"] = True
                result["message"] = f"CSSCI选项已被选中，应用按钮点击结果: {apply_result}"
                return result
                
            # 查找CSSCI复选框
            cssci_checkbox = await page.query_selector('input[type="checkbox"][value="P0209"][title="CSSCI"]')
            
            if cssci_checkbox:
                # 使用模拟真实鼠标点击的方法点击CSSCI复选框
                
                # 获取元素的位置
                bbox = await cssci_checkbox.bounding_box()
                if bbox:
                    # 计算元素中心点
                    x = bbox["x"] + bbox["width"] / 2
                    y = bbox["y"] + bbox["height"] / 2
                    
                    # 移动鼠标到元素中心
                    await page.mouse.move(x, y)
                    # 按下鼠标按钮
                    await page.mouse.down()
                    # 等待50毫秒
                    await asyncio.sleep(0.05)
                    # 释放鼠标按钮
                    await page.mouse.up()
                else:
                    # 如果无法获取位置，回退到普通点击
                    await cssci_checkbox.click()
                
                # 等待一秒确保复选框状态更新
                await asyncio.sleep(1)
                
                # 点击应用按钮
                apply_result = await self.click_apply_button(page)
                
                # 等待页面刷新
                await page.wait_for_load_state("networkidle")
                
                result["filter_applied"] = True
                result["message"] = f"成功勾选CSSCI选项并点击应用按钮，结果: {apply_result}"
                return result
            
            # 如果通过精确选择器未找到，则尝试查找来源类别区域
            source_category = await page.query_selector('.source-category, .filter-item:has-text("来源类别")')
            
            if source_category:
                # 在来源类别区域内查找CSSCI选项
                cssci_checkbox = await source_category.query_selector('input[type="checkbox"]:near(:text("CSSCI"))')
                
                if cssci_checkbox:
                    # 使用模拟真实鼠标点击的方法点击CSSCI复选框
                    
                    # 获取元素的位置
                    bbox = await cssci_checkbox.bounding_box()
                    if bbox:
                        # 计算元素中心点
                        x = bbox["x"] + bbox["width"] / 2
                        y = bbox["y"] + bbox["height"] / 2
                        
                        # 移动鼠标到元素中心
                        await page.mouse.move(x, y)
                        # 按下鼠标按钮
                        await page.mouse.down()
                        # 等待50毫秒
                        await asyncio.sleep(0.05)
                        # 释放鼠标按钮
                        await page.mouse.up()
                    else:
                        # 如果无法获取位置，回退到普通点击
                        await cssci_checkbox.click()
                    
                    # 等待一秒确保复选框状态更新
                    await asyncio.sleep(1)
                    
                    # 点击应用按钮
                    apply_result = await self.click_apply_button(page)
                    
                    # 等待页面刷新
                    await page.wait_for_load_state("networkidle")
                    
                    result["filter_applied"] = True
                    result["message"] = f"成功勾选CSSCI选项并点击应用按钮，结果: {apply_result}"
                    return result
                else:
                    # 尝试另一种方式：直接在整个页面中查找CSSCI
                    cssci_text = await page.query_selector(':text("CSSCI")')
                    if cssci_text:
                        # 使用模拟真实鼠标点击的方法点击CSSCI文本
                        
                        # 获取元素的位置
                        bbox = await cssci_text.bounding_box()
                        if bbox:
                            # 计算元素中心点
                            x = bbox["x"] + bbox["width"] / 2
                            y = bbox["y"] + bbox["height"] / 2
                            
                            # 移动鼠标到元素中心
                            await page.mouse.move(x, y)
                            # 按下鼠标按钮
                            await page.mouse.down()
                            # 等待50毫秒
                            await asyncio.sleep(0.05)
                            # 释放鼠标按钮
                            await page.mouse.up()
                        else:
                            # 如果无法获取位置，回退到普通点击
                            await cssci_text.click()
                        
                        # 等待一秒确保复选框状态更新
                        await asyncio.sleep(1)
                        
                        # 点击应用按钮
                        apply_result = await self.click_apply_button(page)
                        
                        await page.wait_for_load_state("networkidle")
                        
                        result["filter_applied"] = True
                        result["message"] = f"通过文本找到并点击了CSSCI，应用按钮点击结果: {apply_result}"
                        return result
                    else:
                        result["message"] = "未找到CSSCI选项"
                        return result
            else:
                result["message"] = "未找到来源类别区域和CSSCI选项"
                return result
                
        except Exception as e:
            result["message"] = f"应用CSSCI筛选时发生错误: {str(e)}"
            return result
    
    async def click_apply_button(self, page):
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
                    # 获取按钮位置
                    bbox = await button.bounding_box()
                    if bbox:
                        # 计算按钮中心点
                        x = bbox["x"] + bbox["width"] / 2
                        y = bbox["y"] + bbox["height"] / 2
                        
                        # 移动鼠标到按钮中心
                        await page.mouse.move(x, y)
                        # 按下鼠标按钮
                        await page.mouse.down()
                        # 等待50毫秒
                        await asyncio.sleep(0.05)
                        # 释放鼠标按钮
                        await page.mouse.up()
                    else:
                        # 如果无法获取位置，回退到普通点击
                        await button.click()
                    
                    await page.wait_for_load_state("networkidle", timeout=10000)
                    return True
            except Exception:
                pass
        
        # 如果没有找到标准按钮，尝试通过JavaScript应用筛选
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
            await page.wait_for_load_state("networkidle", timeout=10000)
            return True
        
        return False
    
    async def search_keyword(self, keyword: str) -> List[str]:
        """
        搜索关键词并提取结果链接
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            List[str]: 搜索结果链接列表
        """
        if not PLAYWRIGHT_AVAILABLE:
            return []
        
        # 确保浏览器已启动
        if not self.browser_started:
            success = await self.start_browser()
            if not success:
                return []
        
        page = None
        try:
            # 使用open_page方法打开搜索页面
            page = await self.open_page(SEARCH_URL)
            if not page:
                return []
            
            # 输入搜索词
            search_input = await page.query_selector('#txt_search-input')
            
            if search_input:
                await search_input.fill(keyword)
                await search_input.press('Enter')
            else:
                # 尝试其他可能的搜索输入框选择器
                alternate_selectors = [
                    'input[type="search"]',
                    '.search-input',
                    '#search-input'
                ]
                for selector in alternate_selectors:
                    try:
                        input_field = await page.query_selector(selector)
                        if input_field:
                            await input_field.fill(keyword)
                            await input_field.press('Enter')
                            break
                    except Exception:
                        continue
            
            # 等待搜索结果
            await page.wait_for_load_state("networkidle", timeout=60000)
            
            # 尝试等待结果列表出现
            try:
                await page.wait_for_selector('.result-table-list', timeout=10000)
            except Exception:
                pass
            
            # 设置每页显示50条结果
            try:
                # 调用click50模块的设置方法
                page_setting_result = await set_results_per_page(page)
                if page_setting_result.get("success", False):
                    if page_setting_result.get("setting_applied", False):
                        # 等待页面重新加载结果
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        # 增加1000ms额外延时确保页面完全加载
                        await asyncio.sleep(1)
            except Exception:
                pass
            
            # 应用CSSCI筛选
            try:
                # 调用内部的CSSCI筛选方法
                await self.apply_cssci_filter(page)
            except Exception:
                pass
            
            # 强制等待几秒，确保页面加载完毕
            await asyncio.sleep(5)
            
            # 提取链接 - 使用独立的extractlink模块
            links = await extract_links_from_page(page)
            
            return links
            
        except Exception:
            return []
            
        finally:
            # 关闭标签页但保持浏览器打开
            if page:
                await page.close() 