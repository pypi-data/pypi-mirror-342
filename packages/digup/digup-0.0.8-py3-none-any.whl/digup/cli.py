from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent

from digup.commands import run_wc, run_hi, run_ls


def main():
    parser = ArgumentParser(add_help=True)

    common_args_parser = ArgumentParser(add_help=False)
    common_args_parser.add_argument(
        type=Path,
        nargs="*",
        dest="file_or_dirs",
        default=[Path()],
        help="Source file or directory",
    )
    common_args_parser.add_argument(
        "--target",
        "-t",
        choices=["function", "class", "module"],
        default="modules",
    )
    common_args_parser.add_argument(
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
    shorthands = common_args_parser.add_mutually_exclusive_group()
    shorthands.add_argument(
        "--function",
        "-f",
        nargs="?",
        default=None,
        const="",
        help="""\
        Shorthand for `-t function -s SEARCH`. 
        It override their values.
        """,
    )
    shorthands.add_argument(
        "--class",
        "-c",
        nargs="?",
        default=None,
        const="",
        help="""\
        Shorthand for `-t classe -s SEARCH`.
        It override their values.
        """,
    )

    subparsers = parser.add_subparsers()

    wc_parser = subparsers.add_parser("wc", parents=[common_args_parser], help="Count the words in functions")
    wc_parser.add_argument("--aggregate", action="store_true")
    wc_parser.add_argument("-n", type=int, help="Limit to the n first")
    wc_parser.set_defaults(command_handler=run_wc)

    hi_parser = subparsers.add_parser("hi", parents=[common_args_parser], help="Highlight the identifiers in functions")
    hi_parser.add_argument("--word", "-w", type=str, nargs="*", default=None)
    hi_parser.add_argument("--params-only", "-p", action="store_true", default=False)
    hi_limits = hi_parser.add_mutually_exclusive_group()
    hi_limits.add_argument("--least", type=int, help="Highlight only the n least common identifiers")
    hi_limits.add_argument("--most", type=int, help="Highlight only the n most common identifiers")
    hi_limits.add_argument("--first", type=int, help="Highlight only the n first identifiers")
    hi_limits.add_argument("--last", type=int, help="Highlight only the n last identifiers")
    hi_parser.set_defaults(command_handler=run_hi)

    ls_parser = subparsers.add_parser("ls", parents=[common_args_parser], help="List the items")
    ls_parser.add_argument("--sort", action="store_true", help="Sort by length")
    ls_parser.add_argument("-n", type=int, help="Limit to the n first")
    ls_parser.set_defaults(command_handler=run_ls)

    args = parser.parse_args()

    # Handle -f shorthand
    if args.function is not None:
        args.target = "functions"
        args.search = args.function

    # Handle -c shorthand
    if getattr(args, "class") is not None:
        args.target = "classes"
        args.search = getattr(args, "class")

    # Call the command
    command_handler = args.command_handler
    delattr(args, "class")
    delattr(args, "function")
    delattr(args, "command_handler")
    command_handler(args)


if __name__ == "__main__":
    main()
