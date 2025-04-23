import logging
from typing import Optional

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import DescribeTopicRequest, DescribeTopicsRequest
from volcengine.tls.tls_responses import DescribeTopicResponse, DescribeTopicsResponse

from mcp_server_tls.reqeust import get_sdk_client

logger = logging.getLogger(__name__)

async def describe_topic_resource(
        auth_info: dict,
        topic_id: str,
) -> dict:
    try:
        request: DescribeTopicRequest = DescribeTopicRequest(
            topic_id=topic_id,
        )

        result: DescribeTopicResponse = get_sdk_client(auth_info).describe_topic(request)

        return vars(result.get_topic())

    except TLSException as e:
        logger.error(f"Describe topic error: {e}")
        raise e

async def describe_topics_resource(
        auth_info: dict,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 10,
        project_name: Optional[str] = None,
        project_id: Optional[str] = None,
        topic_name: Optional[str] = None,
        topic_id: Optional[str] = None,
) -> dict:
    try:
        request: DescribeTopicsRequest = DescribeTopicsRequest(
            page_number=page_number,
            page_size=page_size,
            project_name=project_name,
            project_id=project_id,
            topic_name=topic_name,
            topic_id=topic_id,
        )

        result: DescribeTopicsResponse = get_sdk_client(auth_info).describe_topics(request)

        return {
            "total": result.get_total(),
            "topics": [vars(topic_info) for topic_info in result.get_topics()]
        }

    except TLSException as e:
        logger.error(f"Describe topics error: {e}")
        raise e