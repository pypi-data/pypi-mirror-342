from .scanner import WebsiteScanner
import asyncio
import platform

__version__ = "0.1.6"

def scan_website(url, *, no_subdomains=False, no_ports=False, no_ssl=False, no_content=False):
    """
    Synchronous function to scan a website. This is a convenience wrapper around WebsiteScanner.
    
    Args:
        url (str): The URL or domain to scan
        no_subdomains (bool): Skip subdomain scanning if True
        no_ports (bool): Skip port scanning if True
        no_ssl (bool): Skip SSL analysis if True
        no_content (bool): Skip content analysis if True
    
    Returns:
        dict: The scan results
    """
    options = {
        "subdomain_scan": not no_subdomains,
        "port_scan": not no_ports,
        "ssl_scan": not no_ssl,
        "content_scan": not no_content
    }
    
    scanner = WebsiteScanner(url, options)
    
    # Set up the event loop
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(scanner.run_scan())
        finally:
            loop.close()
    else:
        asyncio.run(scanner.run_scan())
    
    return scanner.results

async def scan_website_async(url, *, no_subdomains=False, no_ports=False, no_ssl=False, no_content=False):
    """
    Asynchronous function to scan a website. Use this if you're in an async context.
    
    Args:
        url (str): The URL or domain to scan
        no_subdomains (bool): Skip subdomain scanning if True
        no_ports (bool): Skip port scanning if True
        no_ssl (bool): Skip SSL analysis if True
        no_content (bool): Skip content analysis if True
    
    Returns:
        dict: The scan results
    """
    options = {
        "subdomain_scan": not no_subdomains,
        "port_scan": not no_ports,
        "ssl_scan": not no_ssl,
        "content_scan": not no_content
    }
    
    scanner = WebsiteScanner(url, options)
    await scanner.run_scan()
    return scanner.results

__all__ = ["WebsiteScanner", "scan_website", "scan_website_async"] 