import json
from pathlib import Path

import joblog.__main__ as app


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
