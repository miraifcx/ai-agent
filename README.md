# AI Agent

A command-line AI coding agent built with Python and the OpenAI API (via OpenRouter). It takes a user prompt and uses tool-calling to interact with the local filesystem — listing files, reading content, running Python scripts, and writing files.

> **⚠️ Warning:** This project is a learning/personal tool and is **not intended for production use**.

## Features

- **File listing** — browse directories and inspect file metadata
- **File reading** — read the contents of any file in the working directory
- **Python execution** — run `.py` scripts with optional arguments
- **File writing** — create or overwrite files
- **Agentic loop** — the model can chain multiple tool calls before producing a final answer

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (latest version)

## Usage

Install dependencies:

```bash
uv sync
```

Then run the agent:

```bash
python main.py "your prompt here"
```

Add `--verbose` to see token usage and full function-call arguments:

```bash
python main.py --verbose "your prompt here"
```

## Configuration

Before running the agent, you **must** set `WORKING_DIR` in `config.py` to the directory you want the agent to operate on. All file operations (read, write, list, execute) are scoped to this path.

| Variable | File | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | `.env` | API key for OpenRouter |
| `WORKING_DIR` | `config.py` | **Required.** Absolute or relative path to the target working directory |
| `MAXITER` | `config.py` | Max tool-call iterations before the agent stops (default: 10) |
| `MAX_CHARS` | `config.py` | Character limit for file content reads (default: 10 000) |

The default API aggregator is [OpenRouter](https://openrouter.ai) and the default model is `openai/gpt-oss-20b:free`. You are free to change both the `base_url` and `model` inside `main.py` to use any compatible provider or model.

---

*A Boot.dev project*
