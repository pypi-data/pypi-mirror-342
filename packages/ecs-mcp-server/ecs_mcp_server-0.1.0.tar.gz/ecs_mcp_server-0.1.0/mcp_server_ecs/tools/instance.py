"""
Instance related tool functions
"""
from typing import List, Optional

import volcenginesdkecs
from mcp import types
from pydantic import BaseModel, Field
from volcenginesdkecs.models import *

from mcp_server_ecs.common.client import get_volc_ecs_client
from mcp_server_ecs.common.errors import handle_error
from mcp_server_ecs.common.logs import LOG
from mcp_server_ecs.tools import register_tool


class DescribeInstancesParams(BaseModel):
    DedicatedHostClusterId: Optional[str] = Field(
        default=None,
        description="专有宿主机集群ID。您可以调用DescribeDedicatedHostClusters接口查询宿主机集群ID",
    )

    DedicatedHostId: Optional[str] = Field(
        default=None,
        description="专有宿主机ID。您可以调用DescribeDedicatedHosts接口查询专有宿主机列表",
    )

    DeploymentSetGroupNumbers: Optional[List[int]] = Field(
        default_factory=list,
        description="使用部署集组号，查询对应部署集组内的实例",
    )

    DeploymentSetIds: Optional[List[str]] = Field(
        default_factory=list,
        description="使用部署集ID，查询对应部署集内的实例",
    )

    EipAddresses: Optional[List[str]] = Field(
        default_factory=list,
        description="公网IP地址，最多支持100个。您可以调用DescribeEipAddresses接口查询公网IP地址",
    )

    HpcClusterId: Optional[str] = Field(
        default=None,
        description="当查询高性能计算GPU型实例时，可以指定高性能计算集群ID",
    )

    InstanceChargeType: Optional[str] = Field(
        default=None,
        description="实例的计费方式，取值：PostPaid：按量计费，PrePaid：包年包月",
    )

    InstanceIds: Optional[List[str]] = Field(
        default_factory=list,
        description="实例ID，最多支持100个",
    )

    InstanceName: Optional[str] = Field(
        default=None, description="实例的名称，支持关键字模糊查询"
    )

    InstanceTypeFamilies: Optional[List[str]] = Field(
        default_factory=list,
        description="根据规格族过滤实例，最多支持100个实例规格族",
    )

    InstanceTypeIds: Optional[List[str]] = Field(
        default_factory=list,
        description="根据规格过滤实例，最多支持100个实例规格",
    )

    Ipv6Addresses: Optional[List[str]] = Field(
        default_factory=list,
        description="实例的IPv6地址",
    )

    KeyPairName: Optional[str] = Field(default=None, description="密钥对的名称")

    PrimaryIpAddress: Optional[str] = Field(
        default=None, description="实例的私网IP地址，例如主网卡或辅助网卡IP地址"
    )

    ProjectName: Optional[str] = Field(
        default=None,
        description="资源所属项目，一个资源只能归属于一个项目。只能包含字母、数字、下划线'_'、点'.'和中划线'-'。长度限制在64个字符以内",
    )

    ScheduledInstanceId: Optional[str] = Field(
        default=None,
        description="弹性预约单ID。您可以调用DescribeScheduledInstances接口查询弹性预约单ID",
    )

    Status: Optional[List[str]] = Field(
        default_factory=list,
        description="实例的状态，取值：CREATING：创建中，RUNNING：运行中，STOPPING：停止中，STOPPED：已停止，REBOOTING: 重启中，STARTING：启动中，REBUILDING：重装中，RESIZING：更配中，ERROR：错误，DELETING：删除中",
    )

    TagFilters: Optional[List[str]] = Field(
        default_factory=list,
        description="""
            根据标签查询资源时指定的标签键和值，不允许重复，格式如下：
            [
                {
                    "Key": "sys:tag:createdBy",
                    "Value": "IAMUser:3723****:****"
                },
                {
                    "Key": "sys:tag:createdBy",
                    "Value": "IAMUser:3723****:****"
                }
            ],
        """,
    )

    VpcId: Optional[str] = Field(
        default=None,
        description="私有网络ID。您可以调用DescribeVpcs查询满足条件的私有网络",
    )

    ZoneId: Optional[str] = Field(
        default=None,
        description="实例所属可用区ID。您可以调用DescribeZones查询一个地域下的可用区信息",
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


class DescribeImagesParams(BaseModel):
    ImageIds: Optional[List[str]] = Field(
        default_factory=list,
        description="镜像的ID，最多支持100个ID。您可以调用CreateImage、ImportImage接口获取自定义镜像ID，或调用本接口查询获取。参数 - N：表示镜像ID的序号。多个镜像ID之间用&分隔",
    )

    ImageName: Optional[str] = Field(
        default=None,
        description="镜像名称"
    )

    InstanceTypeId: Optional[str] = Field(
        default=None,
        description="实例的规格ID，传入本参数时，将返回该规格可用的镜像ID列表",
    )

    IsLTS: Optional[bool] = Field(
        default=False,
        description="公共镜像是否长期维护。取值：true：长期维护的公共镜像。false（默认）：本参数不生效。说明：本参数仅传true时生效，表示查询长期维护的公共镜像；传false或不传值时，本参数不生效",
    )

    IsSupportCloudInit: Optional[bool] = Field(
        default=True,
        description="镜像是否支持Cloud-init。取值：true：支持，false：不支持",
    )

    NextToken: Optional[str] = Field(
        default=None,
        description="分页查询凭证，用于标记分页的位置，初次调用该接口时无需设置。下次查询时，取值为上一次API调用返回的NextToken参数值",
    )

    OsType: Optional[str] = Field(
        default=None, description="操作系统类型。取值：Linux，Windows")

    Platform: Optional[str] = Field(
        default=None,
        description="镜像操作系统的发行版本。取值：CentOS，Debian，veLinux，Windows Server，Fedora，OpenSUSE，Ubuntu",
    )

    ProjectName: Optional[str] = Field(
        default="default",
        description="资源所属项目"
    )

    Status: Optional[List[str]] = Field(
        default_factory=list,
        description="镜像状态，最多支持10个。取值：available（默认）：可用，creating：创建中，error：错误。参数 - N：表示镜像状态的序号。多个镜像状态之间用&分隔",
    )

    TagFilters: Optional[List[str]] = Field(
        default_factory=list,
        description="镜像标签的标签键和值。TagFilters.N.Key：表示标签键的序号，取值范围：1～10。TagFilters.N.Values.N：表示标签值的序号，同一标签键最多支持同时查询3个标签值",
    )

    Visibility: Optional[str] = Field(
        default=None,
        description="镜像的可见性。取值：public：公共镜像，private：自定义镜像，shared：共享镜像",
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


class DescribeInstanceTypesParams(BaseModel):
    ImageId: Optional[str] = Field(
        default=None, description="镜像ID，查询该镜像可创建的实例规格")

    InstanceTypeIds: Optional[List[str]] = Field(
        default_factory=list,
        description="指定查询的实例规格。取值请参见实例规格介绍。参数 - N：表示实例规格的序号，取值范围：1～100。N大于100时，仅前100个生效。多个InstanceTypeId 之间用&分隔。说明：不传则默认查询所有实例规格的信息",
    )

    NextToken: Optional[str] = Field(
        default=None,
        description="分页查询凭证，用于标记分页的位置，初次调用该接口时无需设置。下次查询时，取值为上一次API调用返回的NextToken参数值",
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


class DescribeAvailableResourceParams(BaseModel):
    DestinationResource: Optional[str] = Field(
        default=None,
        description="要查询的资源类型(必填参数)。取值：InstanceType：实例规格。VolumeType：云盘类型。DedicatedHost：专有宿主机规格。专有宿主机规格请参见规格介绍",
    )

    ElasticScheduledInstanceType: Optional[str] = Field(
        default=None,
        description="弹性预约实例类型，取值：NoEsi（默认）：非弹性预约实例。Esi：弹性预约实例。Segmented：弹性预约实例-时段型。说明：当参数InstanceChargeType取值为PostPaid时生效",
    )

    InstanceChargeType: Optional[str] = Field(
        default=None,
        description="资源的计费类型。取值：PostPaid：按量计费。PrePaid：包年包月。ReservedInstance：预留实例券",
    )

    InstanceTypeId: Optional[str] = Field(
        default=None,
        description="指定一个要查询的实例规格或专有宿主机规格"
    )

    SpotStrategy: Optional[str] = Field(
        default=None,
        description="按量计费的抢占式策略，取值：NoSpot（默认）：正常按量计费实例。SpotAsPriceGo：系统自动出价，跟随当前市场实际价格的抢占式实例。说明：当InstanceChargeType取值为PostPaid时，该参数生效",
    )

    VolumeType: Optional[str] = Field(
        default=None,
        description="指定一个要查询的云盘类型，取值：ESSD_PL0：极速型SSD PL0，ESSD_FlexPL：极速型SSD FlexPL",
    )

    ZoneId: Optional[str] = Field(
        default=None,
        description="可用区ID，您可以调用DescribeZones查询一个地域下的可用区信息。说明：默认为空，表示返回当前地域（RegionId）下的所有可用区中所有符合条件的资源，比如：cn-beijing-a",
    )


@register_tool(name="describe_instances",
               description="Query instance list",
               model_class=DescribeInstancesParams)
async def describe_instances(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client()
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_instances(
                volcenginesdkecs.DescribeInstancesRequest(
                    dedicated_host_cluster_id=args.get(
                        "DedicatedHostClusterId"),
                    dedicated_host_id=args.get("DedicatedHostId"),
                    deployment_set_group_numbers=args.get(
                        "DeploymentSetGroupNumbers"),
                    deployment_set_ids=args.get("DeploymentSetIds"),
                    eip_addresses=args.get("EipAddresses"),
                    hpc_cluster_id=args.get("HpcClusterId"),
                    instance_charge_type=args.get("InstanceChargeType"),
                    instance_ids=args.get("InstanceIds"),
                    instance_name=args.get("InstanceName"),
                    instance_type_families=args.get("InstanceTypeFamilies"),
                    instance_types=args.get("InstanceTypeIds"),
                    ipv6_addresses=args.get("Ipv6Addresses"),
                    key_pair_name=args.get("KeyPairName"),
                    max_results=args.get("MaxResults", 50),
                    primary_ip_address=args.get("PrimaryIpAddress"),
                    project_name=args.get("ProjectName"),
                    scheduled_instance_id=args.get("ScheduledInstanceId"),
                    status=args.get("Status"),
                    tag_filters=args.get("TagFilters"),
                    vpc_id=args.get("VpcId"),
                    zone_id=args.get("ZoneId"),
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "instances", None):
                return handle_error("describe_instances")

            total_results.extend(response.instances)

            if len(total_results) >= args.get("NeedNum") or not response.next_token:
                total_results = total_results[: args.get("NeedNum")]
                break

            next_token = response.next_token

        LOG.info(f"Total instances found: {len(total_results)}")
        return [types.TextContent(
            type="text",
            text=f"Results: {total_results}"
        )]

    except Exception as e:
        return handle_error("describe_instances", e)


@register_tool(name="describe_images",
               description="Query image list",
               model_class=DescribeImagesParams)
async def describe_images(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client()
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_images(
                volcenginesdkecs.DescribeImagesRequest(
                    image_ids=args.get("ImageIds"),
                    image_name=args.get("ImageName"),
                    instance_type_id=args.get("InstanceTypeId"),
                    is_lts=args.get("IsLTS"),
                    is_support_cloud_init=args.get("IsSupportCloudInit"),
                    os_type=args.get("OsType"),
                    platform=args.get("Platform"),
                    project_name=args.get("ProjectName"),
                    status=args.get("Status"),
                    tag_filters=args.get("TagFilters"),
                    visibility=args.get("Visibility"),
                    max_results=args.get("MaxResults", 50),
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "images", None):
                return handle_error("describe_images")

            total_results.extend(response.images)

            if len(total_results) >= args.get("NeedNum") or not response.next_token:
                total_results = total_results[: args.get("NeedNum")]
                break

            next_token = response.next_token

        LOG.info(f"Total images found: {len(total_results)}")
        return [types.TextContent(
            type="text",
            text=f"Results: {total_results}"
        )]

    except Exception as e:
        return handle_error("describe_images", e)


@register_tool(name="describe_instance_types",
               description="Query instance type list",
               model_class=DescribeInstanceTypesParams)
async def describe_instance_types(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client()
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_instance_types(
                volcenginesdkecs.DescribeInstanceTypesRequest(
                    image_id=args.get("ImageId"),
                    instance_type_ids=args.get("InstanceTypeIds"),
                    next_token=next_token,
                    max_results=args.get("MaxResults", 50),
                )
            )

            if not response or not getattr(response, "instance_types", None):
                return handle_error("describe_instance_types")

            total_results.extend(response.instance_types)

            if len(total_results) >= args.get("NeedNum") or not response.next_token:
                total_results = total_results[: args.get("NeedNum")]
                break

            next_token = response.next_token

        LOG.info(f"Total instance types found: {len(total_results)}")
        return [types.TextContent(
            type="text",
            text=f"Results: {total_results}"
        )]

    except Exception as e:
        return handle_error("describe_instance_types", e)


@register_tool(name="describe_available_resource",
               description="Query available zone resource",
               model_class=DescribeAvailableResourceParams)
async def describe_available_resource(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client()
        total_results = []

        response = volc_client.describe_available_resource(
            volcenginesdkecs.DescribeAvailableResourceRequest(
                destination_resource=args.get("DestinationResource"),
                elastic_scheduled_instance_type=args.get(
                    "ElasticScheduledInstanceType"),
                instance_charge_type=args.get("InstanceChargeType"),
                instance_type_id=args.get("InstanceTypeId"),
                spot_strategy=args.get("SpotStrategy"),
                volume_type=args.get("VolumeType"),
                zone_id=args.get("ZoneId"),
            )
        )

        if not response or not getattr(response, "available_zones", None):
            return handle_error("describe_available_resource")

        total_results.extend(response.available_zones)

        LOG.info(f"Total available zones found: {len(total_results)}")
        return [types.TextContent(
            type="text",
            text=f"Results: {total_results}"
        )]

    except Exception as e:
        return handle_error("describe_available_resource", e)
