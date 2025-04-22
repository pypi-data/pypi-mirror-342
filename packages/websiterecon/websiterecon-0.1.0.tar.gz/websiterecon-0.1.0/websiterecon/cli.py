import asyncio
import argparse
from rich.console import Console
from .scanner import WebsiteScanner

def parse_args():
    parser = argparse.ArgumentParser(description="WebsiteRecon - Comprehensive Website Scanner")
    parser.add_argument("url", help="Target URL or domain to scan")
    parser.add_argument("--no-subdomains", action="store_true", help="Disable subdomain scanning")
    parser.add_argument("--no-ports", action="store_true", help="Disable port scanning")
    parser.add_argument("--no-ssl", action="store_true", help="Disable SSL analysis")
    parser.add_argument("--no-content", action="store_true", help="Disable content analysis")
    parser.add_argument("-o", "--output", help="Save results to file (JSON format)")
    return parser.parse_args()

async def main_async():
    args = parse_args()
    console = Console()
    
    options = {
        "subdomain_scan": not args.no_subdomains,
        "port_scan": not args.no_ports,
        "ssl_scan": not args.no_ssl,
        "content_scan": not args.no_content
    }
    
    scanner = WebsiteScanner(args.url, options)
    results = await scanner.run_scan()
    
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
            console.print(f"[green]Results saved to {args.output}[/green]")

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        Console().print("\n[yellow]Scan interrupted by user[/yellow]")
    except Exception as e:
        Console().print(f"[red]Error: {str(e)}[/red]") 