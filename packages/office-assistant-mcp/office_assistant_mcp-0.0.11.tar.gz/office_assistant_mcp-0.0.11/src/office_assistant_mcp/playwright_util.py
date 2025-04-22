import os
import tempfile
# os.environ['PWDEBUG'] = '1'  # 运行程序马上就进入Playwright调试模式
from playwright.async_api import async_playwright, Locator, Frame, Page, expect
import re
import asyncio
from office_assistant_mcp.log_util import log_debug, log_info, log_error
import importlib.metadata
from dotenv import load_dotenv
import httpx
    
load_dotenv()

# 浏览器路径
# CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# 浏览器用户数据目录，指定目录，避免重复登录
# CHROME_USER_DATA_DIR = "/Users/kamous/Library/Application Support/Google/Chrome/playwright1"
CHROME_PATH = None
CHROME_USER_DATA_DIR = None

# 全局变量用于缓存playwright实例
_playwright_instance = None
_browser_instance = None
_page_instance = None

def reset_playwright_cache():
    """重置playwright缓存，以便创建新的浏览器和页面实例"""
    log_info("reset playwright cache")
    global _playwright_instance, _browser_instance, _page_instance
    _playwright_instance = None
    _browser_instance = None
    _page_instance = None


async def create_playwright():
    global CHROME_USER_DATA_DIR
    # 如果CHROME_USER_DATA_DIR为空，则在临时目录下创建一个固定的用户数据目录，以避免需用重复登录验证
    if CHROME_USER_DATA_DIR is None:
        temp_dir = os.path.join(tempfile.gettempdir(), "office_assistant_mcp_chrome_user_data")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        CHROME_USER_DATA_DIR = temp_dir
        log_info(f"使用Chrome临时用户数据目录: {CHROME_USER_DATA_DIR}")
        
    await remove_lock_files()
    p = await async_playwright().start()
    
    # 浏览器启动参数
    launch_options = {
        'user_data_dir': CHROME_USER_DATA_DIR,
        'headless': False,  # 显示浏览器界面
        'args': ['--start-maximized']  # 浏览器全屏启动
    }
    
    # 如果CHROME_PATH不为空，则使用指定的浏览器路径
    if CHROME_PATH:
        launch_options['executable_path'] = CHROME_PATH
    
    browser = await p.chromium.launch_persistent_context(**launch_options)
    return p, browser

def get_current_version():
    """获取当前版本号"""
    return importlib.metadata.version("office_assistant_mcp")

async def get_playwright():
    """获取playwright对象,如果没有则新建，有则返回全局缓存的对象"""
    global _playwright_instance, _browser_instance, _page_instance

    if _playwright_instance is None or _browser_instance is None:
        log_debug(f"获取playwright，创建新实例")
        _playwright_instance, _browser_instance = await create_playwright()
        _page_instance = await _browser_instance.new_page()
        _page_instance.set_default_timeout(5000)
    else:
        log_debug(f"获取playwright，使用缓存")
    return _playwright_instance, _browser_instance, _page_instance


async def close_playwright():
    """关闭并清除缓存的playwright和browser实例"""
    log_debug(f"close playwright")
    global _playwright_instance, _browser_instance, _page_instance

    if _browser_instance:
        await _browser_instance.close()
        _browser_instance = None

    if _playwright_instance:
        await _playwright_instance.stop()
        _playwright_instance = None

    _page_instance = None
    
async def remove_lock_files():
    """删除浏览器用户数据目录下的锁文件，防止浏览器打不开"""
    if not CHROME_USER_DATA_DIR:
        log_info("使用默认chromium浏览器，无需清理缓存")
        return
        
    lock_files_to_remove = ["SingletonLock", "SingletonCookie", "SingletonSocket"]
    if os.path.exists(CHROME_USER_DATA_DIR):
        for file_name in lock_files_to_remove:
            file_path = os.path.join(CHROME_USER_DATA_DIR, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    log_info(f"Successfully removed lock file: {file_path}")
                except OSError as e:
                    log_info(f"Error removing lock file {file_path}: {e}")
            # No need to log if file doesn't exist during cleanup
    else:
        log_info(f"User data directory not found, skipping lock file cleanup: {CHROME_USER_DATA_DIR}")



async def login_sso():
    """处理飞书SSO登录流程"""
    _, _, page = await get_playwright()

    # 检查页面是否包含"飞书登录"文本
    # 打印当前页面url
    log_info(f"当前页面url:{page.url}")
    if "sso.yunjiglobal.com/?backUrl=" in page.url:
        # 点击飞书登录按钮
        await page.get_by_text("飞书登录").click()
        log_info(f"等待飞书授权登录")
        # 等待"授权"按钮出现
        try:
            await page.wait_for_selector('button:has-text("授权")', timeout=30000)
            # 点击授权按钮
            log_debug("点击授权")
            await page.get_by_role("button", name="授权", exact=True).click()
            log_debug("登录成功")
            return "登录成功"
        except Exception as e:
            log_error(f"等待授权按钮出现时发生错误: {e}")
            return "登录失败"
    elif "accounts.feishu.cn" in page.url:
        # 等待"授权"按钮出现
        try:
            await page.wait_for_selector('button:has-text("授权")', timeout=30000)
            # 点击授权按钮
            log_debug("点击授权")
            await page.get_by_role("button", name="授权", exact=True).click()
            log_debug("登录成功")
            return "登录成功"
        except Exception as e:
            log_info(f"扫描登录")
            return "请用户扫码登录"
    else:
        # 页面不包含"飞书登录"文本，无需登录
        log_info(f"无需登录")
        return "无需登录"


async def open_create_customer_group_page():
    """打开客群列表页面并点击新建客群按钮"""
    _, _, page = await get_playwright()

    open_url = "https://portrait.yunjiglobal.com/customersystem/customerList?identify=cgs-cgm-customerList&d=1744176806057"
    # 打开客群列表页面
    await page.goto(open_url)

    login_result = await login_sso()
    log_debug(f"判断登录结果:{login_result}")
    if login_result == "登录成功":
        # 等待两秒
        await asyncio.sleep(2)
        log_debug(f"重新打开页面")
        await page.goto(open_url)
    elif login_result == "登录失败":
        return "登录失败，请提示用户使用飞书扫码登录"

    log_debug(f"开始新建客群")
    content = page.frame_locator("iframe")
    await content.get_by_role("button", name="新建客群").click()

    return "已进入新建客群页面"


async def fill_customer_group_info(group_name: str, business_type: str):
    """填写客群基本信息

    Args:
        group_name: 客群名称
        business_type: 业务类型
    """
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")

    # 填写客群名称
    await content.get_by_role("textbox", name="请输入字母、数字、下划线和汉字格式的客群名称，最多20字").click()
    await content.get_by_role("textbox", name="请输入字母、数字、下划线和汉字格式的客群名称，最多20字").fill(group_name)

    # 选择业务类型
    await content.get_by_role("textbox", name="请选择").click()
    await content.get_by_text(business_type).click()

    # 选择动态客群
    await content.get_by_role("radio", name="动态客群（每日0点重新按照筛选条件更新客群用户）").click()

    # 点击预估客群人数
    await content.get_by_role("button", name="点我预估客群人数").click()

    return f"已填写客群基本信息：名称={group_name}，业务类型={business_type}"


async def print_iframe_snapshot(page):
    iframe = page.frame_locator("iframe")
    body = iframe.locator('body')
    snapshot = await body.aria_snapshot()
    log_debug(f"snapshot:{snapshot}")

    # log_debug(f"page accessibility:{await page.accessibility.snapshot()}")


async def fill_customer_group_user_tag_set_basic_info(
    identity_types: list[str] = None,
    v2_unregistered: str = None
):
    """
    新增客群的用户标签，填写用户身份及是否推客用户。
    
    Args:
        identity_types: 新制度用户身份，可多选，例如 ["P1", "V3"]
                       可选值包括: "P1", "P2", "P3", "P4", "V1", "V2", "V3", "VIP"
                       不区分大小写，如"p1"也会被识别为"P1"
        v2_unregistered: V2以上未注册推客用户，可选值: "是", "否"
    
    :return: 操作结果描述
    """
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")
    log_debug(f"start set basic info")
    # await print_iframe_snapshot(page)

    # 切换到基础信息和云集属性标签页
    await content.get_by_role("tab", name="基础信息").click()
    await content.get_by_role("tab", name="云集属性").click()
    
    # 处理新制度用户身份选项
    if identity_types and isinstance(identity_types, list):
        valid_identity_types = ["P1", "P2", "P3", "P4", "V1", "V2", "V3", "VIP"]
        # 创建大小写匹配字典
        identity_map = {item.upper(): item for item in valid_identity_types}
        
        for identity in identity_types:
            # 将用户输入转为大写进行匹配
            upper_identity = identity.upper() if isinstance(identity, str) else ""
            if upper_identity in identity_map:
                # 获取正确大小写的身份值
                actual_identity = identity_map[upper_identity]
                if actual_identity == "VIP":
                    # VIP选项有多个，需要使用nth(1)
                    await content.get_by_text(actual_identity, exact=True).nth(1).click()
                else:
                    await content.get_by_text(actual_identity, exact=True).click()
    
    # 处理V2以上未注册推客用户选项
    if v2_unregistered in ["是", "否"]:
        # 获取云集属性标签下的"是"或"否"选项
        await content.get_by_label("云集属性").get_by_text(v2_unregistered, exact=True).nth(4).click()

    return "已完成用户标签基础信息填写"



async def add_user_behavior_search_tags_test():
    """添加一个搜索主题的用户行为标签"""
    return await add_user_behavior_common_tags(
        time_range_type="最近",
        time_range_value="10",
        action_type="没做过",
        theme="搜索",
        dimension="搜索词",
        dimension_condition="包含",
        dimension_value="轻姿养",
        metric="搜索次数",
        metric_condition=">=",
        metric_value="1"
    )


async def add_user_behavior_common_tags(
    time_range_type: str = "最近",
    time_range_value: str = None,
    action_type: str = "做过",
    theme: str = "购买", 
    dimension: str = None, 
    dimension_condition: str = None,
    dimension_value: str = None,
    metric: str = None,
    metric_condition: str = None,
    metric_value: str = None,
    metric_value_end: str = None 
):
    """添加一个通用的用户行为标签

    Args:
        time_range_type: 时间范围类型："最近"或"任意时间"
        time_range_value: 时间范围值，天数，如："7"
        action_type: 行为类型："做过"或"没做过"
        theme: 主题："购买"或"搜索"等
        dimension: 维度选项。当theme="购买"时可用：
            - 类目相关：["后台一级类目", "后台二级类目", "后台三级类目", "后台四级类目"]
              (条件均为=或!=，值为字符串，支持下拉列表多选)
            - 商品相关：["商品品牌", "商品名称", "商品id"] 
              (条件均为=或!=，品牌需从下拉列表选择，其他为字符串)
            - 其他："统计日期"
        dimension_condition: 维度条件：通常为=或!=
        dimension_value: 维度值：根据dimension类型提供相应字符串，多个值可用逗号(,或，)分隔
        metric: 指标名称。当theme="购买"时可用：
            ["购买金额", "购买件数", "购买净金额", "购买订单数"]
            (所有指标条件均支持=, >=, <=, <, >，值均为数字)
        metric_condition: 指标条件：=, >=, <=, <, >, 介于
        metric_value: 指标值：数字类型，当metric_condition="介于"时为范围开始值
        metric_value_end: 指标范围结束值：仅当metric_condition="介于"时使用
    """
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")
    # 添加新的行为标签
    await content.get_by_role("button", name=" 添加").click()
    # 定位最新添加的行
    row_class_name = ".sql-item"
    item_count = await content.locator(row_class_name).count()
    item = content.locator(row_class_name).nth(item_count - 1)

    # 选择时间范围类型
    await item.locator(".el-select__caret").first.click()
    await content.get_by_role("listitem").filter(has_text=time_range_type).click()

    # 填写时间范围值
    if time_range_value:
        await item.get_by_role("textbox", name="天数").last.fill(time_range_value)

    # 选择行为类型（做过/没做过）
    await item.get_by_role("textbox", name="请选择").nth(0).click()
    await content.get_by_role("listitem").filter(has_text=re.compile(f"^{action_type}$")).click()

    # 选择主题
    await item.get_by_role("textbox", name="选择主题").last.click()
    await content.get_by_role("listitem").filter(has_text=theme).click()

    # 根据是否有维度来确定指标的位置
    textbox_index = 1  # 初始值，用于追踪当前到了第几个"请选择"框
    input_index = 0    # 初始值，用于追踪当前到了第几个"请输入"框

    # 设置维度（如果有）
    if dimension:
        # 选择维度
        await item.get_by_role("textbox", name="选择维度").last.click()
        await content.get_by_role("listitem").filter(has_text=re.compile(f"^{dimension}$")).click()

        # 设置维度条件
        if dimension_condition:
            await item.get_by_role("textbox", name="请选择").nth(textbox_index).click()
            await content.get_by_role("listitem").filter(has_text=re.compile(f"^{dimension_condition}$")).click()
            textbox_index += 1
            # 填写维度值
            if dimension_value:
                # 检查是否是需要从下拉列表中选择的类目
                need_dropdown_selection = dimension in ["后台一级类目", "后台二级类目", "后台三级类目", "后台四级类目", "商品品牌"]
                
                # 处理多个维度值，支持中英文逗号分隔
                dimension_values = []
                if ',' in dimension_value or '，' in dimension_value:
                    for sep in [',', '，']:
                        if sep in dimension_value:
                            dimension_values.extend([v.strip() for v in dimension_value.split(sep) if v.strip()])
                else:
                    dimension_values = [dimension_value]

                
                log_debug(f"处理维度值: {dimension_values}")
                
                for value in dimension_values:
                    if not value:
                        continue
                        
                    if need_dropdown_selection:
                        # dimension_input = item.locator(".el-select__input").nth(input_index)
                        dimension_input  = content.locator(".sql-row").nth(item_count - 1).locator(".el-select__input").nth(input_index)
                    else:
                        dimension_input = item.get_by_role("textbox", name="请输入").nth(input_index)
                    # log_debug(f"点击维度输入框数量：{await dimension_input.count()}")
                    await dimension_input.click()
                    await dimension_input.fill(value) 
                    await asyncio.sleep(0.5)
                    
                    if need_dropdown_selection:
                        # 获取所有列表项
                        list_items = content.get_by_role("listitem")
                        count = await list_items.count()
                        log_debug(f"找到 {count} 个下拉选项")
                        log_debug(f"下拉选项的文本是：")
                        for i in range(count):
                            item = list_items.nth(i)
                            text = await item.text_content()
                            log_debug(f"{text}")
                        
                        # 修改：只有当dimension=="商品品牌"时才勾选所有下拉列表，其他情况只勾选第一个选项
                        if dimension == "商品品牌":
                            # 勾选所有选项
                            for i in range(count):
                                # 给UI一些响应时间
                                await asyncio.sleep(0.2)
                                item = list_items.nth(i)
                                # 获取文本内容（可选）
                                text = await item.text_content()
                                log_debug(f"点击下拉选项: {text}")
                                # 点击选项
                                await item.click()
                        else:
                            # 其他维度只勾选第一个选项
                            if count > 0:
                                await asyncio.sleep(0.2)
                                item = list_items.nth(0)
                                text = await item.text_content()
                                log_debug(f"点击第一个下拉选项: {text}")
                                await item.click()
                    
                    # 点击空白区域
                    await content.locator(".custom-editer > div").first.click()
                    await asyncio.sleep(0.2)

                
                input_index += 1

    # 设置指标（如果有）
    if metric:
        # 如果没有选择维度，则从维度选项框里选择指标
        metric_title = "选择指标"
        if not dimension:
            metric_title = "选择维度"
        # metric_input = item.get_by_role("textbox", name=metric_title)
        metric_input = content.get_by_placeholder(metric_title).last  # 使用了下拉列表选择商品维度之后，获取下一个下拉列表要从content中寻找
        # log_debug(f"指标组件名称：{metric_title},count:{metric_input.count()},is_visible:{await metric_input.is_visible()}")
        await metric_input.wait_for(state="visible", timeout=5000)
        await metric_input.click()
        await content.get_by_role("listitem").filter(has_text=re.compile(f"^{metric}$")).click()

        # 设置指标条件
        if metric_condition:
            # await item.get_by_role("textbox", name="请选择").nth(textbox_index).click()
            await content.get_by_role("textbox", name="请选择").last.click()
            await content.get_by_role("listitem").filter(has_text=re.compile(f"^{metric_condition}$")).click()

            # 填写指标值
            if metric_value:
                # await item.get_by_role("textbox", name="请输入").nth(input_index).click()
                # await item.get_by_role("textbox", name="请输入").nth(input_index).fill(metric_value)
                metric_input = content.get_by_role("textbox", name="请输入")
                metric_input_count = await metric_input.count()
                if metric_condition == "介于" and metric_value_end:
                    await metric_input.nth(metric_input_count - 2).click()
                    await metric_input.nth(metric_input_count - 2).fill(metric_value)
                    await metric_input.nth(metric_input_count - 1).click()
                    await metric_input.nth(metric_input_count - 1).fill(metric_value_end)
                else:
                    await metric_input.nth(metric_input_count - 1).click()
                    await metric_input.nth(metric_input_count - 1).fill(metric_value)
                
    return f"已添加{theme}用户行为标签"


async def send_llm_request(content: str) -> str:
    """
    发送LLM请求
    
    Args:
        content: 要发送给LLM的内容
        
    Returns:
        LLM的响应内容
    """
    
    # 从环境变量中读取llm_key
    llm_key = os.environ.get("llm_key")
    if not llm_key:
        log_error("环境变量llm_key未设置")
        raise ValueError("环境变量llm_key not found，请联系管理员设置llm_key")
    
    url = "https://talentshot.yunjiglobal.com/digitalhuman/api/llm/completions"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {llm_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "content": content,
        "model": "deepseek",
        "history_message": [],
        "temperature": 0.3,
        "timeout": 60,
        "trace_tags": [],
        "trace_session_id": "",
        "trace_user_id": ""
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=120)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0 and "data" in result and "content" in result["data"]:
                    return result["data"]["content"]
                else:
                    log_error(f"LLM响应格式异常: {result}")
                    return f"LLM响应格式异常: {result}"
            else:
                log_error(f"LLM请求失败，状态码: {response.status_code}")
                return f"LLM请求失败，状态码: {response.status_code}"
    except Exception as e:
        log_error(f"发送LLM请求时出错: {str(e)}")
        return f"发送LLM请求时出错: {str(e)}"


async def toggle_behavior_tag_relation_to_or():
    """将用户行为标签之间的关系从"且"切换为"或"

    用户行为标签之间默认是"且"关系，即用户需要同时满足所有标签条件。
    本函数用于将这种关系切换为"或"关系，即用户只需满足任一标签条件。

    Returns:
        str: 操作结果描述
    """
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")

    await content.get_by_text("且", exact=True).nth(1).click()

    return "已将用户行为标签关系从「且」切换为「或」"


async def estimate_customer_group_size():
    """预估客群人数
    Returns:
        str: 操作结果描述
    """
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")
    
    # 等待预估结果出现
    try:
        # 点击预估客群人数按钮
        await content.get_by_role("button", name="点我预估客群人数").click()
        return "已点击客群人数预估"
    except Exception as e:
        log_error(f"预估客群人数时出错: {e}")
        return f"预估客群人数时出错: {str(e)}"
