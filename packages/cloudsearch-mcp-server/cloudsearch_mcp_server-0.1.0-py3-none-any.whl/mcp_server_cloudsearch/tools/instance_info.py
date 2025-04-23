import volcenginesdkescloud
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from mcp_server_cloudsearch.client import create_cloudsearch_client


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def cloudsearch_describe_instance(region_id: str, instance_id: str):
        """
        查询云搜索服务在指定区域下的实例详细信息，包括实例 id、名称、版本、状态、创建时间、计费类型、规格配置、标签列表、网络配置、数据迁移等信息。

        :param region_id: 区域 id
        :param instance_id: 实例 id
        :return: 实例详细信息
        """
        try:
            client = create_cloudsearch_client(region_id)
            response = client.describe_instance(
                volcenginesdkescloud.DescribeInstanceRequest(instance_id=instance_id)
            )
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool()
    async def cloudsearch_describe_instances(region_id: str, zone_id=None, instance_id=None, instance_name=None,
                                 status=None, version=None, charge_type=None, project_name=None,
                                 page_number=1, page_size=10):
        """
        查询云搜索服务在指定区域下的实例列表，包括每个实例的详细信息。

        :param region_id: 区域 id
        :param zone_id: 可用区 id，支持模糊查询
        :param instance_id: 实例 id，支持模糊查询
        :param instance_name: 实例名称，支持模糊查询
        :param status: 实例状态
        :param version: 实例版本
        :param charge_type: 实例计费类型
        :param project_name: 项目名称
        :param page_number: 分页页码
        :param page_size: 分页大小
        :return: 实例列表
        """
        try:
            filters = []
            if zone_id:
                filters.append(
                    volcenginesdkescloud.FilterForDescribeInstancesInput(name="ZoneId", values=[zone_id])
                )
            if instance_id:
                filters.append(
                    volcenginesdkescloud.FilterForDescribeInstancesInput(name="InstanceId", values=[instance_id])
                )
            if instance_name:
                filters.append(
                    volcenginesdkescloud.FilterForDescribeInstancesInput(name="InstanceName", values=[instance_name])
                )
            if status:
                filters.append(
                    volcenginesdkescloud.FilterForDescribeInstancesInput(name="Status", values=[status])
                )
            if version:
                filters.append(
                    volcenginesdkescloud.FilterForDescribeInstancesInput(name="Version", values=[version])
                )
            if charge_type:
                filters.append(
                    volcenginesdkescloud.FilterForDescribeInstancesInput(name="ChargeType", values=[charge_type])
                )

            client = create_cloudsearch_client(region_id)
            response = client.describe_instances(volcenginesdkescloud.DescribeInstancesRequest(
                filters=filters,
                project_name=project_name,
                page_number=page_number,
                page_size=page_size))
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool()
    async def cloudsearch_describe_instance_nodes(region_id: str, instance_id: str):
        """
        查询云搜索服务在指定区域下的实例节点列表，包括每个节点的名称、类型、状态、存储配置、规格配置、重启次数等信息。

        :param region_id: 区域 id
        :param instance_id: 实例 id
        :return: 实例节点列表
        """
        try:
            client = create_cloudsearch_client(region_id)
            response = client.describe_instance_nodes(
                volcenginesdkescloud.DescribeInstanceNodesRequest(instance_id=instance_id)
            )
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool()
    async def cloudsearch_describe_instance_plugins(region_id: str, instance_id: str):
        """
        查询云搜索服务在指定区域下的实例的插件列表，包括每个插件的名称、版本、状态、描述等信息。

        :param region_id: 区域 id
        :param instance_id: 实例 id
        :return: 实例插件列表
        """
        try:
            client = create_cloudsearch_client(region_id)
            response = client.describe_instance_plugins(
                volcenginesdkescloud.DescribeInstancePluginsRequest(instance_id=instance_id)
            )
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")