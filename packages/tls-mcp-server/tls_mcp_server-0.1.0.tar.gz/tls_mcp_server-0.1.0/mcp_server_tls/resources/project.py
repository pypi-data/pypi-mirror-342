import logging
from typing import Optional

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import DescribeProjectRequest, DescribeProjectsRequest
from volcengine.tls.tls_responses import DescribeProjectResponse, DescribeProjectsResponse

from mcp_server_tls.reqeust import get_sdk_client

logger = logging.getLogger(__name__)

async def describe_project_resource(
        auth_info: dict,
        project_id: str,
) -> dict:
    """describe_project resource
    """
    try:
        reqeust: DescribeProjectRequest = DescribeProjectRequest(
            project_id=project_id,
        )

        result: DescribeProjectResponse = get_sdk_client(auth_info).describe_project(reqeust)

        return vars(result.get_project())

    except TLSException as e:
        logger.error("describe_project_resource error")
        raise e

async def describe_projects_resource(
        auth_info: dict,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 10,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
        is_full_name: Optional[bool] = False,
        iam_project_name: Optional[str] = None,
) -> dict:
    """describe_projects resource
    """
    try:
        request: DescribeProjectsRequest = DescribeProjectsRequest(
            page_number=page_number,
            page_size=page_size,
            is_full_name=is_full_name,
            project_id=project_id,
            project_name=project_name,
            iam_project_name=iam_project_name,
        )

        result: DescribeProjectsResponse =  get_sdk_client(auth_info).describe_projects(request)

        return {
            "total": result.get_total(),
            "projects": [vars(project_info) for project_info in result.get_projects()]
        }

    except TLSException as e:
        logger.error("describe_projects_resource error")
        raise e