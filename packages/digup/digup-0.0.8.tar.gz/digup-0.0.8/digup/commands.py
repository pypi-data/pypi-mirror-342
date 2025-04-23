from pathlib import Path

from digup.count_words import word_count
from digup.limits import LeastN, MostN, FirstN, LastN, NoLimit
from digup.present import present_word_count, present_aggregation, present_nodes, LsItem
from digup.highlight import highlight_identifiers, present_highlights
from digup.get_nodes import get_functions, get_classes, get_modules, Node
from digup.aggregation import Aggregation


def run_wc(args):
    # TODO : assert with a typeddict
    nodes = _get_nodes(args.file_or_dirs, args.search, args.target)
    aggregate = args.aggregate or (args.target == "modules")
    limit_to = args.n or 1_000_000_000
    if aggregate:
        word_counts = [word_count(n.definition, n.length) for n in nodes]
        print(f"{len(nodes)} {args.target}")
        if len(nodes) < 5:
            for node in nodes:
                print(node.location)
        print(present_aggregation(Aggregation.of(word_counts), limit_to=limit_to))
    else:
        for node in nodes:
            print(f"{node.location}")
            print(
                present_word_count(word_count(node.definition, node.length).sorted_by_occurences().limit_to(limit_to))
            )


def run_hi(args):
    # TODO : assert with a typeddict
    nodes = _get_nodes(args.file_or_dirs, args.search, args.target)
    words = set(args.word) if args.word is not None else None
    limit = _get_limit(args)

    for node in nodes:
        print(f"{node.location} ")
        print(
            present_highlights(
                highlight_identifiers(node.source, limit=limit, only=words, params_only=args.params_only), node.source
            )
        )


def _get_limit(args):
    if args.least:
        limit = LeastN(args.least)
    elif args.most:
        limit = MostN(args.most)
    elif args.first:
        limit = FirstN(args.first)
    elif args.last:
        limit = LastN(args.last)
    else:
        limit = NoLimit()
    return limit


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
