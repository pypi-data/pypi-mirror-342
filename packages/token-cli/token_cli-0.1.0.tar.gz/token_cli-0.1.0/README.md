<h1 align="center">Token CLI</h1>

<p align="center">A command-line tool to visualize tokenized text using different encodings.</p>

![Demo](demo.gif)

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/taha-yassine/token-cli.git
    cd token-cli
    ```
2.  Install dependencies (preferably in a virtual environment):
    ```bash
    # Using pip
    python -m venv .venv
    source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
    pip install -r requirements.txt

    # Or using uv
    uv venv
    uv pip install -r requirements.txt
    ```

## Usage

```bash
python main.py [OPTIONS] [INPUT_FILE]
```

**From standard input:**

```bash
echo "This is sample text." | python main.py --hide-stats
```

**From a file:**

```bash
python main.py --tokenizer gpt-4 your_text_file.txt
```

**Interactive Preview:**

Use the `-p` or `--preview-files` flag to launch an interactive `fzf` session. This allows you to browse files in the current directory and its subdirectories, showing a live preview of the tokenization.

```bash
python main.py -p
# Or with a specific tokenizer/mode for the previews
python main.py --tokenizer cl100k_base --mode text -p
```

## Options

```
usage: main.py [-h] [--tokenizer TOKENIZER] [--mode {text,highlight}]
               [--hide-text] [--hide-stats] [--force-terminal] [-p]
               [input_file]

Visualize tokenized text.

positional arguments:
  input_file            Path to the input text file. Reads from stdin if not
                        provided.

options:
  -h, --help            show this help message and exit
  --tokenizer TOKENIZER
                        Tokenizer to use for tokenization. Possible values:
                        gpt-4o, o200k_base, cl100k_base, p50k_base, p50k_edit,
                        r50k_base, gpt2 (default: o200k_base)
  --mode {text,highlight}
                        Mode for displaying tokens: 'text' or 'highlight'.
                        (default: highlight)
  --hide-text           Hide the tokenized text.
  --hide-stats          Hide the token and character counts at the end.
  --force-terminal      Force terminal output.
  -p, --preview-files   Use fzf to preview tokenization of files in the
                        current directory.
```