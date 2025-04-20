# Tokenizer
A Zig library for tokenizing text using PCRE2 regular expressions - now also available as a Python package via `pip`.

## Requirement
zig v0.13.0

## Install
```bash
git clone https://github.com/jaco-bro/tokenizer
cd tokenizer
zig build exe --release=fast
```

## Usage
- `zig-out/bin/tokenizer_exe [--model MODEL_NAME] COMMAND INPUT` 
- `zig build run -- [--model MODEL_NAME] COMMAND INPUT` 

```bash
zig build run -- --encode "hello world"
zig build run -- --decode "{14990, 1879}"
zig build run -- --model "phi-4-4bit" --encode "hello world"
zig build run -- --model "phi-4-4bit" --decode "15339 1917"
```

## Python (optional)
Tokenizer is also pip-installable for use from Python:
```bash
pip install tokenizerz
```

Usage:
```python
import tokenizerz

tokenizer = tokenizerz.Tokenizer
tokens = tokenizer.encode("Hello, world!")
print(tokens)
```

