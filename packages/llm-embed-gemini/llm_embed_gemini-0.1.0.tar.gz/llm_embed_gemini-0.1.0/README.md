# llm-embed-gemini

[![PyPI](https://img.shields.io/pypi/v/llm-embed-gemini.svg)](https://pypi.org/project/llm-embed-gemini/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-embed-gemini?include_prereleases&label=changelog)](https://github.com/simonw/llm-embed-gemini/releases)
[![Tests](https://github.com/simonw/llm-embed-gemini/workflows/Test/badge.svg)](https://github.com/simonw/llm-embed-gemini/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-embed-gemini/blob/main/LICENSE)

[MARCH 7, 2025: State-of-the-art text embedding via the Gemini API](https://developers.googleblog.com/en/gemini-embedding-text-model-now-available-gemini-api/)

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

    llm install llm-embed-gemini

## Usage

To get started embedding a single string, run the following:

```bash
export GEMINI_API_KEY=xxxx
llm embed -m gemini-embedding-exp-03-07 -c 'Hello world'
```

This plugin adds support for three new embedding models:

* gemini-embedding-exp-03-07
* text-embedding-004
* embedding-001

See [the LLM documentation](https://llm.datasette.io/en/stable/embeddings/index.html) for everything you can do.


