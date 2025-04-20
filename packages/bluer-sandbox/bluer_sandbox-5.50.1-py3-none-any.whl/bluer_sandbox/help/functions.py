from typing import List

from bluer_options.terminal import show_usage, xtra
from bluer_ai.help.generic import help_functions as generic_help_functions
from bluer_sandbox.help.assets import help_functions as help_assets
from bluer_sandbox.help.notebooks import help_functions as help_notebooks
from bluer_sandbox.help.offline_llm import help_functions as help_offline_llm

from bluer_sandbox import ALIAS


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "assets": help_assets,
        "notebooks": help_notebooks,
        "offline_llm": help_offline_llm,
    }
)
