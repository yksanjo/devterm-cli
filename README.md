# DevTerm CLI

Command-line developer utilities - 50+ tools in your terminal.

## Installation

```bash
pip install devterm-cli
```

## Usage

```bash
# JSON formatting
devterm format json '{"key": "value"}'
devterm format json --minify '{"key": "value"}'

# Base64 encoding
devterm encode base64enc "Hello World"
devterm encode base64dec "SGVsbG8gV29ybGQ="

# Hash generation
devterm hash md5 "text"
devterm hash sha256 "text"

# Password generation
devterm hash password --length 20 --special

# UUID generation
devterm hash uuid4

# Network tools
devterm net scan localhost --start 1 --end 100
devterm net http https://api.github.com
devterm net parseurl "https://example.com/path?key=value"

# Utilities
devterm util wc "Hello world"
devterm util case "hello_world" --to camel
devterm util timestamp
devterm util qr "Hello"
```

## Tools

- **Data Formats**: JSON, YAML, XML
- **Encoding**: Base64, URL, HTML
- **Cryptography**: MD5, SHA-256, Password, UUID
- **Network**: Port Scanner, HTTP Client, URL Parser
- **Utilities**: Word Count, Case Converter, Timestamp, QR Code
