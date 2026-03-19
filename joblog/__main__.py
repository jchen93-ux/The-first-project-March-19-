import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="joblog", description="Track job applications.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List applications (placeholder).")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "list":
        print("No applications yet. (placeholder)")


if __name__ == "__main__":
    main()

