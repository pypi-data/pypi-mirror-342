import asyncio
import aiohttp
import dns.resolver
import validators
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from urllib.parse import urljoin, urlparse
from tld import get_fld
import re
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor
import json
from collections import defaultdict
from datetime import datetime
from typing import Dict, Set, List, Optional, Any, Tuple
from aiohttp import ClientTimeout
from aiohttp_client_cache import CachedSession, SQLiteBackend

class WebsiteScanner:
    def __init__(self, target_url: str, options: Optional[Dict[str, bool]] = None):
        self.target_url = target_url if target_url.startswith(('http://', 'https://')) else f'http://{target_url}'
        self.domain = get_fld(self.target_url)
        self.options = options or {
            "subdomain_scan": True,
            "port_scan": True,
            "ssl_scan": True,
            "content_scan": True
        }
        self.console = Console()
        self.visited_urls: Set[str] = set()
        self.found_emails: Set[str] = set()
        self.found_phones: Set[str] = set()
        self.found_social: Set[str] = set()
        self.open_ports: List[Tuple[int, str]] = []
        self.session: Optional[CachedSession] = None
        self.site_info: Dict[str, Set[str]] = defaultdict(set)
        self.tech_stack: Set[str] = set()
        self.content_stats: Dict[str, int] = defaultdict(int)
        self.forms: List[Dict[str, Any]] = []
        self.security_headers: Dict[str, str] = {}
        self.ssl_info: Dict[str, Any] = {}
        self.subdomains: Set[str] = set()
        self.results: Dict[str, Any] = {}
        self.timeout = ClientTimeout(total=30)

    async def initialize_session(self):
        cache = SQLiteBackend(cache_name='website_cache', expire_after=3600)
        self.session = CachedSession(cache=cache)
        
    async def close_session(self):
        if self.session:
            await self.session.close()

    async def enumerate_subdomains(self):
        common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'news', 'cp', 'blog',
            'dev', 'api', 'staging', 'test', 'admin', 'portal', 'beta', 'demo', 'shop',
            'store', 'app', 'support', 'cdn', 'cloud', 'vpn', 'git', 'docs', 'status'
        ]

        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1

        async def resolve_subdomain(subdomain: str):
            try:
                hostname = f"{subdomain}.{self.domain}"
                answers = await asyncio.get_event_loop().run_in_executor(
                    None, resolver.resolve, hostname, 'A'
                )
                if answers:
                    self.subdomains.add(hostname)
                    try:
                        cname = await asyncio.get_event_loop().run_in_executor(
                            None, resolver.resolve, hostname, 'CNAME'
                        )
                        if cname:
                            self.subdomains.add(str(cname[0].target))
                    except Exception:
                        pass
            except Exception:
                pass

        tasks = [resolve_subdomain(subdomain) for subdomain in common_subdomains]
        await asyncio.gather(*tasks)

        if self.ssl_info and not self.ssl_info.get('error'):
            san_list = self.ssl_info.get('SAN', [])
            for san in san_list:
                if isinstance(san, tuple) and san[0] == 'DNS':
                    self.subdomains.add(san[1])

    def get_ssl_info(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    self.ssl_info = {
                        'Issuer': dict(x[0] for x in cert['issuer']),
                        'Subject': dict(x[0] for x in cert['subject']),
                        'Valid From': datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d'),
                        'Valid Until': datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d'),
                        'Version': cert['version'],
                        'Serial Number': cert['serialNumber'],
                        'OCSP': cert.get('OCSP', ['N/A']),
                        'CA Issuers': cert.get('caIssuers', ['N/A']),
                        'SAN': cert.get('subjectAltName', [])
                    }
        except Exception as e:
            self.ssl_info = {"error": str(e)}

    def check_security_headers(self, headers: Dict[str, str]):
        security_headers = {
            'Strict-Transport-Security': 'HSTS not enabled',
            'Content-Security-Policy': 'CSP not configured',
            'X-Frame-Options': 'X-Frame-Options not set',
            'X-Content-Type-Options': 'X-Content-Type-Options not set',
            'Referrer-Policy': 'Referrer-Policy not set',
            'Permissions-Policy': 'Permissions-Policy not set',
            'X-XSS-Protection': 'X-XSS-Protection not set'
        }
        
        self.security_headers = {
            header: headers.get(header, default_value)
            for header, default_value in security_headers.items()
        }

    def detect_technologies(self, response_headers: Dict[str, str], html: str):
        tech_patterns = {
            'WordPress': ['wp-content', 'wp-includes', 'wp-json'],
            'jQuery': ['jquery.js', 'jquery.min.js'],
            'Bootstrap': ['bootstrap.css', 'bootstrap.js'],
            'React': ['react.js', 'react.production.min.js', 'react-dom'],
            'Vue.js': ['vue.js', 'vue.min.js', 'vue-router'],
            'Angular': ['angular.js', 'ng-', '@angular'],
            'Google Analytics': ['google-analytics.com', 'ga.js', 'gtag'],
            'Cloudflare': ['cloudflare', '__cf', 'cf-ray'],
            'PHP': ['.php', 'PHP', 'phpsessid'],
            'ASP.NET': ['.aspx', 'ASP.NET', '__VIEWSTATE'],
            'Laravel': ['laravel', 'XSRF-TOKEN', '_token'],
            'Django': ['csrftoken', 'django', 'dsession'],
            'Node.js': ['node_modules', 'express', 'next.js'],
            'TypeScript': ['ts-', '.ts', 'typescript'],
            'Webpack': ['webpack', 'chunkhash', 'webpackJsonp'],
            'GraphQL': ['graphql', '/graphql', 'apollo'],
        }

        headers_str = str(response_headers).lower()
        html_lower = html.lower()
        
        for tech, patterns in tech_patterns.items():
            if any(pattern.lower() in headers_str or pattern.lower() in html_lower for pattern in patterns):
                self.tech_stack.add(tech)

        if 'Server' in response_headers:
            self.tech_stack.add(f"Server: {response_headers['Server']}")

    def extract_site_info(self, soup: BeautifulSoup, url: str):
        if soup.title:
            self.site_info['titles'].add(soup.title.string.strip() if soup.title.string else '')

        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '').strip()
            
            if name == 'description':
                self.site_info['meta_descriptions'].add(content)
            elif name == 'keywords':
                self.site_info['meta_keywords'].update(k.strip() for k in content.split(','))

        favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon and favicon.get('href'):
            self.site_info['favicons'].add(urljoin(url, favicon['href']))

        self.forms.extend([{
            'action': form.get('action', ''),
            'method': form.get('method', 'get'),
            'inputs': [{
                'type': input.get('type', ''),
                'name': input.get('name', ''),
                'id': input.get('id', ''),
                'required': input.has_attr('required')
            } for input in form.find_all('input')]
        } for form in soup.find_all('form')])

        self.content_stats.update({
            'paragraphs': len(soup.find_all('p')),
            'headings': len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
            'images': len(soup.find_all('img')),
            'links': len(soup.find_all('a'))
        })

    async def scan_ports(self):
        common_ports = [21, 22, 23, 25, 53, 80, 110, 115, 135, 139, 143, 194, 443, 445, 1433, 3306, 3389, 5632, 5900, 8080]
        
        async def scan_single_port(port: int) -> Optional[Tuple[int, str]]:
            try:
                future = asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: socket.create_connection((self.domain, port), timeout=1)
                )
                await asyncio.wait_for(future, timeout=1)
                service = socket.getservbyport(port) if port < 1024 else "unknown"
                return port, service
            except (socket.timeout, socket.error, asyncio.TimeoutError):
                return None
            except Exception:
                return None

        tasks = [scan_single_port(port) for port in common_ports]
        results = await asyncio.gather(*tasks)
        self.open_ports = [result for result in results if result is not None]

    async def get_dns_info(self) -> Dict[str, Any]:
        dns_info: Dict[str, Any] = {}
        resolver = dns.resolver.Resolver()
        
        async def resolve_record(record_type: str) -> Optional[List[str]]:
            try:
                answers = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: resolver.resolve(self.domain, record_type)
                )
                if record_type == 'MX':
                    return [str(rdata.exchange) for rdata in answers]
                return [str(rdata) for rdata in answers]
            except Exception:
                return None

        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CAA']
        tasks = [resolve_record(rt) for rt in record_types]
        results = await asyncio.gather(*tasks)

        for rt, result in zip(record_types, results):
            if result:
                key = {
                    'A': 'IP Addresses',
                    'AAAA': 'IPv6 Addresses',
                    'MX': 'Mail Servers',
                    'NS': 'Name Servers',
                    'TXT': 'TXT Records',
                    'CAA': 'CAA Records'
                }[rt]
                dns_info[key] = result

        return dns_info

    def extract_contact_info(self, text: str):
        patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'\b(?:\+?\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
            'social': {
                'twitter': r'twitter\.com/[a-zA-Z0-9_]+',
                'facebook': r'facebook\.com/[a-zA-Z0-9.]+',
                'linkedin': r'linkedin\.com/(?:in|company)/[a-zA-Z0-9-]+',
                'instagram': r'instagram\.com/[a-zA-Z0-9_]+',
                'github': r'github\.com/[a-zA-Z0-9-]+',
                'youtube': r'youtube\.com/[@a-zA-Z0-9-]+'
            }
        }

        self.found_emails.update(re.findall(patterns['email'], text, re.IGNORECASE))
        self.found_phones.update(re.findall(patterns['phone'], text))
        
        for platform, pattern in patterns['social'].items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            self.found_social.update(f"{platform}:{match}" for match in matches)

    async def scan_url(self, url: str):
        if not self.session or url in self.visited_urls:
            return

        self.visited_urls.add(url)
        try:
            async with self.session.get(url, timeout=self.timeout, allow_redirects=True) as response:
                self.check_security_headers(response.headers)
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                
                self.detect_technologies(response.headers, content)
                self.extract_site_info(soup, url)
                self.extract_contact_info(content)

                return [
                    urljoin(url, link.get('href'))
                    for link in soup.find_all('a', href=True)
                    if validators.url(urljoin(url, link.get('href')))
                    and get_fld(urljoin(url, link.get('href'))) == self.domain
                ]
        except Exception as e:
            self.console.print(f"[red]Error scanning {url}: {str(e)}[/red]")
            return []

    async def crawl(self, max_urls: int = 100):
        if not self.session:
            await self.initialize_session()

        urls_to_scan = {self.target_url}
        scanned_count = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Crawling website...", total=max_urls)
            
            while urls_to_scan and scanned_count < max_urls:
                url = urls_to_scan.pop()
                new_urls = await self.scan_url(url)
                if new_urls:
                    urls_to_scan.update(new_urls)
                scanned_count += 1
                progress.update(task, completed=scanned_count)

    async def run_scan(self):
        try:
            await self.initialize_session()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                tasks = []
                
                if self.options["subdomain_scan"]:
                    task = progress.add_task("[cyan]Enumerating subdomains...", total=1)
                    tasks.append(self.enumerate_subdomains())
                    
                if self.options["ssl_scan"]:
                    task = progress.add_task("[cyan]Checking SSL certificate...", total=1)
                    self.get_ssl_info()
                    progress.update(task, completed=1)
                    
                if self.options["port_scan"]:
                    task = progress.add_task("[cyan]Scanning ports...", total=1)
                    tasks.append(self.scan_ports())
                    
                if tasks:
                    await asyncio.gather(*tasks)
                
                if self.options["content_scan"]:
                    task = progress.add_task("[cyan]Crawling website...", total=1)
                    await self.crawl()
                    progress.update(task, completed=1)

            self.results = {
                "target_url": self.target_url,
                "domain": self.domain,
                "subdomains": list(self.subdomains),
                "ssl_info": self.ssl_info,
                "security_headers": self.security_headers,
                "open_ports": self.open_ports,
                "technologies": list(self.tech_stack),
                "site_info": {k: list(v) for k, v in self.site_info.items()},
                "content_stats": self.content_stats,
                "forms": self.forms,
                "contact_info": {
                    "emails": list(self.found_emails),
                    "phones": list(self.found_phones),
                    "social": list(self.found_social)
                }
            }

        except Exception as e:
            self.console.print(f"[red]Error during scan: {str(e)}[/red]")
        finally:
            if self.session:
                await self.close_session()

    def display_results(self):
        if not self.results:
            self.console.print("[red]No scan results available.[/red]")
            return

        self.console.print("\n[bold cyan]Website Reconnaissance Report[/bold cyan]")
        self.console.print(Panel(f"Target: {self.results['target_url']}\nDomain: {self.results['domain']}"))

        if self.results["subdomains"]:
            table = Table(title="Subdomains")
            table.add_column("Subdomain")
            for subdomain in sorted(self.results["subdomains"]):
                table.add_row(subdomain)
            self.console.print(table)

        if self.results["ssl_info"] and "error" not in self.results["ssl_info"]:
            table = Table(title="SSL Certificate Information")
            table.add_column("Field")
            table.add_column("Value")
            for key, value in self.results["ssl_info"].items():
                if isinstance(value, (list, tuple)):
                    value = ", ".join(str(v) for v in value)
                elif isinstance(value, dict):
                    value = ", ".join(f"{k}={v}" for k, v in value.items())
                table.add_row(key, str(value))
            self.console.print(table)

        if self.results["security_headers"]:
            table = Table(title="Security Headers")
            table.add_column("Header")
            table.add_column("Value")
            for header, value in self.results["security_headers"].items():
                table.add_row(header, str(value))
            self.console.print(table)

        if self.results["open_ports"]:
            table = Table(title="Open Ports")
            table.add_column("Port")
            table.add_column("Service")
            for port, service in sorted(self.results["open_ports"]):
                table.add_row(str(port), service)
            self.console.print(table)

        if self.results["technologies"]:
            table = Table(title="Detected Technologies")
            table.add_column("Technology")
            for tech in sorted(self.results["technologies"]):
                table.add_row(tech)
            self.console.print(table)

        if self.results["site_info"]:
            self.console.print("\n[bold cyan]Site Information[/bold cyan]")
            for key, values in self.results["site_info"].items():
                if values:
                    self.console.print(f"\n[bold]{key.replace('_', ' ').title()}:[/bold]")
                    for value in values:
                        self.console.print(f"  • {value}")

        if self.results["content_stats"]:
            table = Table(title="Content Statistics")
            table.add_column("Type")
            table.add_column("Count")
            for stat_type, count in self.results["content_stats"].items():
                table.add_row(stat_type.replace("_", " ").title(), str(count))
            self.console.print(table)

        if self.results["forms"]:
            self.console.print("\n[bold cyan]Forms Found[/bold cyan]")
            for i, form in enumerate(self.results["forms"], 1):
                self.console.print(f"\n[bold]Form {i}:[/bold]")
                self.console.print(f"  Method: {form['method'].upper()}")
                self.console.print(f"  Action: {form['action']}")
                if form['inputs']:
                    self.console.print("  Inputs:")
                    for input_field in form['inputs']:
                        required = "[red]*[/red]" if input_field.get('required') else ""
                        self.console.print(f"    • {input_field['type']} - {input_field['name']} {required}")

        contact_info = self.results["contact_info"]
        if any(contact_info.values()):
            self.console.print("\n[bold cyan]Contact Information[/bold cyan]")
            if contact_info["emails"]:
                self.console.print("\n[bold]Email Addresses:[/bold]")
                for email in sorted(contact_info["emails"]):
                    self.console.print(f"  • {email}")
            if contact_info["phones"]:
                self.console.print("\n[bold]Phone Numbers:[/bold]")
                for phone in sorted(contact_info["phones"]):
                    self.console.print(f"  • {phone}")
            if contact_info["social"]:
                self.console.print("\n[bold]Social Media:[/bold]")
                for social in sorted(contact_info["social"]):
                    platform, handle = social.split(":", 1)
                    self.console.print(f"  • {platform.title()}: {handle}") 