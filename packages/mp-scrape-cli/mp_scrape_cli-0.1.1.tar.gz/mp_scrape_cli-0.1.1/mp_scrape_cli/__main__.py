# SPDX-FileCopyrightText: 2025 Sofía Aritz <sofiaritz@fsfe.org>
#
# SPDX-License-Identifier: AGPL-3.0-only

from . import Workflow

from mp_scrape_core import Pipeline

import sys
import subprocess
import asyncio
import tomllib
import importlib
import inspect
import click

@click.command()
@click.option('--workflow', '-w')
@click.option('--log-level', '-l')
def mp_scrape(workflow, log_level = "INFO"):
    """Run modules in the CLI"""

    workflow = Workflow(workflow, warning_log=click.echo, on_module_not_found=install_module)

    sources = workflow.sources()   
    click.echo("All sources instantiated")

    processes = workflow.processes()
    click.echo("All processes instantiated")
    
    consumers = workflow.consumers()
    click.echo("All consumers instantiated")

    pipeline = Pipeline(sources=sources, processes=processes, consumers=consumers)
    asyncio.run(pipeline.run(log_level=log_level.upper() if log_level is not None else "INFO"))

    click.echo("Pipeline ran successfully!")

def install_module(mod):
    if click.confirm(f"Module '{mod}' was not found. Would you like to install it now using pip?"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", mod])
    else:
        click.echo(f"Cannot proceed without '{mod}', please install it and try again")
        raise Exception(f"Cannot proceed without '{mod}'")

if __name__ == "__main__":
    mp_scrape()