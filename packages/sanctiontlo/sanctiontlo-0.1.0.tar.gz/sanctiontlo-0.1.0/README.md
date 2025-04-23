# SanctionTLO CLI

A command-line interface for TLO searches.

## Installation

```bash
pip install sanctiontlo
```

## Configuration

First, configure your admin key:

```bash
sanctiontlo config --admin-key "your-key"
```

## Usage

```bash
# Search by name
sanctiontlo search --first-name "John" --last-name "Doe"

# Search by address
sanctiontlo search --street "123 Main St" --city "New York" --state "NY"

# Override saved admin key for a single search
sanctiontlo search --first-name "John" --last-name "Doe" --admin-key "different-key"
```

## Features

- Person search by name or address
- Persistent admin key configuration
- Rich terminal output
- Easy to use command-line interface

## License

MIT 