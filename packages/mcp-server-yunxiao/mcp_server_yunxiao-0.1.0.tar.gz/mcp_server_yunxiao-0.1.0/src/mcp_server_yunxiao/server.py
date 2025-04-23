"""
云霄服务工具定义和路由处理
"""
from asyncio.log import logger
from typing import Any
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from . import tool_yunxiao


server = Server("yunxiao")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """获取支持的工具列表"""
    return [
        types.Tool(
            name="DescribeSalePolicies",
            description="查询售卖推荐数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "Customhouse": {
                        "type": "string",
                        "description": "境内外，取值：境内，境外",
                        "default": "境内"
                    },
                    "Region": {
                        "type": "string",
                        "description": "地域，类似ap-guangzhou"
                    },
                    "Zone": {
                        "type": "string",
                        "description": "可用区，类似ap-guangzhou-8"
                    },
                    "InstanceFamily": {
                        "type": "string",
                        "description": "实例族，类似 SA5"
                    },
                    "InstanceFamilyState": {
                        "type": "string",
                        "description": "实例族售卖状态",
                        "default": "PRINCIPAL"
                    },
                    "InstanceFamilySupplyState": {
                        "type": "string",
                        "description": "实例族供货状态",
                        "default": "LTS"
                    },
                    "ZoneState": {
                        "type": "string",
                        "description": "可用区售卖状态",
                        "default": "PRINCIPAL"
                    },
                    "StockState": {
                        "type": "string",
                        "description": "库存状态",
                        "default": "WithStock"
                    },
                    "PageNumber": {
                        "type": "integer",
                        "description": "页码",
                        "default": 1
                    },
                    "PageSize": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 10
                    }
                }
            }
        ),
        types.Tool(
            name="DescribeInventory",
            description="查询库存数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域"
                    },
                    "Zone": {
                        "type": "string",
                        "description": "可用区"
                    },
                    "InstanceFamily": {
                        "type": "string",
                        "description": "实例族"
                    },
                    "InstanceType": {
                        "type": "string",
                        "description": "实例类型"
                    },
                    "Offset": {
                        "type": "integer",
                        "description": "偏移量",
                        "default": 0
                    },
                    "Limit": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 10
                    }
                },
                "required": ["Region"]
            }
        ),
        types.Tool(
            name="GetUserOwnedGrid",
            description="获取用户归属预扣统计",
            inputSchema={
                "type": "object",
                "properties": {
                    "AppId": {
                        "type": "integer",
                        "description": "APPID"
                    },
                    "Region": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "地域列表"
                    },
                    "Sort": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "排序规则"
                    },
                    "Offset": {
                        "type": "integer",
                        "description": "偏移量",
                        "default": 0
                    },
                    "Limit": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 20
                    }
                },
                "required": ["AppId"]
            }
        ),
        types.Tool(
            name="GetCustomerAccountInfo",
            description="获取客户账号信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "CustomerIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "客户ID列表"
                    }
                },
                "required": ["CustomerIds"]
            }
        ),
        types.Tool(
            name="QueryQuota",
            description="查询配额信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域"
                    },
                    "Limit": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 20
                    },
                    "Offset": {
                        "type": "integer",
                        "description": "偏移量",
                        "default": 0
                    },
                    "ZoneIds": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "可用区ID列表"
                    },
                    "AppIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "APPID列表"
                    },
                    "PayModes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "付费模式列表"
                    },
                    "InstanceTypes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例类型列表"
                    },
                    "InstanceFamilies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例族列表"
                    }
                },
                "required": ["Region"]
            }
        ),
        types.Tool(
            name="QueryInstanceFamilies",
            description="查询实例族信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "InstanceFamily": {
                        "type": "string",
                        "description": "实例族"
                    },
                    "States": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "状态列表"
                    },
                    "SupplyStates": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "供货状态列表"
                    },
                    "InstanceCategories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例分类列表"
                    },
                    "TypeNames": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "类型名称列表"
                    },
                    "InstanceClass": {
                        "type": "string",
                        "description": "实例规格"
                    },
                    "PageNumber": {
                        "type": "integer",
                        "description": "页码",
                        "default": 1
                    },
                    "PageSize": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 20
                    }
                }
            }
        ),
        types.Tool(
            name="GetInstanceCount",
            description="获取实例数量统计",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域"
                    },
                    "NextToken": {
                        "type": "string",
                        "description": "分页标记",
                        "default": ""
                    },
                    "Limit": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 20
                    },
                    "AppIds": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "APPID列表"
                    },
                    "Uins": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "UIN列表"
                    },
                    "InstanceTypes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例类型列表"
                    },
                    "InstanceFamilies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例族列表"
                    }
                },
                "required": ["Region"]
            }
        ),
        types.Tool(
            name="QueryInstances",
            description="查询实例列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域"
                    },
                    "NextToken": {
                        "type": "string",
                        "description": "分页标记",
                        "default": ""
                    },
                    "Limit": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 20
                    },
                    "AppIds": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "APPID列表"
                    },
                    "Uins": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "UIN列表"
                    },
                    "InstanceTypes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例类型列表"
                    },
                    "InstanceFamilies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例族列表"
                    }
                },
                "required": ["Region"]
            }
        ),
        types.Tool(
            name="GetInstanceDetails",
            description="获取实例详细信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域"
                    },
                    "NextToken": {
                        "type": "string",
                        "description": "分页标记",
                        "default": ""
                    },
                    "Limit": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 20
                    },
                    "AppIds": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "APPID列表"
                    },
                    "Uins": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "UIN列表"
                    },
                    "InstanceTypes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例类型列表"
                    },
                    "InstanceFamilies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "实例族列表"
                    }
                },
                "required": ["Region"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具调用
    
    Args:
        name: 工具名称
        arguments: 工具参数
        
    Returns:
        工具执行结果的JSON字符串
    """
    logger.info(f"Handling tool call: {name} with arguments: {arguments}")
    
    if name == "DescribeSalePolicies":
        result = tool_yunxiao.describe_sale_policies(
            customhouse=arguments.get("Customhouse", "境内"),
            region=arguments.get("Region"),
            zone=arguments.get("Zone"),
            instance_family=arguments.get("InstanceFamily"),
            instance_family_state=arguments.get("InstanceFamilyState", "PRINCIPAL"),
            instance_family_supply_state=arguments.get("InstanceFamilySupplyState", "LTS"),
            zone_state=arguments.get("ZoneState", "PRINCIPAL"),
            stock_state=arguments.get("StockState", "WithStock"),
            page_number=arguments.get("PageNumber", 1),
            page_size=arguments.get("PageSize", 10)
        )
    elif name == "DescribeInventory":
        result = tool_yunxiao.describe_inventory(
            region=arguments["Region"],
            zone=arguments.get("Zone"),
            instance_family=arguments.get("InstanceFamily"),
            instance_type=arguments.get("InstanceType"),
            offset=arguments.get("Offset", 0),
            limit=arguments.get("Limit", 10)
        )
    elif name == "GetUserOwnedGrid":
        result = tool_yunxiao.get_user_owned_grid(
            app_id=arguments["AppId"],
            region=arguments.get("Region"),
            sort=arguments.get("Sort"),
            offset=arguments.get("Offset", 0),
            limit=arguments.get("Limit", 20)
        )
    elif name == "GetCustomerAccountInfo":
        result = tool_yunxiao.get_customer_account_info(
            customer_ids=arguments["CustomerIds"]
        )
    elif name == "QueryQuota":
        result = tool_yunxiao.query_quota(
            region=arguments["Region"],
            limit=arguments.get("Limit", 20),
            offset=arguments.get("Offset", 0),
            zone_ids=arguments.get("ZoneIds"),
            app_ids=arguments.get("AppIds"),
            pay_modes=arguments.get("PayModes"),
            instance_types=arguments.get("InstanceTypes"),
            instance_families=arguments.get("InstanceFamilies")
        )
    elif name == "QueryInstanceFamilies":
        result = tool_yunxiao.query_instance_families(
            instance_family=arguments.get("InstanceFamily"),
            states=arguments.get("States"),
            supply_states=arguments.get("SupplyStates"),
            instance_categories=arguments.get("InstanceCategories"),
            type_names=arguments.get("TypeNames"),
            instance_class=arguments.get("InstanceClass"),
            page_number=arguments.get("PageNumber", 1),
            page_size=arguments.get("PageSize", 20)
        )
    elif name == "GetInstanceCount":
        result = tool_yunxiao.get_instance_count(
            region=arguments["Region"],
            next_token=arguments.get("NextToken", ""),
            limit=arguments.get("Limit", 20),
            app_ids=arguments.get("AppIds"),
            uins=arguments.get("Uins"),
            instance_types=arguments.get("InstanceTypes"),
            instance_families=arguments.get("InstanceFamilies")
        )
    elif name == "QueryInstances":
        result = tool_yunxiao.query_instances(
            region=arguments["Region"],
            next_token=arguments.get("NextToken", ""),
            limit=arguments.get("Limit", 20),
            app_ids=arguments.get("AppIds"),
            uins=arguments.get("Uins"),
            instance_types=arguments.get("InstanceTypes"),
            instance_families=arguments.get("InstanceFamilies")
        )
    elif name == "GetInstanceDetails":
        result = tool_yunxiao.get_instance_details(
            region=arguments["Region"],
            next_token=arguments.get("NextToken", ""),
            limit=arguments.get("Limit", 20),
            app_ids=arguments.get("AppIds"),
            uins=arguments.get("Uins"),
            instance_types=arguments.get("InstanceTypes"),
            instance_families=arguments.get("InstanceFamilies")
        )
    else:
        raise ValueError(f"Unknown tool: {name}")
        
    return [types.TextContent(type="text", text=str(result))] 

async def serve():
    """启动服务"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cvm",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        ) 