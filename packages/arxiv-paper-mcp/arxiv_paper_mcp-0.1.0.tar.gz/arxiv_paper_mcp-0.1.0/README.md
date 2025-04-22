# 🧠 arXiv Research Assistant MCP Server

This project is an MCP (Model Context Protocol) server built to interact with the vast arXiv.org paper database.

It allows clients like **Claude AI** to search, explore, and compare arXiv papers efficiently — all through a custom-built, local server. It’s built with **Python** and the **FastMCP** framework, and uses **uv** for lightweight package management.

---
S
## ✨ Features

- **🔍 Keyword-based Paper Search**  
  Search arXiv papers by keywords, with options to sort by relevance or most recent.

- **📚 Latest Papers by Category**  
  Specify an arXiv category code (e.g., `cs.AI`, `math.AP`) to fetch the most recent papers in that field.

- **📄 Paper Details Lookup**  
  Fetch detailed metadata using a paper's arXiv ID: title, authors, abstract, categories, DOI, PDF link, and more.

- **🧑‍🔬 Author-based Paper Search**  
  Retrieve a list of papers published by a specific author.

- **📊 Trend Analysis (Experimental)**  
  Get an overview of trending keywords or topics based on recent papers in a category (currently uses mock data).

- **📝 Summarization Prompt Generator**  
  Dynamically generate prompts that help LLMs summarize a selected paper more effectively.

- **🆚 Comparison Prompt Generator**  
  Provide two paper IDs to generate a structured prompt for comparing their content.

---

## 🛠️ Tech Stack

- Python 3.11+
- [FastMCP](https://github.com/modelcontextprotocol/fastmcp)
- uv (for dependency & environment management)
- requests (for API communication)
- xml.etree.ElementTree (for parsing XML responses)

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/daheepk/arxiv-mcp-server.git
cd mcp-server-demo
```
### 🔧 2. Install Dependencies

Use `uv` to install all dependencies in editable mode:

```bash
uv pip install -e .
```

## ⚙️ How to Run

### ▶️ Run the server (locally)

You can start the server in two ways:

```bash
uv run python -m server
or using the project script defined in pyproject.toml:
```

```bash
uv run arxiv-mcp
```

## Project Structure
```
mcp-server-demo/
├── server.py               # Entry point
├── arxiv_mcp/              # Main package
│   ├── __init__.py
│   ├── app.py              # FastMCP app setup
│   ├── utils.py            # arXiv API communication logic
│   ├── resources/          # MCP resources (categories, authors, etc.)
│   ├── tools/              # MCP tools (search, detail lookup, trends)
│   └── prompts/            # Prompt templates (summarize, compare)
├── pyproject.toml          # Project config & dependencies
└── README.md               # This file
```
