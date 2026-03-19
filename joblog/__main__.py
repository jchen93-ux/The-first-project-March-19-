import argparse
from datetime import date

from .commands import cmd_add, cmd_list, cmd_search, cmd_stats, cmd_update


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="joblog", description="Track job applications.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add an application.")
    p_add.add_argument("--company", required=True)
    p_add.add_argument("--role", required=True)
    p_add.add_argument("--status", required=True, choices=["applied", "interview", "offer", "rejected"])
    p_add.add_argument("--date", default=str(date.today()))
    p_add.add_argument("--notes", default="")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List applications.")
    p_list.set_defaults(func=cmd_list)

    p_update = sub.add_parser("update", help="Update an application by id.")
    p_update.add_argument("--id", type=int, required=True)
    p_update.add_argument("--status", choices=["applied", "interview", "offer", "rejected"])
    p_update.add_argument("--notes")
    p_update.set_defaults(func=cmd_update)

    p_stats = sub.add_parser("stats", help="Show status counts.")
    p_stats.set_defaults(func=cmd_stats)

    p_search = sub.add_parser("search", help="Search applications.")
    p_search.add_argument("--company")
    p_search.add_argument("--role")
    p_search.set_defaults(func=cmd_search)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
