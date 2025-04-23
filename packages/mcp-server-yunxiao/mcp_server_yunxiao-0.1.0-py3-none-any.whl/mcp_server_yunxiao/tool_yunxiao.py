"""
云霄服务工具模块
"""
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from .client import get_yunxiao_client

def describe_sale_policies(
    customhouse: str = "境内",
    region: Optional[str] = None,
    zone: Optional[str] = None,
    instance_family: Optional[str] = None,
    instance_family_state: str = "PRINCIPAL",
    instance_family_supply_state: str = "LTS",
    zone_state: str = "PRINCIPAL",
    stock_state: str = "WithStock",
    page_number: int = 1,
    page_size: int = 10
) -> str:
    """查询售卖推荐
    
    Args:
        customhouse: 境内外，取值：境内，境外
        region: 地域，类似ap-guangzhou
        zone: 可用区，类似ap-guangzhou-8
        instance_family: 实例族，类似 SA5
        instance_family_state: 实例族售卖状态
        instance_family_supply_state: 实例族供货状态
        zone_state: 可用区售卖状态
        stock_state: 库存状态
        page_number: 页码
        page_size: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "customhouse": [customhouse],
        "instanceFamilyState": [instance_family_state],
        "instanceFamilySupplyState": [instance_family_supply_state],
        "zoneState": [zone_state],
        "stockState": [stock_state],
        "pageNumber": page_number,
        "pageSize": page_size
    }
    
    if region:
        request_body["region"] = [region]
    if zone:
        request_body["zone"] = [zone]
    if instance_family:
        request_body["instanceFamily"] = [instance_family]
        
    response = client.post("/compass/sales-policy/list", request_body)
    
    # 处理响应数据
    result = {}
    if "data" in response:
        data = response["data"]
        result["data"] = [{
            "境内外": item["customhouse"],
            "可用区名称": item["zoneName"],
            "实例族": item["instanceFamily"],
            "售卖状态": {
                "PRINCIPAL": "主力",
                "SECONDARY": "非主力"
            }.get(item["instanceFamilyState"], item["instanceFamilyState"]),
            "供货策略": {
                "LTS": "持续供应",
                "EOL": "停止供应"
            }.get(item["instanceFamilySupplyState"], item["instanceFamilySupplyState"]),
            "可用区售卖策略": {
                "PRINCIPAL": "主力",
                "SECONDARY": "非主力"
            }.get(item["zoneState"], item["zoneState"]),
            "实例分类": item["instanceCategory"],
            "库存情况": {
                "WithStock": "库存充足",
                "ClosedWithStock": "库存紧张",
                "WithoutStock": "售罄"
            }.get(item["stockState"], item["stockState"]),
            "售卖策略": {
                0: "未知",
                1: "推荐购买",
                2: "正常购买",
                3: "即将售罄",
                4: "联系购买",
                5: "无法购买",
                6: "请预约"
            }.get(item["salesPolicy"], "未知"),
            "库存/核": f"{item['stock']}核",
            "十六核以上库存核": f"{item['stock16c']}核",
            "数据更新时间": item["updateTime"]
        } for item in data["data"]]
        result["totalCount"] = data["totalCount"]
        
    return json.dumps(result, ensure_ascii=False)

def describe_inventory(
    region: str,
    zone: Optional[str] = None,
    instance_family: Optional[str] = None,
    instance_type: Optional[str] = None,
    offset: int = 0,
    limit: int = 10
) -> str:
    """查询库存数据
    
    Args:
        region: 地域
        zone: 可用区
        instance_family: 实例族
        instance_type: 实例类型
        offset: 偏移量
        limit: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "chargeType": [2],
        "pool": ["public"],
        "offset": offset,
        "limit": limit,
        "region": region
    }
    
    if zone:
        request_body["zone"] = [zone]
    if instance_family:
        request_body["instanceFamily"] = instance_family
    if instance_type:
        request_body["instanceType"] = [instance_type]
        
    response = client.post("/beacon/ceres/instance-sales-config/list", request_body)
    
    # 处理响应数据
    result = {}
    if "data" in response:
        data = response["data"]
        result["data"] = [{
            "可用区": item["zone"],
            "实例族": item["instanceFamily"],
            "实例类型": item["instanceType"],
            "实例CPU数": f"{item['cpu']}核",
            "实例内存": item["mem"],
            "实例GPU数": item["gpu"],
            "库存": f"{item['inventory']}核",
            "数据更新时间": datetime.fromtimestamp(item["updateTime"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        } for item in data["data"]]
        result["totalCount"] = data["totalCount"]
        
    return json.dumps(result, ensure_ascii=False)

def get_user_owned_grid(
    app_id: int,
    region: Optional[List[str]] = None,
    sort: Optional[List[str]] = None,
    offset: int = 0,
    limit: int = 20
) -> str:
    """获取用户归属预扣统计
    
    Args:
        app_id: APPID
        region: 地域列表
        sort: 排序规则
        offset: 偏移量
        limit: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "limit": limit,
        "offset": offset,
        "appId": app_id
    }
    
    if region:
        request_body["region"] = region
    if sort:
        request_body["sort"] = sort
        
    response = client.post("/data360/user360/grid", request_body)
    return json.dumps(response, ensure_ascii=False)

def get_user_owned_instances(
    app_id: int,
    region: Optional[List[str]] = None,
    sort: Optional[List[str]] = None,
    offset: int = 0,
    limit: int = 20
) -> str:
    """获取用户归属实例统计
    
    Args:
        app_id: APPID
        region: 地域列表
        sort: 排序规则
        offset: 偏移量
        limit: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "limit": limit,
        "offset": offset,
        "appId": app_id
    }
    
    if region:
        request_body["region"] = region
    if sort:
        request_body["sort"] = sort
        
    response = client.post("/data360/user360/instance", request_body)
    return json.dumps(response, ensure_ascii=False)

def get_customer_account_info(customer_ids: List[str]) -> str:
    """客户信息查询
    
    Args:
        customer_ids: 客户ID列表
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    response = client.post("/data360/customer/batch-query-account-info", customer_ids)
    return json.dumps(response, ensure_ascii=False)

def query_quota(
    region: str,
    limit: int = 20,
    offset: int = 0,
    zone_ids: Optional[List[int]] = None,
    app_ids: Optional[List[str]] = None,
    pay_modes: Optional[List[str]] = None,
    instance_types: Optional[List[str]] = None,
    instance_families: Optional[List[str]] = None
) -> str:
    """查询用户配额
    
    Args:
        region: 地域
        limit: 每页数量
        offset: 偏移量
        zone_ids: 可用区ID列表
        app_ids: 用户AppID列表
        pay_modes: 计费模式列表
        instance_types: 实例类型列表
        instance_families: 机型族列表
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "region": region,
        "productCode": "cvm-instance",
        "limit": limit,
        "offset": offset
    }
    
    if zone_ids:
        request_body["zoneId"] = zone_ids
    if app_ids:
        request_body["appId"] = app_ids
    if pay_modes:
        request_body["payMode"] = pay_modes
    if instance_types:
        request_body["instanceType"] = instance_types
    if instance_families:
        request_body["instanceFamily"] = instance_families
        
    response = client.post("/data360/quota/query", request_body)
    return json.dumps(response, ensure_ascii=False)

def query_instance_families(
    instance_family: Optional[str] = None,
    states: Optional[List[str]] = None,
    supply_states: Optional[List[str]] = None,
    instance_categories: Optional[List[str]] = None,
    type_names: Optional[List[str]] = None,
    instance_class: Optional[str] = None,
    page_number: int = 1,
    page_size: int = 20
) -> str:
    """查询机型族信息
    
    Args:
        instance_family: 实例族名称
        states: 实例族状态列表
        supply_states: 实例族供货状态列表
        instance_categories: 实例分类列表
        type_names: 类型名称列表
        instance_class: 实例类型分类
        page_number: 页码
        page_size: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "pageNumber": page_number,
        "pageSize": page_size,
        "display": True
    }
    
    if instance_family:
        request_body["instanceFamily"] = instance_family
    if states:
        request_body["state"] = states
    if supply_states:
        request_body["supplyState"] = supply_states
    if instance_categories:
        request_body["instanceCategory"] = instance_categories
    if type_names:
        request_body["typeName"] = type_names
    if instance_class:
        request_body["instanceClass"] = instance_class
        
    response = client.post("/data360/instance-family", request_body)
    return json.dumps(response, ensure_ascii=False)

def get_instance_count(
    region: str,
    next_token: str = "",
    limit: int = 20,
    app_ids: Optional[List[int]] = None,
    uins: Optional[List[str]] = None,
    instance_types: Optional[List[str]] = None,
    instance_families: Optional[List[str]] = None
) -> str:
    """查询实例数量
    
    Args:
        region: 地域
        next_token: 分页token
        limit: 每页数量
        app_ids: AppID列表
        uins: UIN列表
        instance_types: 实例类型列表
        instance_families: 实例族列表
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "hasTotalCount": True,
        "nextToken": next_token,
        "limit": limit,
        "region": region
    }
    
    if app_ids:
        request_body["appId"] = app_ids
    if uins:
        request_body["uin"] = uins
    if instance_types:
        request_body["instanceType"] = instance_types
    if instance_families:
        request_body["instanceFamily"] = instance_families
        
    response = client.post("/data360/instance/count", request_body)
    return str(response)

def query_instances(
    region: str,
    next_token: str = "",
    limit: int = 20,
    app_ids: Optional[List[int]] = None,
    uins: Optional[List[str]] = None,
    instance_types: Optional[List[str]] = None,
    instance_families: Optional[List[str]] = None
) -> str:
    """查询实例列表
    
    Args:
        region: 地域
        next_token: 分页token
        limit: 每页数量
        app_ids: AppID列表
        uins: UIN列表
        instance_types: 实例类型列表
        instance_families: 实例族列表
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "hasTotalCount": True,
        "nextToken": next_token,
        "limit": limit,
        "region": region
    }
    
    if app_ids:
        request_body["appId"] = app_ids
    if uins:
        request_body["uin"] = uins
    if instance_types:
        request_body["instanceType"] = instance_types
    if instance_families:
        request_body["instanceFamily"] = instance_families
        
    response = client.post("/data360/instance", request_body)
    return json.dumps(response, ensure_ascii=False)

def get_instance_details(
    region: str,
    next_token: str = "",
    limit: int = 20,
    app_ids: Optional[List[int]] = None,
    uins: Optional[List[str]] = None,
    instance_types: Optional[List[str]] = None,
    instance_families: Optional[List[str]] = None
) -> str:
    """查询实例详情
    
    Args:
        region: 地域
        next_token: 分页token
        limit: 每页数量
        app_ids: AppID列表
        uins: UIN列表
        instance_types: 实例类型列表
        instance_families: 实例族列表
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "hasTotalCount": True,
        "nextToken": next_token,
        "limit": limit,
        "region": region
    }
    
    if app_ids:
        request_body["appId"] = app_ids
    if uins:
        request_body["uin"] = uins
    if instance_types:
        request_body["instanceType"] = instance_types
    if instance_families:
        request_body["instanceFamily"] = instance_families
        
    response = client.post("/data360/instance/detail", request_body)
    return json.dumps(response, ensure_ascii=False) 