import json
from pathlib import Path

import joblog.commands as app
import joblog.storage as storage

def test_load_data_when_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = app.load_data()
    assert data["next_id"] == 1
    assert data["items"] == []


def test_add_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    args = type("Args", (), {})()
    args.company = "Amazon"
    args.role = "SDE"
    args.status = "applied"
    args.date = "2026-03-19"
    args.notes = ""

    app.cmd_add(args)

    p = Path("joblog.json")
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["next_id"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["company"] == "Amazon"


def test_update_changes_status_and_notes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    add_args = type("Args", (), {})()
    add_args.company = "TestCo"
    add_args.role = "Backend"
    add_args.status = "applied"
    add_args.date = "2026-03-19"
    add_args.notes = "first"
    app.cmd_add(add_args)

    upd_args = type("Args", (), {})()
    upd_args.id = 1
    upd_args.status = "interview"
    upd_args.notes = "phone"
    app.cmd_update(upd_args)

    data = json.loads(Path("joblog.json").read_text(encoding="utf-8"))
    item = data["items"][0]
    assert item["status"] == "interview"
    assert item["notes"] == "phone"


def test_update_unknown_id_does_not_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    upd_args = type("Args", (), {})()
    upd_args.id = 999
    upd_args.status = "offer"
    upd_args.notes = "x"
    app.cmd_update(upd_args)

    out = capsys.readouterr().out
    assert "not found" in out.lower()

def test_stats_outputs_counts(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    a1 = type("Args", (), {})()
    a1.company = "A"
    a1.role = "R"
    a1.status = "applied"
    a1.date = "2026-03-19"
    a1.notes = ""
    app.cmd_add(a1)

    a2 = type("Args", (), {})()
    a2.company = "B"
    a2.role = "R"
    a2.status = "interview"
    a2.date = "2026-03-19"
    a2.notes = ""
    app.cmd_add(a2)

    app.cmd_stats(type("Args", (), {})())
    out = capsys.readouterr().out.lower()
    assert "total: 2" in out
    assert "applied: 1" in out
    assert "interview: 1" in out


def test_search_filters_by_company(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    a1 = type("Args", (), {})()
    a1.company = "Amazon"
    a1.role = "SDE"
    a1.status = "applied"
    a1.date = "2026-03-19"
    a1.notes = ""
    app.cmd_add(a1)

    a2 = type("Args", (), {})()
    a2.company = "Google"
    a2.role = "SWE"
    a2.status = "applied"
    a2.date = "2026-03-19"
    a2.notes = ""
    app.cmd_add(a2)

    args = type("Args", (), {})()
    args.company = "ama"
    args.role = None
    capsys.readouterr()
    app.cmd_search(args)

    out = capsys.readouterr().out
    assert "Amazon" in out
    assert "Google" not in out
