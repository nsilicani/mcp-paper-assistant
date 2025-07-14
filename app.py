import streamlit as st
import asyncio
import json

# from datetime import datetime
# from fastmcp import Client
from mcp_paper_assistant.client.client import McpClient
from mcp_paper_assistant.settings import ServerSettings


# Helper for Streamlit to run async code
def run_async(func, *args, **kwargs):
    return asyncio.run(func(*args, **kwargs))


def main():
    st.set_page_config(page_title="🧠 ArXiv Assistant", layout="wide")
    st.title("📚 ArXiv Paper Search Assistant")

    st.markdown(
        "Enter a research question or query in natural language. Example: *Are there any recent papers on quantum computing in the last year?*"
    )

    user_query = st.text_input(
        "Your query",
        placeholder="e.g., Provide 5 papers on diffusion models in computer vision",
    )
    # openai_api_key = st.text_input("OpenAI API Key", type="password")

    if st.button("Search") and user_query:
        with st.spinner("Processing your query..."):
            server_config = ServerSettings()
            mcp_client = McpClient(server_config)
            search_args = run_async(
                mcp_client.call_tool,
                "extract-user-args",
                {"user_query": user_query},
            )

            if search_args.structured_content is not None:
                st.success(
                    f"Extracted arguments: `{search_args.structured_content}`"
                )
                result = run_async(
                    mcp_client.call_tool,
                    "search-tool",
                    search_args.structured_content,
                )

                if hasattr(result, "structured_content"):
                    papers = result.structured_content.get("papers", [])
                    st.subheader(f"📄 Found {len(papers)} papers")
                    for paper in papers:
                        st.markdown(f"### [{paper['title']}]({paper['url']})")
                        st.markdown(
                            f"**Authors:** {', '.join(paper['authors'])}"
                        )
                        st.markdown(f"**Published:** {paper['published']}")
                        st.markdown(
                            f"**Categories:** {', '.join(paper['categories'])}"
                        )
                        st.markdown(f"**Abstract:** {paper['abstract']}")
                        st.markdown("---")
                else:
                    st.error(f"Error: {result}")
            else:
                st.warning(
                    f"Could not extract search arguments from the query. {search_args=}"
                )


if __name__ == "__main__":
    main()
