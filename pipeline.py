
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


def extract_text(result):
    """Extract readable text without printing metadata or signatures."""
    content = result["messages"][-1].content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)

        return "\n".join(parts)

    return str(content)


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # STEP 1: SEARCH AGENT
    print("\n" + "=" * 50, flush=True)
    print("STEP 1: Search agent is working...", flush=True)
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find 3 recent, reliable sources about: {topic}. "
                "Return each source's title, URL, and a short summary. "
                "Keep the response concise."
            )
        ]
    })

    state["search_results"] = extract_text(search_result)

    print("\nSearch results:")
    print(state["search_results"][:1500])

    # STEP 2: READER AGENT
    print("\n" + "=" * 50, flush=True)
    print("STEP 2: Reader agent is scraping sources...", flush=True)
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Research topic: {topic}\n\n"
                "Select the single most relevant URL from these results. "
                "Scrape that page using your available tools. "
                "Return the URL, key facts, and a concise summary. "
                "If scraping fails, explain why.\n\n"
                f"Search results:\n{state['search_results'][:2500]}"
            )
        ]
    })

    state["scraped_content"] = extract_text(reader_result)

    print("\nScraped content:")
    print(state["scraped_content"][:1500])

    # STEP 3: WRITER
    print("\n" + "=" * 50, flush=True)
    print("STEP 3: Writer is drafting the report...", flush=True)
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results'][:2500]}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content'][:4000]}"
    )

    report = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    # Support chains that return either text or message-like objects.
    if hasattr(report, "content"):
        report = report.content

    state["report"] = report

    print("\nFinal report:")
    print(state["report"])

    # STEP 4: CRITIC
    print("\n" + "=" * 50, flush=True)
    print("STEP 4: Critic is reviewing the report...", flush=True)
    print("=" * 50)

    feedback = critic_chain.invoke({
        "report": state["report"]
    })

    if hasattr(feedback, "content"):
        feedback = feedback.content

    state["feedback"] = feedback

    print("\nCritic feedback:")
    print(state["feedback"])

    print("\nResearch pipeline completed!", flush=True)

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ").strip()

    if topic:
        run_research_pipeline(topic)
    else:
        print("Please enter a research topic.")
