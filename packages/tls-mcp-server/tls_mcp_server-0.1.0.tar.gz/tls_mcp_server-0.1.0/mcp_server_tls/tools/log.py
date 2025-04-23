import time
import logging

from typing import Optional
from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.log import search_logs_v2_resource
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)

async def search_logs_v2_tool(
        query: str,
        topic_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = 10
) -> dict:
    """Search logs using the provided query from the TLS service.

    This tool allows you to search logs using various query types including full text search,
    key-value search, and SQL analysis. It provides flexible time range filtering and
    limit options to customize your search results.

    Args:
        query: Search query string. Supports three formats:
            - Full text search: e.g., "error"
            - Key-value search: e.g., "key1:error"
            - SQL analysis: e.g., "* | select count(*) as count"
        topic_id: Optional topic ID to search logs from. If not provided, uses the globally configured topic.
        limit: Maximum number of logs to return (default: 100)
        start_time: Start time in milliseconds since epoch (default: 15 minutes ago)
        end_time: End time in milliseconds since epoch (default: current time)

    Returns:
        List of log entries matching the search criteria. Each log entry is a dictionary
        containing the log data, timestamp, and other metadata.

    Examples:
        # Search for error logs
        search_logs("error")

        # Search for logs with a specific key-value
        search_logs("status_code:500")

        # Perform SQL analysis
        search_logs("* | select count(*) as count group by status_code")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not query:
            raise ValueError("query is required")

        if end_time is None:
            end_time = int(time.time() * 1000)

        if start_time is None:
            start_time = end_time - ( 15 * 60 * 1000 )

        topic_id = TLS_CONFIG.topic_id or topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await search_logs_v2_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            query=query,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    except Exception as e:
        logger.error("call tool error: search_logs_v2_tool, err is {}".format(str(e)))
        return {"error": str(e)}