from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent

from src.count_words import word_count
from src.present import present_word_count, present_aggregation, present_nodes, LsItem
from src.highlight_identifiers import highlight_identifiers
from src.get_nodes import get_functions, get_classes, get_modules
from src.aggregation import Aggregation

USAGE = """\
%(prog)s COMMAND [options]

A cli-tool that helps you dig up knowledge from Python legacy code.

Commands:
  hi          Highlight the identifiers in functions
  wc          Count the words in functions
  ls          List 
"""


def main():
    parser = ArgumentParser(
        usage=USAGE,
        add_help=True,
    )
    parser.add_argument("command")
    parser.add_argument(
        type=Path,
        nargs="*",
        dest="file_or_dirs",
        default=[Path()],
        help="Source file or directory",
    )
    parser.add_argument(
        "--target",
        "-t",
        choices=["functions", "classes", "modules"],
        default="modules",
    )
    parser.add_argument(
        "--search",
        "-s",
        nargs="?",
        default="",
        help=dedent(
            """\
        keep only nodes that with a location that match the 'search'.
        Location has form 'file.py::ClassName::method_name'
        """
        ),
    )
    parser.add_argument(
        "-f",
        nargs="?",
        default=None,
        const="",
        help="""\
        Shorthand for `-t functions -s SEARCH`. 
        It override their values.
        """,
    )
    parser.add_argument(
        "-c",
        nargs="?",
        default=None,
        const="",
        help="""\
        Shorthand for `-t classes -s SEARCH`.
        It override their values.
        """,
    )

    args, remaining_args = parser.parse_known_args()
    command = args.command

    dirs = args.file_or_dirs
    target = args.target
    search = args.search

    if args.f is not None:
        target = "functions"
        search = args.f

    if args.c is not None:
        target = "classes"
        search = args.c

    match target:
        case "functions":
            nodes = list(get_functions(dirs, search))
        case "classes":
            nodes = list(get_classes(dirs, search))
        case _:  # "modules"
            nodes = list(get_modules(dirs, search))

    print()
    match command:
        case "wc":
            wc_parser = ArgumentParser()
            aggregate_by_default = target == "modules"
            wc_parser.add_argument("--aggregate", action="store_true", default=aggregate_by_default)
            wc_args = wc_parser.parse_args(remaining_args)
            if wc_args.aggregate:
                word_counts = [word_count(n.definition, n.length) for n in nodes]
                print(f"{len(nodes)} {target}")
                if len(nodes) < 5:
                    for node in nodes:
                        print(node.location)
                print(present_aggregation(Aggregation.of(word_counts)))
            else:
                for node in nodes:
                    print(f"{node.location}")
                    print(present_word_count(word_count(node.definition, node.length).sorted_by_occurences()))
        case "hi":
            hi_parser = ArgumentParser()
            hi_parser.add_argument("--word", "-w", type=str, nargs="*", default=None)
            hi_parser.add_argument("--params-only", "-p", action="store_true", default=False)
            hi_args = hi_parser.parse_args(remaining_args)
            words = set(hi_args.word) if hi_args.word is not None else None

            for node in nodes:
                print(f"{node.location} ")
                print(highlight_identifiers(node.source, words, params_only=hi_args.params_only))
        case "ls":
            ls_parser = ArgumentParser()
            ls_parser.add_argument("--sort", action="store_true", help="Sort by length")
            ls_parser.add_argument("-n", type=int, help="Limit to the n first")
            ls_args = ls_parser.parse_args(remaining_args)
            items = [LsItem.from_node(n, Path()) for n in nodes]
            n = ls_args.n or len(items)
            items = items[:n]
            if ls_args.sort:
                items.sort(key=lambda item: -item.length)
            else:
                items.sort(key=lambda item: item.name)
            print(f"{n}/{len(nodes)} {target}")
            print(present_nodes(items, target))


if __name__ == "__main__":
    main()
