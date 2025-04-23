import re
from difflib import get_close_matches
from operator import itemgetter
from pathlib import Path
from typing import Annotated, TypedDict

import requests
import shellingham  # type: ignore[import-untyped]
import typer
import typer.completion
from rich import print as rprint
from rich.columns import Columns
from rich.console import Console
from rich.prompt import Prompt

app = typer.Typer(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
    help="Create a .gitignore or .prettierignore file for over 500 languages and frameworks. Currently, the source for the ignore files is https://gitignore.io but this may change in the future to ensure the most up-to-date ignore files are used (see also https://github.com/toptal/gitignore.io/issues/650)",
)

typer.completion.completion_init()  # type: ignore[attr-defined]


def get_file_type_links(languages: list[str]) -> str:
    if len(languages) == 1:
        return f"[bold][link=https://gitignore.io/api/{languages[0]}]{languages[0]}[/link][/bold]"
    elif len(languages) == 2:
        return f"[bold][link=https://gitignore.io/api/{languages[0]}]{languages[0]}[/link][/bold] and [bold][link=https:///gitignore.io/api/{languages[1]}]{languages[1]}[/link][/bold]"
    elif len(languages) > 2:
        languages_str = ", ".join([f"[link=https://gitignore.io/api/{ft}]{ft}[/link]" for ft in languages[:-1]])
        return (
            f"{languages_str}, and [bold][link=https://gitignore.io/api/{languages[-1]}]{languages[-1]}[/link][/bold]"
        )
    return ""


def get_gitignore(languages: list[str]) -> str:
    languages_joined = ",".join([f"{ft}" for ft in languages])
    response = requests.get(f"https://gitignore.io/api/{languages_joined}")
    if response.status_code == 200:
        return f"# Created with easyignore\n{response.text}"
    else:
        rprint(
            f"[red]Failed to fetch gitignore for {languages_joined}. Check that {languages_joined} is valid and that you are connected to the internet and try again.[/red]"
        )
        raise typer.Exit(code=1)


def get_gitignores() -> list[str]:
    response = requests.get("https://gitignore.io/api/list")
    if response.status_code == 200:
        return re.split("\n|,", response.text)
    else:
        rprint("[red]Failed to fetch gitignore list. Check your internet connection and try again.[/red]")
        raise typer.Exit(code=1)


def complete_gitignores() -> list[str]:
    return get_gitignores()


def validate_gitignores(value: list[str]) -> list[str]:
    for v in value:
        if v not in complete_gitignores():
            best_matches = get_close_matches(v, complete_gitignores(), n=5, cutoff=0)
            if best_matches:
                raise typer.BadParameter(
                    f"'{v}'. Perhaps you meant one of: {'  '.join(best_matches)}",
                    param_hint="LANGUAGES",
                )
            else:
                raise typer.BadParameter(f"'{v}'. No close matches found.", param_hint="LANGUAGES")
    return value


def list_gitignores(value: bool) -> None:
    """
    List available languages/frameworks available from gitignore.io
    """
    if not value:
        return
    git_ignores = get_gitignores()
    git_ignores = [f"{g}" for g in git_ignores]
    git_ignores_output = Columns(git_ignores, equal=True, expand=True)
    console = Console()
    with console.pager():
        console.print(git_ignores_output)
    raise typer.Exit(code=0)


def show_completion(ctx: typer.Context, value: bool) -> None:
    if value:
        shell, _ = shellingham.detect_shell()
        # param is currently unused in typer code, if this changes this will break
        typer.completion.show_callback(ctx, None, shell)  # type: ignore[arg-type]
        raise typer.Exit(code=0)


def install_completion(ctx: typer.Context, value: bool) -> None:
    if value:
        shell, _ = shellingham.detect_shell()
        # param is currently unused in typer code, if this changes this will break
        typer.completion.install_callback(ctx, None, shell)  # type: ignore[arg-type]
        raise typer.Exit(code=0)


def save_file(path: Path, mode: str, content: str) -> None:
    with open(path, mode) as f:
        f.write(content)


class OverwriteOrAppend(TypedDict):
    append: bool
    overwrite: bool


def prompt_overwrite_or_append(path: Path) -> OverwriteOrAppend:
    append_or_overwrite = Prompt.ask(
        "File already exists. Do you want to overwrite, append, or cancel? (o/a/c)",
    )
    if append_or_overwrite == "a":
        return {"append": True, "overwrite": False}
    elif append_or_overwrite == "o":
        return {"append": False, "overwrite": True}
    else:
        raise typer.Abort()


@app.command(no_args_is_help=True)
def main(
    languages: Annotated[
        list[str],
        typer.Argument(
            help="Language/framework for ignore file. Enter multiple separated by spaces.",
            autocompletion=get_gitignores,
            callback=validate_gitignores,
            is_eager=True,
        ),
    ],
    directory: Annotated[
        Path,
        typer.Option(
            "--directory",
            "-d",
            help="Directory for ignore file. [default: current directory]",
            file_okay=False,
            dir_okay=True,
            is_eager=True,
            rich_help_panel="File Options",
        ),
    ] = Path.cwd(),  # noqa: B008  # function-call-in-default-argument
    file: Annotated[
        str,
        typer.Option(
            "--file",
            "-f",
            help="File name for ignore file. [default: .gitignore]",
            file_okay=True,
            dir_okay=False,
            is_eager=True,
            rich_help_panel="File Options",
        ),
    ] = ".gitignore",
    append: Annotated[
        bool,
        typer.Option(
            "--append",
            "-a",
            help="Append to existing ignore file.",
            show_default=True,
            is_eager=True,
            rich_help_panel="File Options",
        ),
    ] = False,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            "-o",
            help="Overwrite existing ignore file.",
            show_default=True,
            is_eager=True,
            rich_help_panel="File Options",
        ),
    ] = False,
    output_to_stdout: Annotated[
        bool,
        typer.Option(
            "--print",
            "-p",
            help="Print ignore file to stdout instead of saving to file.",
            is_eager=True,
        ),
    ] = False,
    list_gitignores: Annotated[
        bool,
        typer.Option(
            "--list",
            "-l",
            help="List available languages/frameworks for ignore file.",
            is_eager=True,
            callback=list_gitignores,
        ),
    ] = False,
    # custom handling of install completion and show completion
    # allows no arguments to be passed when installing or showing completion scripts
    install_completion: Annotated[
        bool,
        typer.Option(
            "--install-completion",
            "-i",
            help="Install shell completion for easyignore.",
            callback=install_completion,
            is_eager=True,
            rich_help_panel="Shell Completion",
        ),
    ] = False,
    show_completion: Annotated[
        bool,
        typer.Option(
            "--show-completion",
            "-s",
            help="Show shell completion for easyignore.",
            callback=show_completion,
            is_eager=True,
            rich_help_panel="Shell Completion",
        ),
    ] = False,
) -> None:
    """
    Create an ignore file for over 500 languages and frameworks.
    """
    # Consider using https://donotcommit.com/api as a source instead of gitignore.io once they expand available languages
    if output_to_stdout:
        # no rich print here to enable easy piping to other commands
        print(get_gitignore(languages))
        raise typer.Exit(code=0)

    if append and overwrite:
        raise typer.BadParameter(
            "Cannot use both append and overwrite options at the same time.",
            param_hint="append / overwrite",
        )
    if directory.exists() and not directory.is_dir():
        # this should be caught by the file_okay=False option
        raise typer.BadParameter(
            "directory must be a directory. Please provide a directory directory to create the .gitignore file.",
            param_hint="directory",
        )
    if not directory.exists():
        Path(directory).mkdir(parents=True, exist_ok=False)
    path = directory / file

    if path.exists():
        if not append and not overwrite:
            # unpack the dictionary returned by prompt_overwrite_or_append
            append, overwrite = itemgetter("append", "overwrite")(prompt_overwrite_or_append(path))
        if append and not overwrite:
            save_file(path, "a+", f"\n\n{get_gitignore(languages)}")
            rprint(f"[green]Appended {get_file_type_links(languages)} ignore to existing file at path[/green]")
        elif overwrite and not append:
            save_file(path, "w", get_gitignore(languages))
            rprint(f"[green]Overwrote existing file with {get_file_type_links(languages)} ignore at {path}[/green]")
    else:
        save_file(path, "w", get_gitignore(languages))
        rprint(f"[green]Created new {get_file_type_links(languages)} ignore at {path}[/green]")
    typer.Exit(code=0)


if __name__ == "__main__":
    app()
