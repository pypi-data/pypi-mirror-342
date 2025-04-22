# aiszrhk

**aiszrhk.llm4data** is a lightweight and customizable API wrapper designed to assist data analysts by leveraging the power of large language models (LLMs).

---

## Features

- Modular utility functions for LLM interaction
- Customizable for data analysis workflows
- Designed with namespace package structure

---

## Usage

### 1. Import
```python
from aiszrhk.llm4data import utils
```

### 2. Extra & Run code 
```python
utils.extract_and_optionally_run_code(response: str, level: int = 0)
```
- To simplify the process of extra generated code during the process, we've built in with code automate detect function. Once llm output with code block inside, the terminal will automatically display extracted code and ask user if to execute or not.

### 3. Placeholder inserter
```python
utils.extract_options_and_insert_into_placeholders(response: str, placeholders: dict, input_file: str, level: int = 0)
```
- We also provide a placeholder inserter. For step(s) you want to insert output options into reserved placeholder field, you may fill the corresponded "system_prompt" field with following sentence: "You're a multiple choice generator. You must provide the output with format:'[A].... [B]...' and continue with C, D, and etc. only." Thus, you will be able to trigger the multiple choice detetor function.
