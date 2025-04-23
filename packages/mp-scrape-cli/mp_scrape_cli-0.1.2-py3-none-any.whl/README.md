<!--
SPDX-FileCopyrightText: 2025 Sofía Aritz <sofiaritz@fsfe.org>

SPDX-License-Identifier: AGPL-3.0-only
-->

# MP Scrape CLI

Part of the [MP Scrape](https://git.fsfe.org/mp-scrape/mp-scrape) project.

MP Scrape CLI allows you to easily run MP Scrape Workflows from the CLI.

## Where to get it

You can get it through the [Python Package Index (PyPI)](https://pypi.org/project/mp_scrape_core/):

```sh
$ pip3 install mp_scrape_cli
```

## How to use it

Assuming you have a workflow at `workflow.toml`

```sh
$ python3 -m mp_scrape_cli -w workflow.toml -l DEBUG
```