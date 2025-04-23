import os
import click
import subprocess

README_TEMPLATE = """# {name}

A simple Python package.
"""

SETUP_TEMPLATE = '''from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{name}",
    version="0.1.0",
    author="{username}",
    author_email="{username}.contact@gmail.com",
    description="A simple Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/{username}/{name}",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
'''

LICENSE_TEMPLATE = """MIT License

Copyright (c) 2025 {username}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

INIT_TEMPLATE = '''__version__ = "0.1.0"
'''

CODE_TEMPLATE = '''def example():
    print("Hello from {pkg_name}!")
'''

@click.group()
def cli():
    """BuildSnap CLI."""
    pass

@cli.command()
@click.option('--tar', is_flag=True, help='Build source distribution (.tar.gz).')
@click.option('--whl', is_flag=True, help='Build wheel distribution (.whl).')
@click.option('--path', '-p', default='.', help='Path to setup.py or project root.')
def build(tar, whl, path):
    """Build the package."""
    os.chdir(path)

    if tar:
        click.echo("Building source distribution...")
        subprocess.run(['python', 'setup.py', 'sdist'])

    if whl:
        click.echo("Building wheel distribution...")
        subprocess.run(['python', 'setup.py', 'bdist_wheel'])

    if not (tar or whl):
        click.echo("Please specify --tar and/or --whl.")

@cli.command()
@click.option('--name', required=True, help='Package name to initialize.')
@click.option('--username', required=True, help='Your GitHub username (also used in LICENSE and setup).')
def init(name, username):
    """Initialize a new Python package layout."""
    if os.path.exists(name):
        click.echo(f"Directory '{name}' already exists.")
        return

    os.makedirs(f"{name}/{name}")

    with open(f"{name}/README.md", "w") as f:
        f.write(README_TEMPLATE.format(name=name))

    with open(f"{name}/LICENSE", "w") as f:
        f.write(LICENSE_TEMPLATE.format(username=username))

    with open(f"{name}/setup.py", "w") as f:
        f.write(SETUP_TEMPLATE.format(name=name, username=username))

    with open(f"{name}/{name}/__init__.py", "w") as f:
        f.write(INIT_TEMPLATE)

    with open(f"{name}/{name}/code.py", "w") as f:
        f.write(CODE_TEMPLATE.format(pkg_name=name))

    click.echo(f"Initialized new package '{name}' for user '{username}' at './{name}'.")

@cli.command()
@click.option('--path', '-p', default='.', help='Path to the package directory to install.')
def install(path):
    """Install the package locally."""
    if not os.path.exists(path):
        click.echo(f"Path '{path}' does not exist.")
        return

    click.echo(f"Installing package from '{path}'...")
    result = subprocess.run(['pip', 'install', path])
    if result.returncode == 0:
        click.echo("Package installed successfully.")
    else:
        click.echo("Installation failed.")

if __name__ == "__main__":
    cli()