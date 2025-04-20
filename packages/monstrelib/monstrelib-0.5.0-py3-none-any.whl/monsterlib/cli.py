import argparse
import logging

from . import __version__
from .core import add, subtract


def main():
    parser = argparse.ArgumentParser(description="🧠 Calculatrice MonsterLib")
    parser.add_argument(
        "--version", action="version", version=f"MonsterLib v{__version__}"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Afficher les logs détaillés"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ADD
    parser_add = subparsers.add_parser("add", help="Additionne deux nombres")
    parser_add.add_argument("a", type=float)
    parser_add.add_argument("b", type=float)
    parser_add.add_argument("--as-int", action="store_true", help="Retourne un entier")

    # SUBTRACT
    parser_sub = subparsers.add_parser("subtract", help="Soustrait deux nombres")
    parser_sub.add_argument("a", type=float)
    parser_sub.add_argument("b", type=float)
    parser_sub.add_argument("--as-int", action="store_true", help="Retourne un entier")

    args = parser.parse_args()

    # Logging si --verbose
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Arguments reçus : %s", args)

    # Logique principale
    result = None
    if args.command == "add":
        result = add(args.a, args.b)
    elif args.command == "subtract":
        result = subtract(args.a, args.b)
    else:
        parser.print_help()
        return

    # Format de sortie
    if hasattr(args, "as_int") and args.as_int:
        result = int(result)

    print(result)


# Compatible python -m monsterlib.cli
if __name__ == "__main__" or __name__ == "monsterlib.cli":
    main()
