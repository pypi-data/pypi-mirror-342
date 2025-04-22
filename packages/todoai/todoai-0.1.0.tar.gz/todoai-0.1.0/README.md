# taskAI

taskAI is a simple Python library that allows you to summarize YouTube videos using Gemini models via LangChain.

## Install
```bash
pip install taskai

from taskAI import setup, summarize_youtube

setup("YOUR_API_KEY")
summary = summarize_youtube("https://youtu.be/xyz", summary_type="bullet")
print(summary)
```
