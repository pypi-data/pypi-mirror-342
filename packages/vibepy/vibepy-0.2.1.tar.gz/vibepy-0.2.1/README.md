# Vibepy

Talking to and running codes from open-ai.

## Installation

```bash
pip install vibepy
```
Or if use uv  

```bash
uv  pip install --no-cache vibepy==0.1.7
```

## Usage

Have OPENAI_API_KEYS as one of your environment variables.  

1. Start the vibepy CLI, and have conversation with open-ai

    Default gpt-4o-mini

```bash
vibepy
```
2. Specify model

```bash
vibepy --model gpt-4.1-mini
```

3. automatically run the returned code blocks:  

```bash
vibepy -e
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"
```

## License

MIT License
