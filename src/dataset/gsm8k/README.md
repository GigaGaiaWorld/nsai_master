---
license: mit
task_categories:
- question-answering
language:
- en
tags:
- code
size_categories:
- 1K<n<10K
source_datasets:
- gsm8k (https://huggingface.co/datasets/gsm8k)
---

# Dataset Card for GSM8K-Prolog

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
- [Additional Information](#additional-information)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Repository:** https://github.com/yxc-cyber/ProPer
- **Paper:** https://aclanthology.org/2024.naacl-short.61

### Dataset Summary
This is the Prolog annotated version of the [GSM8K math reasoning dataset](https://huggingface.co/datasets/gsm8k).
We used the same dataset splits and questions in GSM8K and prompted GPT-4 to generate the Prolog programs to solve the questions.
We then manually corrected some malfunctioning samples.

### Supported Tasks and Leaderboards

This dataset can be used to train language models to generate Prolog codes in order to solve math questions and evaluate the performance.

### Languages

The instructions and inputs in the dataset are in English. The outputs are in Prolog.

## Dataset Structure

### Data Instances

Each instance contains a string to instruct the model, a string for the grade-school level math question, and a string for a Prolog program which solves the question.

```python
{
    "instruction": "Please generate a piece of Prolog code to solve the given math problem.",
    "input": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
    "output": ":- use_module(library(clpq)).\n\nsell_clips(natalia, april, 48).\n\nsolve(Total_amount) :-\n    sell_clips(natalia, april, April_amount),\n    {May_amount = April_amount / 2},\n    {Total_amount = May_amount + April_amount}."
}
```

### Data Fields

The GSM8K-Prolog dataset follows the instruction prompt used in [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca).
The data fields are the same among `train` and `test` splits.

- instruction: The task the model should perform. All the instructions in this dataset are the same because the only task here is to use Prolog to solve math questions.

- input: The question to a grade school math problem.

- output: The Prolog program which solves the math question.


### Data Splits

| name   |train|validation|
|--------|----:|---------:|
|main    | 7473|      1319|

## Additional Information

### Licensing Information

The GSM8K-Prolog dataset is licensed under the [MIT License](https://opensource.org/licenses/MIT).

### Citation Information

Xiaocheng Yang, Bingsen Chen, and Yik-Cheung Tam. 2024. Arithmetic Reasoning with LLM: Prolog Generation & Permutation. In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 2: Short Papers), pages 699–710, Mexico City, Mexico. Association for Computational Linguistics.