# FastMCP Expense Tracker local Server

A demonstration MCP server for expense management built with FastMCP (Model Context Protocol). This server provides tools and resources for tracking, categorizing, and managing personal or business expenses.

## Demo

Here's a demo video showing the FastMCP server in action:
![demo_mcp-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/d869d80a-824a-4b5d-943f-13c37b46f6b6)


## Installation

```bash
pip install uv
uv init .

uv sync
```

## Usage

We are using [FASTMCP](https://github.com/jlowin/fastmcp) server for creating the server.

To test the server and its feature
```bash
uv run fastmcp dev main.py
```

To install the server with your Host(llm--> Claude-desktop, ChatGPT, Gemini)

```bash
uv run fastmcp install claude-desktop main.py
```

## Features

### Core Functionality
- **Expense Tracking**: Add, update, and delete expense records
- **Category Management**: Organize expenses by custom categories  
- **Reporting**: Generate expense reports and summaries
- **Data Persistence**: Store expense data with proper validation
- **Real-time Updates**: Instant synchronization of expense changes

### Visual Dashboard
You can also visually track the expenses on expense board created using [Streamlit](https://streamlit.io/)

To run the streamlit host;
```bash
uv run streamlit run viz.py
```

![viz image](viz//demo_viz.png)

## Contact

For questions, suggestions, or support, feel free to reach out:

- **GitHub**: [Open an issue](https://github.com/yourusername/fastmcp-demo-server/issues)
- **Email**: kagadevishal@gmail.com
