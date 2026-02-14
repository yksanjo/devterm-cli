"""DevTerm CLI - Command-line interface for developer utilities."""

import click
import json
import base64
import urllib.parse
import html
import hashlib
import uuid
import re
import hmac
import secrets
import socket
import urllib.parse as urlparse
import time
from datetime import datetime
from typing import Optional

import yaml
import toml
import xmltodict
import requests
import qrcode


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """DevTerm CLI - Developer Productivity Tools"""
    pass


# === DATA FORMATS ===

@cli.group()
def format():
    """Data formatting tools"""
    pass

@format.command()
@click.argument('input', required=False)
@click.option('--minify', is_flag=True, help='Minify instead of pretty print')
def json(input, minify):
    """Format/validate JSON"""
    if not input:
        input = click.get_text_stream('stdin').read()
    try:
        data = json.loads(input)
        if minify:
            output = json.dumps(data, separators=(',', ':'))
        else:
            output = json.dumps(data, indent=2)
        click.echo(output)
    except json.JSONDecodeError as e:
        click.echo(f"Error: {e}", err=True)

@format.command()
@click.argument('input', required=False)
def yaml_cmd(input):
    """Format YAML"""
    if not input:
        input = click.get_text_stream('stdin').read()
    try:
        data = yaml.safe_load(input)
        output = yaml.dump(data, default_flow_style=False)
        click.echo(output)
    except yaml.YAMLError as e:
        click.echo(f"Error: {e}", err=True)

@format.command()
@click.argument('input', required=False)
def xml(input):
    """Format XML"""
    if not input:
        input = click.get_text_stream('stdin').read()
    try:
        data = xmltodict.parse(input)
        output = json.dumps(data, indent=2)
        click.echo(output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


# === ENCODING ===

@cli.group()
def encode():
    """Encoding/decoding tools"""
    pass

@encode.command()
@click.argument('input', required=False)
def base64enc(input):
    """Base64 encode"""
    if not input:
        input = click.get_text_stream('stdin').read()
    output = base64.b64encode(input.encode()).decode()
    click.echo(output)

@encode.command()
@click.argument('input', required=False)
def base64dec(input):
    """Base64 decode"""
    if not input:
        input = click.get_text_stream('stdin').read()
    try:
        output = base64.b64decode(input.encode()).decode()
        click.echo(output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@encode.command()
@click.argument('input', required=False)
def urlenc(input):
    """URL encode"""
    if not input:
        input = click.get_text_stream('stdin').read()
    output = urllib.parse.quote(input, safe='')
    click.echo(output)

@encode.command()
@click.argument('input', required=False)
def urldec(input):
    """URL decode"""
    if not input:
        input = click.get_text_stream('stdin').read()
    output = urllib.parse.unquote(input)
    click.echo(output)

@encode.command()
@click.argument('input', required=False)
def htmlenc(input):
    """HTML encode"""
    if not input:
        input = click.get_text_stream('stdin').read()
    output = html.escape(input)
    click.echo(output)

@encode.command()
@click.argument('input', required=False)
def htmldec(input):
    """HTML decode"""
    if not input:
        input = click.get_text_stream('stdin').read()
    output = html.unescape(input)
    click.echo(output)


# === CRYPTOGRAPHY ===

@cli.group()
def hash():
    """Hashing tools"""
    pass

@hash.command()
@click.argument('input', required=False)
def md5(input):
    """MD5 hash"""
    if not input:
        input = click.get_text_stream('stdin').read()
    click.echo(hashlib.md5(input.encode()).hexdigest())

@hash.command()
@click.argument('input', required=False)
def sha256(input):
    """SHA-256 hash"""
    if not input:
        input = click.get_text_stream('stdin').read()
    click.echo(hashlib.sha256(input.encode()).hexdigest())

@hash.command()
@click.option('--length', default=16, help='Password length')
@click.option('--uppercase/--no-uppercase', default=True, help='Include uppercase')
@click.option('--lowercase/--no-lowercase', default=True, help='Include lowercase')
@click.option('--digits/--no-digits', default=True, help='Include digits')
@click.option('--special/--no-special', default=True, help='Include special')
def password(length, uppercase, lowercase, digits, special):
    """Generate password"""
    chars = ''
    if uppercase:
        chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if lowercase:
        chars += 'abcdefghijklmnopqrstuvwxyz'
    if digits:
        chars += '0123456789'
    if special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    if not chars:
        click.echo("Error: Select at least one character type", err=True)
        return
    
    pw = ''.join(secrets.choice(chars) for _ in range(length))
    click.echo(pw)

@hash.command()
def uuid4():
    """Generate UUID v4"""
    click.echo(str(uuid.uuid4()))


# === NETWORK ===

@cli.group()
def net():
    """Network tools"""
    pass

@net.command()
@click.argument('host', default='localhost')
@click.option('--start', default=1, help='Start port')
@click.option('--end', default=1024, help='End port')
def scan(host, start, end):
    """Scan ports"""
    click.echo(f"Scanning {host} ports {start}-{end}...")
    open_ports = []
    for port in range(start, min(end + 1, 10000)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        if sock.connect_ex((host, port)) == 0:
            open_ports.append(port)
        sock.close()
    
    if open_ports:
        click.echo(f"Open ports: {', '.join(map(str, open_ports))}")
    else:
        click.echo("No open ports found")

@net.command()
@click.argument('url')
@click.option('--method', default='GET', help='HTTP method')
def http(url, method):
    """Make HTTP request"""
    try:
        response = requests.request(method, url, timeout=10)
        click.echo(f"Status: {response.status_code}")
        click.echo(f"Headers: {dict(response.headers)}")
        click.echo(f"\nBody:\n{response.text[:1000]}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@net.command()
@click.argument('url')
def parseurl(url):
    """Parse URL"""
    parsed = urlparse.urlparse(url)
    click.echo(f"Scheme: {parsed.scheme}")
    click.echo(f"Host: {parsed.hostname}")
    click.echo(f"Port: {parsed.port}")
    click.echo(f"Path: {parsed.path}")
    click.echo(f"Query: {parsed.query}")


# === UTILITIES ===

@cli.group()
def util():
    """Utility tools"""
    pass

@util.command()
@click.argument('input', required=False)
def wc(input):
    """Word count"""
    if not input:
        input = click.get_text_stream('stdin').read()
    words = len(input.split())
    chars = len(input)
    lines = len(input.splitlines())
    click.echo(f"Words: {words}")
    click.echo(f"Characters: {chars}")
    click.echo(f"Lines: {lines}")

@util.command()
@click.argument('input', required=False)
@click.option('--to', default='upper', type=click.Choice(['upper', 'lower', 'title', 'camel', 'snake', 'kebab']))
def case(input, to):
    """Convert case"""
    if not input:
        input = click.get_text_stream('stdin').read()
    
    if to == 'upper':
        output = input.upper()
    elif to == 'lower':
        output = input.lower()
    elif to == 'title':
        output = input.title()
    elif to == 'camel':
        words = re.findall(r'[A-Za-z]+', input)
        output = words[0].lower() + ''.join(w.capitalize() for w in words[1:])
    elif to == 'snake':
        output = re.sub(r'[\W]+', '_', input).lower().strip('_')
    elif to == 'kebab':
        output = re.sub(r'[\W]+', '-', input).lower().strip('-')
    
    click.echo(output)

@util.command()
def timestamp():
    """Current timestamp"""
    click.echo(f"Unix: {int(time.time())}")
    click.echo(f"ISO: {datetime.now().isoformat()}")

@util.command()
@click.argument('text')
def qr(text):
    """Generate QR code"""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    click.echo("QR code saved to qrcode.png")


def main():
    cli()

if __name__ == "__main__":
    main()
