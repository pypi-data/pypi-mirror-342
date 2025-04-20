from pathlib import Path

from src.colors import LINEAR_COLORS
from src.count_words import word_count
from src.present import present_word_count, present_aggregation, present_nodes, LsItem
from src.highlight_identifiers import highlight_identifiers
from src.get_nodes import get_functions, get_classes, get_modules, Node
from src.aggregation import Aggregation


def run_wc(args):
    # TODO : assert with a typeddict
    nodes = _get_nodes(args.file_or_dirs, args.search, args.target)
    aggregate = args.aggregate or (args.target == "modules")
    if aggregate:
        word_counts = [word_count(n.definition, n.length) for n in nodes]
        print(f"{len(nodes)} {args.target}")
        if len(nodes) < 5:
            for node in nodes:
                print(node.location)
        print(present_aggregation(Aggregation.of(word_counts)))
    else:
        for node in nodes:
            print(f"{node.location}")
            print(present_word_count(word_count(node.definition, node.length).sorted_by_occurences()))


def run_hi(args):
    # TODO : assert with a typeddict
    nodes = _get_nodes(args.file_or_dirs, args.search, args.target)
    words = set(args.word) if args.word is not None else None

    for node in nodes:
        print(f"{node.location} ")
        print(highlight_identifiers(node.source, LINEAR_COLORS, words, params_only=args.params_only))


def run_ls(args):
    # TODO : assert with a typeddict
    nodes = _get_nodes(args.file_or_dirs, args.search, args.target)
    items = [LsItem.from_node(n, Path()) for n in nodes]
    n = args.n or len(items)
    if args.sort:
        items.sort(key=lambda item: -item.length)
    else:
        items.sort(key=lambda item: item.name)
    items = items[:n]
    print(f"{n}/{len(nodes)} {args.target}")
    print(present_nodes(items, args.target))


def _get_nodes(file_or_dirs: list[Path], search: str, target: str) -> list[Node]:
    match target:
        case "functions":
            return list(get_functions(file_or_dirs, search))
        case "classes":
            return list(get_classes(file_or_dirs, search))
        case _:  # "modules"
            return list(get_modules(file_or_dirs, search))
