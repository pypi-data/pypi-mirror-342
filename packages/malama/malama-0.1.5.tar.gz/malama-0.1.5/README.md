# 📚 Malama PDFMAN

**Malama PDFMAN** is a flexible and extensible framework for querying content from PDF files using various large language models (LLMs) like OpenAI, Gemini, Claude, Mistral, LLaMA, DeepSeek, and more.

> 🔍 Upload a PDF → Load context → Ask questions → Get intelligent answers from the LLM of your choice.

---

## ✨ Features

- ✅ Extracts context from PDFs (fully or within specified page ranges)
- 🤖 Supports multiple LLMs via simple abstraction
- 🔌 Easily pluggable support for new AI providers
- 🧠 Unified prompt structure and clean output handling
- ⚙️ Minimal external dependencies

---

## 🏗️ Supported Models

| Provider          | Model Examples                        |
|-------------------|---------------------------------------|
| **OpenAI**        | `gpt-3.5-turbo`                       |
| **Gemini**        | `gemini-1.5-pro-002`                  |
| **Anthropic**     | `claude-3-7-sonnet-20250219`          |
| **Groq**          | `compound-beta-mini`,`llama3-70b-8192`|
| **Mistral**       | `mistral-medium`                      |
| **Cohere**        | `command-r-plus`                      |
| **DeepSeek**      | `deepseek-ai/DeepSeek-R1`             |
| **Together.ai**   | `Qwen/Qwen2-72B-Instruct`             |
| **Together.ai**   | Coming Soon - Falcon                  |
| **Amazon Titan**  | Coming Soon (via Boto3)               |

---

## 📦 Installation

```bash
pip install malama
