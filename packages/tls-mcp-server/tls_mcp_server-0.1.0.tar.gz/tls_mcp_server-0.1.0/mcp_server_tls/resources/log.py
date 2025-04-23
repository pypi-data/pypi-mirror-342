import logging
from typing import Optional

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import SearchLogsRequest
from volcengine.tls.tls_responses import SearchLogsResponse
from mcp_server_tls.reqeust import get_sdk_client

logger = logging.getLogger(__name__)

async def search_logs_v2_resource(
        auth_info: dict,
        topic_id: str,
        query: str,
        start_time: int,
        end_time: int,
        limit: int,
        context: Optional[str] = None,
        sort: Optional[str] = "DESC",
) -> dict:
    try:
        request: SearchLogsRequest = SearchLogsRequest(
            topic_id=topic_id,
            query=query,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            context=context,
            sort=sort,
        )

        response: SearchLogsResponse = get_sdk_client(auth_info).search_logs_v2(request)

        search_result = response.get_search_result()
        search_result.analysis_result = vars(search_result.analysis_result)
        result =  vars(search_result)
        # Remove useless fields
        result.pop("HitCount", None)
        return result

    except TLSException as e:
        logger.error("search_logs_v2_resource error")
        raise e
