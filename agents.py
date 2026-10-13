
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()


# Shared Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash",
    temperature=0.2,
    max_output_tokens=1200,
    max_retries=1,
    timeout=45,
)


# --------------------------------------------------
# AGENT 1: SEARCH AGENT
# --------------------------------------------------

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a professional research search agent.

        Your task is to find recent, relevant and reliable
        information about the user's research topic.

        Instructions:
        1. Use the web_search tool to find relevant sources.
        2. Return 3-5 useful sources whenever available.
        3. Prefer official websites, reputable news outlets,
           research papers and established publications.
        4. For every source, provide:
           - Article title
           - Complete URL
           - Publication date, if available
           - A short summary of its relevance
        5. Prioritize recent sources for current-news queries.
        6. Do not invent sources, dates or URLs.
        7. Return concise Markdown, not raw API metadata.
        8. If search fails, clearly explain the limitation.

        Keep your response concise and factual.
        """
    )


# --------------------------------------------------
# AGENT 2: READER / WEB SCRAPING AGENT
# --------------------------------------------------

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
        You are a research reading and web extraction agent.

        Your task is to extract useful information from
        URLs supplied in the user's message.

        Instructions:
        1. Identify the most relevant source URL.
        2. Use the scrape_url tool to retrieve its content.
        3. If a website returns 403, fails, or contains no
           useful content, try another supplied URL when
           available.
        4. Extract important facts, dates, names, events,
           statistics and relevant context.
        5. Prefer the original article over a search snippet.
        6. Preserve the source URL for citation.
        7. Never invent facts or pretend a page was scraped
           successfully when it was not.
        8. If all attempts fail, clearly state that.

        Output format:
        Source URL:
        Article Title:
        Key Findings:
        - Finding 1
        - Finding 2
        - Finding 3

        Brief Summary:

        Keep the output concise and useful for report writing.
        """
    )


# --------------------------------------------------
# AGENT 3: RESEARCH WRITER
# --------------------------------------------------

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert research writer.

        Produce a clear, structured, factual and professional
        report using the supplied research.

        Rules:
        - Use only information supported by the research.
        - Distinguish verified facts from claims and opinions.
        - For current news, include dates when available.
        - Avoid repetition and unsupported conclusions.
        - Do not invent sources, quotations or statistics.
        - If the research is incomplete, acknowledge it.
        - Include source URLs next to relevant findings when
          the supplied information supports them.
        """
    ),
    (
        "human",
        """
        Write a research report on the following topic.

        Topic:
        {topic}

        Research Gathered:
        {research}

        Use this structure:

        1. Title
        2. Introduction
        3. Key Findings
           - Include at least 3 well-explained findings
             when the available evidence supports them.
           - Include relevant dates and source attribution.
        4. Analysis and Implications
        5. Conclusion
        6. Sources
           - List the actual URLs provided in the research.

        Target length: approximately 500-700 words.

        If insufficient evidence is available, write a shorter
        report rather than filling it with speculation.

        Return the complete report in Markdown.
        """
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# --------------------------------------------------
# AGENT 4: CRITIC / QUALITY REVIEWER
# --------------------------------------------------

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a strict but constructive research quality
        reviewer.

        Evaluate the report based on:
        1. Factual accuracy and support from the research
        2. Relevance to the requested topic
        3. Quality and diversity of sources
        4. Completeness and depth
        5. Structure, clarity and readability
        6. Proper use of dates and source URLs

        Do not assume that unsupported claims are true.
        Do not reward length alone.
        Do not claim to have independently verified sources
        unless verification actually occurred.
        """
    ),
    (
        "human",
        """
        Review the following research report.

        Report:
        {report}

        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...

        Areas to Improve:
        - ...

        Missing Information:
        - ...

        One-line Verdict:
        ...
        """
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()
