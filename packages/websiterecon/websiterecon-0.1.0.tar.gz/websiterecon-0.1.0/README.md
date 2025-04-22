# WebsiteRecon

A comprehensive website reconnaissance and scanning tool that provides detailed information about websites, including subdomains, security headers, SSL certificates, and more.

## Features

- Subdomain enumeration
- Port scanning
- DNS information gathering
- SSL certificate analysis
- Security headers check
- Technology detection
- Content analysis
- Form analysis
- Contact information extraction
- Beautiful console output using Rich

## Installation

```bash
pip install websiterecon
```

## Usage

### Command Line

```bash
websiterecon example.com
```

### Options

- `--no-subdomains`: Skip subdomain scanning
- `--no-ports`: Skip port scanning
- `--no-ssl`: Skip SSL certificate analysis
- `--no-content`: Skip content analysis
- `-o` or `--output`: Save results to a JSON file

### Examples

```bash
# Basic scan
websiterecon example.com

# Skip subdomain scanning
websiterecon --no-subdomains example.com

# Save results to a file
websiterecon example.com -o results.json

# Quick scan (skip intensive operations)
websiterecon --no-subdomains --no-ports example.com
```

## License

MIT License 