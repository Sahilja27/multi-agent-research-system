# 🔬 Multi-Agent AI Research System

An AI-powered research automation system that uses multiple specialized agents to search the web, extract relevant information, generate structured research reports, and evaluate the final output.

Built with **Python, LangChain, Google Gemini, and You.com Search API**, this project demonstrates how multiple AI agents can collaborate to automate the research workflow.

## ✨ Features

- 🔎 **AI-Powered Web Search** — Finds recent and relevant sources for a given research topic.
- 📄 **Web Content Extraction** — Selects a relevant source and extracts useful information.
- ✍️ **Automated Report Generation** — Generates a research report using an LLM-powered writer.
- 🧐 **AI Critic and Review** — Reviews the generated report and provides feedback.
- 🔗 **Multi-Agent Workflow** — Connects specialized agents into a sequential research pipeline.
- 🖥️ **Streamlit UI** — Includes a web interface for submitting research topics and viewing results.
- 📥 **Markdown Export** — Allows the final research report to be downloaded as a Markdown file.
- 🔐 **Environment-Based API Keys** — Uses environment variables to keep API credentials out of the source code.

## 🏗️ System Architecture

The research pipeline consists of four main stages:

```text
          Research Topic
                |
                v
        +----------------+
        |  Search Agent  |
        | Find Sources   |
        +----------------+
                |
                v
        +----------------+
        |  Reader Agent  |
        | Extract Content|
        +----------------+
                |
                v
        +----------------+
        |  Writer Chain  |
        | Generate Report|
        +----------------+
                |
                v
        +----------------+
        |  Critic Chain  |
        | Review Report  |
        +----------------+
                |
                v
       Final Report & Feedback
```

### Workflow

1. **Search Agent:** Searches for relevant sources related to the user's research topic.
2. **Reader Agent:** Selects a relevant URL and retrieves useful information from the source.
3. **Writer Chain:** Combines the search results and extracted content to produce a research report.
4. **Critic Chain:** Reviews the generated report and provides feedback.

The Streamlit interface calls the existing `run_research_pipeline(topic)` function, keeping the research logic separate from the UI.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | Agent orchestration and LLM integration |
| Google Gemini | Language model for research and generation |
| You.com Search API | Web search |
| Beautiful Soup | HTML parsing and web scraping utilities |
| Streamlit | Interactive web interface |
| python-dotenv | Environment variable management |

## 📂 Project Structure

```text
multi-agent-research-system/
│
├── agents.py             # Agent and chain definitions
├── pipeline.py           # Main research pipeline
├── app.py                # Streamlit web interface
├── .env                  # API credentials (not committed)
├── .env.example          # Example environment configuration
├── .gitignore            # Excludes secrets and local files
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

Your actual project may contain additional files or directories depending on your implementation.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-research-system.git
cd multi-agent-research-system
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
YDC_API_KEY=your_youcom_api_key
```

Use the exact environment variable names expected by your existing code. If your implementation uses different names, update this example accordingly.

**Important:** Never commit your real `.env` file or expose API keys in source code.

### 5. Run the research pipeline in the terminal

```bash
python pipeline.py
```

Enter a research topic when prompted.

### 6. Launch the Streamlit interface

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 🖥️ Using the Application

1. Launch the Streamlit application.
2. Enter a research topic.
3. Click **Start Research**.
4. Wait for the research pipeline to finish.
5. Explore the results in the separate tabs:
   - Search Results
   - Scraped Content
   - Final Report
   - Critic Feedback
6. Download the final report as a Markdown file.

## 🔐 Security

- API keys are loaded through environment variables.
- `.env` should be excluded using `.gitignore`.
- `.env.example` contains placeholders only.
- The virtual environment should not be committed to GitHub.
- If an API key is accidentally published, revoke or rotate it immediately.

## 🚀 Future Improvements

Potential extensions for the project include:

- Real-time progress indicators for individual agents.
- Support for multiple source URLs and cross-source analysis.
- Citation verification and source reliability scoring.
- Research history and report management.
- Persistent storage for previous research tasks.
- Improved error handling and retry mechanisms.
- Deployment to a cloud hosting platform.
- More detailed report evaluation and quality metrics.

These are potential future enhancements and are not necessarily implemented in the current version.

## 🎯 Project Objective

The goal of this project is to explore how AI agents can work together to automate research tasks, reduce manual information gathering, and generate structured reports through a modular, reusable workflow.

## 👨‍💻 Author

**Sahil Jadhav**

GitHub: [YOUR_GITHUB_USERNAME](https://github.com/YOUR_GITHUB_USERNAME)

---

⭐ If you find this project interesting, consider giving the repository a star.
