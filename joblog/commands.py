import argparse
from collections import Counter

from .storage import load_data, save_data


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


def cmd_list(_: argparse.Namespace) -> None:
    data = load_data()
    items = data["items"]
    if not items:
        print("No applications yet.")
        return

    for it in items:
        print(f"[{it['id']}] {it['company']} | {it['role']} | {it['status']} | {it['date']}")


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


def cmd_stats(_: argparse.Namespace) -> None:
    data = load_data()
    items = data["items"]
    if not items:
        print("No applications yet.")
        return

    counts = Counter(it["status"] for it in items)
    total = len(items)

    print(f"Total: {total}")
    for status in ["applied", "interview", "offer", "rejected"]:
        print(f"{status}: {counts.get(status, 0)}")


def cmd_search(args: argparse.Namespace) -> None:
    data = load_data()
    items = data["items"]

    q_company = (args.company or "").lower().strip()
    q_role = (args.role or "").lower().strip()

    results = []
    for it in items:
        ok = True
        if q_company and q_company not in it["company"].lower():
            ok = False
        if q_role and q_role not in it["role"].lower():
            ok = False
        if ok:
            results.append(it)

    if not results:
        print("No matching applications.")
        return

    for it in results:
        print(f"[{it['id']}] {it['company']} | {it['role']} | {it['status']} | {it['date']}")
