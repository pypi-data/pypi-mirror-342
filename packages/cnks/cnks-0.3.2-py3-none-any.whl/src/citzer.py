#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
引文分析器模块（Citzer Module）

这是一个专门负责处理链接页面和提取引文信息的模块。
使用Playwright技术访问链接并提取标题、作者和摘要等结构化信息。

主要职责:
1. 启动和管理浏览器实例
2. 访问文献链接并提取引文数据
3. 处理验证页面和特殊情况
4. 返回结构化引文数据
"""
import os
import platform
import traceback
import time
import re
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

# 导入必要的模块
try:
    from playwright.async_api import async_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# 尝试导入其他模块
try:
    from src.ifverify import check_verification_needed, handle_verification
except ImportError:
    try:
        from ifverify import check_verification_needed, handle_verification
    except ImportError:
        pass

class Citzer:
    """引文分析器类，负责浏览器管理和引文内容提取"""
    
    def __init__(self):
        """初始化Citzer类"""
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
            
        except Exception as e:
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
        # 检查是否有可用的上下文（可能是共享的）
        if self.context is None and not self.browser_started:
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
    
    async def process_link(self, link: str) -> Dict[str, Any]:
        """
        处理单个链接并提取引用信息
        
        Args:
            link: 要处理的链接URL
            
        Returns:
            Dict[str, Any]: 包含提取的引用信息的字典
        """
        page = None
        try:
            # 检查是否已经有浏览器上下文(可能是共享的)
            if self.context is None and not self.browser_started:
                await self.start_browser()
            
            # 打开链接
            page = await self.open_page(link)
            if not page:
                return {}
            
            # 不进行截图操作
            
            # 提取摘要
            abstract = await self._extract_abstract(page)
            
            # 提取引用信息
            citation = await self.extract_citation_from_button(page)
            
            # 如果提取失败，尝试从页面标题获取基本信息
            if not citation:
                title = await page.title()
                citation = {
                    "title": title,
                    "raw_extracted": True
                }
            
            # 组合结果
            result = {
                "title": citation.get("title", ""),
                "cite_format": citation.get("cite_format", ""),
                "abstract": abstract,
                "url": link
            }
            
            # 如果标题为空但有引用格式，尝试从引用格式中提取标题
            if not result["title"] and result["cite_format"]:
                result["title"] = self.extract_title_from_cite(result["cite_format"])
            
            return result
            
        except Exception:
            return {}
            
        finally:
            if page:
                await page.close()
    
    async def extract_from_html(self, page):
        """从HTML页面提取引用信息"""
        try:
            # 等待页面加载完成
            await page.wait_for_load_state("networkidle")
            
            # 先尝试直接提取摘要
            abstract = await self._extract_abstract(page)
            
            # 获取引用格式按钮
            citation_data = await self.extract_citation_from_button(page)
            
            if citation_data:
                result = {
                    'title': citation_data.get('title', ''),
                    'cite_format': citation_data.get('cite_format', ''),
                    'abstract': abstract
                }
                
                # 生成引用文本
                if result.get('title') and not result.get('cite_format'):
                    result['cite_format'] = f"{result['title']}"
                
                return result
            else:
                return None
            
        except Exception:
            return None
    
    @staticmethod
    def process_citation(citation_data: Dict) -> Dict:
        """Process citation data and format it into a standard structure."""
        try:
            # Create result dictionary
            result = {
                "title": citation_data.get("title", ""),
                "abstract": citation_data.get("abstract", ""),
                "cite_format": ""
            }
            
            # Process citation format
            cite_format = citation_data.get("cite_format", "")
            if cite_format:
                # Clean citation format
                cite_format = cite_format.strip()
                result["cite_format"] = cite_format
                
                # Try to extract title (if original title is empty)
                if not result["title"] and cite_format:
                    title_match = re.search(r'[\.。]\s*([^\.。]+)[\.。]', cite_format)
                    if title_match:
                        result["title"] = title_match.group(1).strip()
            
            # Process abstract
            abstract = citation_data.get("abstract", "")
            if abstract:
                # Clean abstract
                abstract = re.sub(r'\s+', ' ', abstract).strip()
                result["abstract"] = abstract
            
            return result
            
        except Exception:
            # Return raw data
            return {
                "title": citation_data.get("title", ""),
                "abstract": citation_data.get("abstract", ""),
                "cite_format": citation_data.get("cite_format", "")
            }
    
    @staticmethod
    def extract_title_from_cite(cite_format: str) -> str:
        """Extract title from citation format."""
        if not cite_format:
            return ""
        
        try:
            # Try to match title (usually between first and second period)
            match = re.search(r'[\.。]\s*([^\.。]+)[\.。]', cite_format)
            if match:
                return match.group(1).strip()
        except Exception:
            pass
        
        return ""
    
    @staticmethod
    def extract_authors_from_cite(cite_format: str) -> List[str]:
        """Extract authors from citation format."""
        if not cite_format:
            return []
        
        try:
            # Try to match authors (usually at the start of citation format until first period)
            match = re.match(r'^([^\.。]+)[\.。]', cite_format)
            if match:
                authors_str = match.group(1)
                return [a.strip() for a in re.split(r'[,，、]', authors_str) if a.strip()]
        except Exception:
            pass
        
        return []
    
    @staticmethod
    def validate_citation(citation_data: Dict) -> bool:
        """Validate if citation data is valid."""
        # At least title or citation format is required
        return bool(citation_data.get("title") or citation_data.get("cite_format"))
    
    async def extract_citation_from_button(self, page) -> Dict:
        """
        尝试点击页面中的引用按钮并提取引用信息
        
        Args:
            page: Playwright页面对象
            
        Returns:
            Dict: 包含从引用按钮中提取的信息，如果无法提取则返回空字典
        """
        try:
            # 首先尝试直接从页面提取摘要
            citation_data = {}
            
            # 在点击引用按钮之前先尝试直接提取摘要信息
            try:
                # 提取摘要
                abstract_js = """
                    () => {
                        // 尝试多种可能的选择器查找摘要
                        const abstractSelectors = [
                            '.abstract-text', '.abstract', '#abstract',
                            '.summary', '.summary-text', '#summary',
                            '.row-abstract span', '.row-abstract div',
                            '[role="abstract"]', '[data-role="abstract"]',
                            '.abstract-box', '.abstract-content',
                            '.article-abstract', '.article-summary'
                        ];
                        
                        for (const selector of abstractSelectors) {
                            const element = document.querySelector(selector);
                            if (element && element.textContent) {
                                return element.textContent.trim();
                            }
                        }
                        
                        // 寻找包含"摘要"文本的元素
                        const elements = Array.from(document.querySelectorAll('*'));
                        for (const element of elements) {
                            if (element.textContent && 
                                (element.textContent.includes('摘要') || 
                                 element.textContent.includes('Abstract') ||
                                 element.textContent.includes('内容提要'))) {
                                // 检查父元素
                                const parent = element.parentElement;
                                if (parent && parent.textContent.length > 30) {
                                    const text = parent.textContent.replace(/摘要[：:]/g, '').trim();
                                    if (text.length > 30) {
                                        return text;
                                    }
                                }
                                
                                // 检查下一个兄弟元素
                                let nextElement = element.nextElementSibling;
                                if (nextElement && nextElement.textContent.length > 30) {
                                    return nextElement.textContent.trim();
                                }
                                
                                // 检查包含元素中的段落
                                const container = element.closest('div, section, article');
                                if (container) {
                                    const paragraphs = container.querySelectorAll('p');
                                    for (const p of paragraphs) {
                                        if (p.textContent && p.textContent.length > 50 && !p.textContent.includes('摘要')) {
                                            return p.textContent.trim();
                                        }
                                    }
                                }
                            }
                        }
                        
                        return "";
                    }
                """
                abstract = await page.evaluate(abstract_js)
                if abstract:
                    citation_data["abstract"] = abstract
            except Exception:
                pass
            
            # 不创建调试截图
            
            # 使用JavaScript定位并点击引用按钮
            js_button_finder = """
            () => {
                // 根据已知的HTML结构首先尝试精确定位
                // 尝试先查找 li.btn-quote
                let btn = document.querySelector('li.btn-quote a, li[class*="btn-quote"] a');
                if (btn) {
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        return {
                            found: true,
                            x: rect.left + rect.width/2,
                            y: rect.top + rect.height/2,
                            text: (btn.textContent || '').trim(),
                            tag: btn.tagName,
                            method: 'direct_class'
                        };
                    }
                }
                
                // 尝试查找包含getQuotes()的onclick属性
                btn = document.querySelector('a[onclick*="getQuotes()"]');
                if (btn) {
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        return {
                            found: true,
                            x: rect.left + rect.width/2,
                            y: rect.top + rect.height/2,
                            text: (btn.textContent || '').trim(),
                            tag: btn.tagName,
                            method: 'onclick_getQuotes'
                        };
                    }
                }
                
                // 尝试查找title="引用"的li下的a标签
                btn = document.querySelector('li[title="引用"] a');
                if (btn) {
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        return {
                            found: true,
                            x: rect.left + rect.width/2,
                            y: rect.top + rect.height/2,
                            text: (btn.textContent || '').trim(),
                            tag: btn.tagName,
                            method: 'title_citation'
                        };
                    }
                }
                
                // 尝试在更广泛的范围内查找
                // 查找btns-tool下的other-btns内的引用按钮
                const otherBtns = document.querySelectorAll('.btns-tool .other-btns li a, .btn-tool .other-btn li a');
                for (const btn of otherBtns) {
                    const parent = btn.closest('li');
                    if (parent && (parent.title === '引用' || 
                                  parent.classList.contains('btn-quote') || 
                                  (parent.textContent && parent.textContent.includes('引用')))) {
                        const rect = btn.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {
                            return {
                                found: true,
                                x: rect.left + rect.width/2,
                                y: rect.top + rect.height/2,
                                text: (btn.textContent || '').trim(),
                                tag: btn.tagName,
                                method: 'other_btns'
                            };
                        }
                    }
                }
                
                // 图片中的结构示例: div.btn-tool > ul.other-btn > li.btn-quote[title="引用"] > a
                // 尝试通过这个明确的路径查找
                btn = document.querySelector('div.btn-tool ul.other-btn li.btn-quote[title="引用"] a');
                if (btn) {
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        return {
                            found: true,
                            x: rect.left + rect.width/2,
                            y: rect.top + rect.height/2,
                            text: (btn.textContent || '').trim(),
                            tag: btn.tagName,
                            method: 'exact_path_match'
                        };
                    }
                }
                
                // 如果还没找到，尝试一次遍历所有a标签
                const allLinks = document.querySelectorAll('a');
                for (const link of allLinks) {
                    const onclick = link.getAttribute('onclick') || '';
                    const text = link.textContent || '';
                    const parent = link.parentElement;
                    const parentTitle = parent ? parent.getAttribute('title') || '' : '';
                    
                    if (onclick.includes('getQuotes') || 
                        onclick.includes('quote') ||
                        text.includes('引用') || 
                        parentTitle.includes('引用')) {
                        const rect = link.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {
                            return {
                                found: true,
                                x: rect.left + rect.width/2,
                                y: rect.top + rect.height/2,
                                text: text.trim(),
                                tag: link.tagName,
                                method: 'general_search'
                            };
                        }
                    }
                }
                
                return { found: false };
            }
            """
            
            button_info = await page.evaluate(js_button_finder)
            if button_info and button_info.get('found'):
                # 使用鼠标点击坐标
                x, y = button_info.get('x'), button_info.get('y') 
                await page.mouse.click(x, y)
                
                # 等待引用对话框出现
                await page.wait_for_timeout(2000)
                
                # 不获取点击后截图
                
                # 提取引用信息
                cite_result = await self._extract_citation_text(page)
                if cite_result:
                    cite_result.update(citation_data)
                    return cite_result
            
            # 如果点击按钮都失败了，但我们已经提取到了其他信息
            if citation_data:
                return citation_data
            
        except Exception:
            pass
        
        return {}
        
    async def _extract_citation_text(self, page) -> Dict:
        """提取引用文本内容"""
        try:
            # 使用页面评估提取引用信息
            cite_result = await page.evaluate('''
                () => {
                    // 尝试多种可能的选择器查找引用文本区域
                    const textareaSelectors = [
                        '.quote-r textarea.text',
                        'textarea.reference-text',
                        '.reference-container textarea',
                        'div.quote-content textarea',
                        '.cite-form textarea',
                        '.citation textarea',
                        'textarea[id*="citation"]',
                        'textarea[id*="reference"]',
                        'textarea[class*="citation"]',
                        'textarea[class*="reference"]',
                        // 添加更多可能的选择器
                        '.citation-text', 
                        '#citation-text',
                        'textarea',  // 如果只有一个textarea，可能就是引用文本
                        '.modal textarea', // 如果在模态框中
                        '.panel textarea',  // 如果在面板中
                        'div[id*="quote"] textarea', 
                        'div[id*="citation"] textarea',
                        'div[id*="cite"] textarea',
                        'div[class*="quote"] textarea', 
                        'div[class*="citation"] textarea',
                        'div[class*="cite"] textarea'
                    ];
                    
                    let textarea = null;
                    for (const selector of textareaSelectors) {
                        const elements = document.querySelectorAll(selector);
                        if (elements.length > 0) {
                            // 如果有多个匹配，找出第一个非空的textarea
                            for (const element of elements) {
                                if (element.textContent) {
                                    textarea = element;
                                    break;
                                }
                            }
                        }
                    }
                    
                    if (textarea) {
                        return textarea.textContent.trim();
                        } else {
                        return "";
                    }
                }
            ''')
            
            if cite_result:
                return {
                    "title": "",
                    "cite_format": cite_result,
                    "abstract": ""
                }
            else:
                return {}
            
        except Exception:
            return {}
    
    async def _extract_abstract(self, page) -> str:
        """
        从页面提取文章摘要
        
        Args:
            page: Playwright页面对象
            
        Returns:
            str: 提取到的摘要文本，如果未找到则返回空字符串
        """
        try:
            # 使用JavaScript提取摘要
            abstract_js = """
                () => {
                    // 尝试多种可能的选择器查找摘要
                    const abstractSelectors = [
                        '.abstract-text', '.abstract', '#abstract',
                        '.summary', '.summary-text', '#summary',
                        '.row-abstract span', '.row-abstract div',
                        '[role="abstract"]', '[data-role="abstract"]',
                        '.abstract-box', '.abstract-content',
                        '.article-abstract', '.article-summary'
                    ];
                    
                    for (const selector of abstractSelectors) {
                        const element = document.querySelector(selector);
                        if (element && element.textContent) {
                            return element.textContent.trim();
                        }
                    }
                    
                    // 寻找包含"摘要"文本的元素
                    const elements = Array.from(document.querySelectorAll('*'));
                    for (const element of elements) {
                        if (element.textContent && 
                            (element.textContent.includes('摘要') || 
                             element.textContent.includes('Abstract') ||
                             element.textContent.includes('内容提要'))) {
                            // 检查父元素
                            const parent = element.parentElement;
                            if (parent && parent.textContent.length > 30) {
                                const text = parent.textContent.replace(/摘要[：:]/g, '').trim();
                                if (text.length > 30) {
                                    return text;
                                }
                            }
                            
                            // 检查下一个兄弟元素
                            let nextElement = element.nextElementSibling;
                            if (nextElement && nextElement.textContent.length > 30) {
                                return nextElement.textContent.trim();
                            }
                            
                            // 检查包含元素中的段落
                            const container = element.closest('div, section, article');
                            if (container) {
                                const paragraphs = container.querySelectorAll('p');
                                for (const p of paragraphs) {
                                    if (p.textContent && p.textContent.length > 50 && !p.textContent.includes('摘要')) {
                                        return p.textContent.trim();
                                    }
                                }
                            }
                        }
                    }
                    
                    return "";
                }
            """
            
            abstract = await page.evaluate(abstract_js)
            if abstract:
                # 清理摘要文本
                abstract = abstract.replace("摘要:", "").replace("摘要：", "").replace("Abstract:", "").strip()
                return abstract
            else:
                return ""
                
        except Exception:
            return "" 
  