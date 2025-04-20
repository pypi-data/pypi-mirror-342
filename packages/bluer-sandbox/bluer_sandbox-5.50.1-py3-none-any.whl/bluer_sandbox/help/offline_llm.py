from typing import List

from bluer_options.terminal import show_usage, xtra


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
    options = xtra("~upload", mono=mono)

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
    "prompt": help_prompt,
}
