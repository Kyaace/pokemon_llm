# Pokemon LLM Tokenizer Release Plan

## Objective
Transition the current custom Python tokenizer (`tokenizer.py`) into a native Hugging Face `tokenizers` configuration (`tokenizer.json`) before publicly releasing the model on the Hugging Face Hub or sharing it broadly with students.

## The Problem: `trust_remote_code=True`
Currently, our `tokenizer.py` is a heavily customized Python class designed to enforce a strict grammar using dictionary lookups and custom string processing (e.g. converting many-to-one synonyms like "hatchable" to "egg"). 

To share this tokenizer with others, we would normally have to upload `tokenizer.py` alongside the model and instruct users to run:
`AutoTokenizer.from_pretrained(..., trust_remote_code=True)`

**This is a massive cybersecurity risk.** 
`trust_remote_code=True` allows the `transformers` library to download arbitrary Python scripts from the internet and execute them on the user's machine using `exec()`. Malicious actors use this exact mechanism to distribute malware or steal environment variables. In an educational setting, teaching students to blindly accept remote code execution is a bad practice.

## The Solution: `WordLevel` + `Normalizer`
Hugging Face maintains a blazing-fast, sandboxed Rust backend library called `tokenizers`. We can construct our strict dictionary tokenizer entirely within this safe framework and export it as a pure data file (`tokenizer.json`).

### 1. The Core: WordLevel Model
The `WordLevel` model acts as a strict 1:1 mapping dictionary. It forces the tokenizer to translate exact word matches directly to their integer IDs, identical to our current dictionary approach.

### 2. The Secret Weapon: Normalizers
Because `WordLevel` strictly requires 1:1 mappings (for decoding purposes), we previously handled many-to-one synonyms (like `hatchable` -> `egg`) using messy Python logic. 
Instead, we will use a `Sequence` of `Replace` **Normalizers**. Normalizers intercept raw text *before* it hits the tokenizer and standardizes it. 

```python
# Conceptual Example
from tokenizers.normalizers import Sequence, Replace
tokenizer.normalizer = Sequence([
    Replace("hatchable", "egg"),
    Replace("breedable", "egg")
])
```

## Why this is the "Gold Standard"
1. **Cybersecurity First:** The `tokenizer.json` file is a purely declarative configuration file. It tells the Hugging Face Rust backend *how* to tokenize, meaning absolutely no remote Python execution is required. 
2. **Professionalism:** This methodology perfectly mirrors how production-grade models (LLaMA, GPT-4, Mistral) define their tokenization pipelines on the Hugging Face Hub.
3. **Performance:** Moving the tokenization math from Python into Hugging Face's pre-compiled Rust backend will yield a massive speedup when processing giant chat histories.
