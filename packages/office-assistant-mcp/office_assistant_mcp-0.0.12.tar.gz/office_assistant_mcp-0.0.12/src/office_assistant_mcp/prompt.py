"""
提示词模块，用于存放各种提示词模板
"""

def get_planning_customer_group_prompt(user_query: str) -> str:
    """
    获取创建客群规划的提示词模板
    
    Args:
        user_query: 用户输入的创建客群的原样指令
    
    Returns:
        填充后的提示词
    """
    return f"""## 任务：新建客群参数检查与规划

## 指令：
分析 用户的输入的指令，检查创建客群所需信息：
1. 客群名称
2. 业务类型（活动运营、用户运营等）
3. 客群定义 (用户行为描述 或 用户身份类型，至少一项)

- 如果缺少信息，直接返回缺少的信息点列表。
- 如果信息完整，直接返回下方创建客群规划的操作步骤。

## 创建客群规划的操作步骤：

1. 调用 `open_create_customer_group_page`打开客群新建页面。
2. 调用 `fill_customer_group_info` (含客群名称, 业务类型默认为"活动运营")。
3. 如指定了用户身份，调用 `fill_customer_group_user_tag_set_basic_info`。
4. 填写用户行为标签前，对维度相关的描述，用户如果没有明确指定属于哪一级类目或品牌、或商品名，则调用`judge_category_or_brand_type`工具先去判断，再填写。
5. 如描述了用户行为许村添加标签，调用 `fill_customer_add_user_behavior_tag`。
6. 成功填写全部表单后，调用 `estimate_customer_group_size` 预估客群人数，填写表单失败则不执行客群人数预估。
7. 如果页面如需登录，调用 `login_sso`去登录。
8. 完成客群创建后，提醒用户：“已完成客群创建表单填写，请人工检查客群信息，再点击\“提交\”执行计划！”。
9. 注意：使用中文回复，步骤需按顺序一步一步执行，不能并发执行。（该提示也作为结果返回）

## 用户的输入
{user_query}

## 返回结果：
"""


def get_planning_message_plan_prompt(user_query: str) -> str:
    """
    获取创建短信计划规划的提示词模板
    
    Args:
        user_query: 用户输入的创建短信计划的原样指令
    
    Returns:
        填充后的提示词
    """
    return f"""## 任务：新建短信发送计划参数检查与规划

## 指令：
分析用户输入的指令，检查创建短信计划所需的以下必要信息是否齐全：
1. 客群ID
2. 发送时间
3. 商品ID，或者指定的日期二选一（包括今天、明天等表示日期的字符串）（如果指令中提到了日期，则用户指令中可以不提供商品ID，根据日期调用`search_date_cell`、`read_item_id`等飞书表格工具，从飞书表格中查询具体的商品ID）

- 如果缺少必填信息，直接返回缺少的信息点。
- 如果信息完整，直接返回下方创建短信计划规划的操作步骤。

## 规划的操作步骤：
1. 如果没有`商品ID`，但有指定日期，则根据日期调用`search_date_cell`、`read_item_id`等飞书表格工具，从飞书表格中查询具体的商品ID等商品信息。
2. 如果用户没有提供具体的`短信内容`，则调用`generate_item_sms_content`工具根据商品信息生成短信内容。
3. 调用 `open_create_customer_group_page` 打开短信计划页面。
4. 调用 `fill_message_group_id` 搜索并选择指定客群。
5. 调用 `fill_message_plan_info` 设置计划名称和发送时间。
6. 调用 `fill_message_content` 设置短信内容和商品链接。
7. 调用 `set_department_info` 设置默认的费用归属部门。
8. 如页面需要登录，调用 `login_sso` 去登录。
9. 注意：使用中文回复，步骤需按顺序一步一步执行，不能并发执行。（该提示也作为结果返回）

## 用户的输入指令
{user_query}

## 返回结果：
""" 