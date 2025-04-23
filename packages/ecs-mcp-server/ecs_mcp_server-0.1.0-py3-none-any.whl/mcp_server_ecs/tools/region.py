"""
Region and available zone related tool functions
"""
from typing import List, Optional

import volcenginesdkecs
from pydantic import BaseModel, Field
from mcp import types
from volcenginesdkecs.models import *

from mcp_server_ecs.common.client import get_volc_ecs_client
from mcp_server_ecs.common.errors import handle_error
from mcp_server_ecs.common.logs import LOG
from mcp_server_ecs.tools import register_tool


class DescribeRegionsParams(BaseModel):
    RegionIds: Optional[List[str]] = Field(
        default_factory=list,
        description="地域ID，最多支持20个ID",
    )

    MaxResults: Optional[int] = Field(
        default=20,
        description="分页查询时设置的每页行数，需要根据用户的意图来设置",
        ge=0,
        le=100,
    )

    NeedNum: Optional[int] = Field(
        default=20,
        description="用户需要查询的事件总数，需要根据用户的意图来设置",
    )


class DescribeZonesParams(BaseModel):
    ZoneIds: Optional[List[str]] = Field(
        default_factory=list,
        description="可用区ID，最多支持20个",
    )


@register_tool(name="describe_regions",
               description="Query region list",
               model_class=DescribeRegionsParams)
async def describe_regions(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client()
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_regions(
                volcenginesdkecs.DescribeRegionsRequest(
                    region_ids=args.get("RegionIds"),
                    max_results=args.get("MaxResults"),
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "regions", None):
                return handle_error("describe_regions")

            total_results.extend(response.regions)

            if len(total_results) >= args.get("NeedNum") or not response.next_token:
                total_results = total_results[: args.get("NeedNum")]
                break

            next_token = response.next_token

        LOG.info(f"Total regions found: {len(total_results)}")
        return [types.TextContent(
            type="text",
            text=f"Results: {total_results}"
        )]

    except Exception as e:
        return handle_error("describe_regions", e)


@register_tool(name="describe_zones",
               description="Query available zone list",
               model_class=DescribeZonesParams)
async def describe_zones(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client()
        response = volc_client.describe_zones(
            volcenginesdkecs.DescribeZonesRequest(
                zone_ids=args.get("ZoneIds"),
            )
        )

        if not response or not getattr(response, "zones", None):
            return handle_error("describe_zones")

        return [types.TextContent(
            type="text",
            text=f"Results: {response.zones}"
        )]

    except Exception as e:
        return handle_error("describe_zones", e)
