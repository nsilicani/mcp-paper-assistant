import arxiv

from typing import Optional, Dict, Any, Union

from datetime import datetime, timezone
from dateutil import parser

from fastmcp.tools.tool import ToolResult
from fastmcp.exceptions import ToolError


def _is_within_date_range(
    date: datetime, start: datetime | None, end: datetime | None
) -> bool:
    """Check if a date falls within the specified range."""
    if start and not start.tzinfo:
        start = start.replace(tzinfo=timezone.utc)
    if end and not end.tzinfo:
        end = end.replace(tzinfo=timezone.utc)

    if start and date < start:
        return False
    if end and date > end:
        return False
    return True


def _process_paper(paper: arxiv.Result) -> Dict[str, Any]:
    """Process paper information with resource URI."""
    return {
        "id": paper.get_short_id(),
        "title": paper.title,
        "authors": [author.name for author in paper.authors],
        "abstract": paper.summary,
        "categories": paper.categories,
        "published": paper.published.strftime("%Y-%m-%d"),
        "url": paper.pdf_url,
        "resource_uri": f"arxiv://{paper.get_short_id()}",
    }

# See https://github.com/blazickjp/arxiv-mcp-server/blob/main/src/arxiv_mcp_server/tools/search.py#L60
async def search_paper(query: str, max_results: int, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Union[ToolResult, ToolError]:
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    results = []
    try:
        date_from = (
            parser.parse(date_from).replace(tzinfo=timezone.utc)
            if date_from is not None
            else None
        )
        date_to = (
            parser.parse(date_to).replace(tzinfo=timezone.utc)
            if date_to is not None
            else None
        )
    except (ValueError, TypeError) as e:
        return ToolError(e)
    
    for paper in client.results(search):
        if _is_within_date_range(paper.published, date_from, date_to):
            results.append(_process_paper(paper))

        if len(results) >= max_results:
            break

    response_data = {"total_results": len(results), "papers": results}

    return ToolResult(structured_content=response_data)
