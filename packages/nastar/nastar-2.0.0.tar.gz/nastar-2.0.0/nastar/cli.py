import click
from .encoder import NastarEncoder

@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_file')
@click.option('--output', '-o', default='', help='Output file')
@click.option('--key', '-k', default='nastar_default_key', help='Kunci enkripsi')
def protect(input_file, output, key):
    """Proteksi file Python."""
    with open(input_file, 'r') as f:
        code = f.read()
    
    protected = NastarEncoder(key).protect(code)
    output_path = output or f"protected_{input_file}"
    with open(output_path, 'w') as f:
        f.write(protected)
    
    print(f"[+] File aman dibuat: {output_path}")

if __name__ == '__main__':
    cli()
