import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


DATA_PATH = Path("joblog.json")


def load_data() -> dict[str, Any]:
    if not DATA_PATH.exists():
        return {"next_id": 1, "items": []}
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_data(data: dict[str, Any]) -> None:
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_add(args: argparse.Namespace) -> None:
    data = load_data()
    item = {
        "id": data["next_id"],
        "company": args.company,
        "role": args.role,
        "status": args.status,
        "date": args.date,
        "notes": args.notes,
    }
    data["items"].append(item)
    data["next_id"] += 1
    save_data(data)
    print(f"Added application id={item['id']} ({item['company']} - {item['role']})")


def cmd_update(args: argparse.Namespace) -> None:
    data = load_data()
    items = data["items"]

    target = None
    for it in items:
        if it["id"] == args.id:
            target = it
            break

    if target is None:
        print(f"Application id={args.id} not found.")
        return

    if args.status is not None:
        target["status"] = args.status
    if args.notes is not None:
        target["notes"] = args.notes

    save_data(data)
    print(f"Updated application id={args.id}")



def cmd_list(_: argparse.Namespace) -> None:
    data = load_data()
    items = data["items"]
    if not items:
        print("No applications yet.")
        return

    for it in items:
        print(f"[{it['id']}] {it['company']} | {it['role']} | {it['status']} | {it['date']}")


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
    p_update.add_argument("--status", choices=["applied", "interview", "offer","rejected"])
    p_update.add_argument("--notes")
    p_update.set_defaults(func=cmd_update)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
