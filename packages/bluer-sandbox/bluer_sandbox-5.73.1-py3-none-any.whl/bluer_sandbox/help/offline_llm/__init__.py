from typing import List

from bluer_options.terminal import show_usage, xtra

from bluer_sandbox.help.offline_llm.model import help_functions as help_model


def help_install(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("dryrun", mono=mono)

    return show_usage(
        [
            "@offline_llm",
            "install",
            f"[{options}]",
        ],
        "install offline_llm.",
        mono=mono,
    )


def help_prompt(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("tiny,~upload", mono=mono)

    return show_usage(
        [
            "@offline_llm",
            "prompt",
            f"[{options}]",
            '"<prompt>"',
            "[-|<object-name>]",
        ],
        '"<prompt>" -> offline_llm.',
        mono=mono,
    )


help_functions = {
    "install": help_install,
    "model": help_model,
    "prompt": help_prompt,
}
