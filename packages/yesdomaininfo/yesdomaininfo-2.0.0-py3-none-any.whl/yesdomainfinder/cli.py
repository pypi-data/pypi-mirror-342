import requests
import dns.resolver
import whois
import socket
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import argparse
import json

console = Console()

class DomainInvestigator:
    def __init__(self, domain):
        self.domain = domain
        self.results = {
            'whois': {},
            'dns': {},
            'server_info': {},
            'security': {},
            'subdomains': []
        }

    def get_whois_info(self):
        """Get WHOIS information for the domain"""
        with Progress() as progress:
            task = progress.add_task("[cyan]Fetching WHOIS data...", total=1)
            
            try:
                whois_data = whois.whois(self.domain)
                self.results['whois'] = {
                    'registrar': whois_data.registrar,
                    'creation_date': whois_data.creation_date,
                    'expiration_date': whois_data.expiration_date,
                    'name_servers': whois_data.name_servers,
                    'status': whois_data.status
                }
            except Exception as e:
                self.results['whois'] = {'error': str(e)}
            
            progress.update(task, completed=1)

    def get_dns_records(self):
        """Get various DNS records for the domain"""
        with Progress() as progress:
            task = progress.add_task("[cyan]Fetching DNS records...", total=1)
            
            record_types = ['A', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(self.domain, record_type)
                    self.results['dns'][record_type] = [str(r) for r in answers]
                except:
                    self.results['dns'][record_type] = None
            
            progress.update(task, completed=1)

    def get_server_info(self):
        """Get web server and IP information"""
        with Progress() as progress:
            task = progress.add_task("[cyan]Checking server info...", total=1)
            
            try:
                # Get IP address
                ip_addr = socket.gethostbyname(self.domain)
                self.results['server_info']['ip_address'] = ip_addr
                
                # Get server headers
                response = requests.get(f"http://{self.domain}", timeout=5)
                self.results['server_info']['http_status'] = response.status_code
                self.results['server_info']['server'] = response.headers.get('Server', 'Unknown')
                self.results['server_info']['content_type'] = response.headers.get('Content-Type', 'Unknown')
            except Exception as e:
                self.results['server_info']['error'] = str(e)
            
            progress.update(task, completed=1)

    def check_security(self):
        """Check basic security headers"""
        with Progress() as progress:
            task = progress.add_task("[cyan]Checking security...", total=1)
            
            try:
                response = requests.get(f"https://{self.domain}", timeout=5)
                security_headers = {
                    'Strict-Transport-Security': response.headers.get('Strict-Transport-Security'),
                    'Content-Security-Policy': response.headers.get('Content-Security-Policy'),
                    'X-Frame-Options': response.headers.get('X-Frame-Options'),
                    'X-Content-Type-Options': response.headers.get('X-Content-Type-Options'),
                    'X-XSS-Protection': response.headers.get('X-XSS-Protection')
                }
                self.results['security'] = security_headers
            except:
                self.results['security'] = {'error': 'Could not fetch security headers'}
            
            progress.update(task, completed=1)

    def find_subdomains(self):
        """Find common subdomains (limited without API)"""
        with Progress() as progress:
            task = progress.add_task("[cyan]Checking subdomains...", total=1)
            
            common_subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 
                               'test', 'dev', 'staging', 'api', 'cdn']
            
            for sub in common_subdomains:
                full_domain = f"{sub}.{self.domain}"
                try:
                    socket.gethostbyname(full_domain)
                    self.results['subdomains'].append(full_domain)
                except:
                    continue
            
            progress.update(task, completed=1)

    def display_results(self):
        """Display all results in a structured format"""
        console.print()
        console.print(Panel.fit(f"[bold green]Domain Investigation Report for [yellow]{self.domain}[/]", 
                              border_style="green"))
        
        # WHOIS Information
        console.print(Panel.fit("[bold cyan]WHOIS Information[/]", border_style="cyan"))
        whois_table = Table(show_header=True, header_style="bold magenta")
        whois_table.add_column("Field", style="dim", width=25)
        whois_table.add_column("Value")
        
        for key, value in self.results['whois'].items():
            if isinstance(value, list):
                value = "\n".join(value) if value else "None"
            whois_table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(whois_table)

        # DNS Records
        console.print(Panel.fit("[bold cyan]DNS Records[/]", border_style="cyan"))
        dns_table = Table(show_header=True, header_style="bold magenta")
        dns_table.add_column("Record Type", style="dim", width=10)
        dns_table.add_column("Values")
        
        for record_type, values in self.results['dns'].items():
            if values:
                dns_table.add_row(record_type, "\n".join(values))
        
        console.print(dns_table)

        # Server Information
        console.print(Panel.fit("[bold cyan]Server Information[/]", border_style="cyan"))
        server_table = Table(show_header=True, header_style="bold magenta")
        server_table.add_column("Info", style="dim", width=25)
        server_table.add_column("Details")
        
        for key, value in self.results['server_info'].items():
            server_table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(server_table)

        # Security Headers
        console.print(Panel.fit("[bold cyan]Security Headers[/]", border_style="cyan"))
        security_table = Table(show_header=True, header_style="bold magenta")
        security_table.add_column("Header", style="dim", width=30)
        security_table.add_column("Present")
        
        for header, value in self.results['security'].items():
            present = "[green]Yes[/]" if value else "[red]No[/]"
            security_table.add_row(header, present)
        
        console.print(security_table)

        # Subdomains
        console.print(Panel.fit("[bold cyan]Found Subdomains[/]", border_style="cyan"))
        if self.results['subdomains']:
            subdomain_table = Table(show_header=True, header_style="bold magenta")
            subdomain_table.add_column("Subdomain")
            
            for sub in self.results['subdomains']:
                subdomain_table.add_row(sub)
            
            console.print(subdomain_table)
        else:
            console.print("[yellow]No common subdomains found[/]")

        # Footer
        console.print(Panel.fit("[red]NOTE:[/] This tool provides basic information only. For comprehensive security testing, use professional tools.", 
                              border_style="red"))

def main():
    parser = argparse.ArgumentParser(description='Domain Information Finder')
    parser.add_argument('domain', help='Domain to investigate')
    args = parser.parse_args()

    # ASCII Art Header
    console.print(Panel.fit("""
    [bold blue]
\ \ / /__  __\ \   / /_ _ _ __  ___| |__  ____
 \ V / _ \/ __\ \ / / _` | '_ \/ __| '_ \|_  /
  | |  __/\__ \\ V / (_| | | | \__ \ | | |/ / 
  |_|\___||___/ \_/ \__,_|_| |_|___/_| |_/___|
    [/]""", subtitle="[green]Domain Information Finder (DIF) Made By YesVanshz[/]"))

    investigator = DomainInvestigator(args.domain)
    
    console.print(f"[yellow]Investigating:[/] [white]{args.domain}[/]")
        
    investigator.get_whois_info()
    investigator.get_dns_records()
    investigator.get_server_info()
    investigator.check_security()
    investigator.find_subdomains()
    
    investigator.display_results()

if __name__ == "__main__":
    main()