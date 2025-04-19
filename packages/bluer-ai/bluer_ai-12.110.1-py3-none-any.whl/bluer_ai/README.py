import os

from bluer_options.help.functions import get_help
from bluer_objects import file, README

from bluer_ai import NAME, VERSION, ICON, REPO_NAME
from bluer_ai.help.functions import help_functions


def build():
    return all(
        README.build(
            path=os.path.join(file.path(__file__), path),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
            MODULE_NAME=NAME,
            help_function=lambda tokens: get_help(
                tokens,
                help_functions,
                mono=True,
            ),
        )
        for path in [
            "..",
            "docs/aliases/conda.md",
            "docs/aliases/git.md",
            "docs/aliases/gpu.md",
            "docs/aliases/init.md",
            "docs/aliases/latex.md",
            "docs/aliases/logging.md",
            "docs/aliases/pypi.md",
            "docs/aliases/screen.md",
            "docs/aliases/seed.md",
            "docs/aliases/ssh.md",
            "docs/aliases/terraform.md",
            "docs/aliases/wifi.md",
        ]
    )
