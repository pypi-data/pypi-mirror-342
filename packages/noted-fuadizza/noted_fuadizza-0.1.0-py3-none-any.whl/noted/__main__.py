# noted/__main__.py

import json
import argparse
import os

DATA_FILE = os.path.expanduser("~/.noted.json")  # simpan di home

def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def list_notes():
    notes = load_notes()
    if not notes:
        print("Belum ada catatan.")
        return
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")

def add_note(content):
    notes = load_notes()
    notes.append(content)
    save_notes(notes)
    print("Catatan ditambahkan.")

def delete_note(index):
    notes = load_notes()
    if 0 <= index < len(notes):
        removed = notes.pop(index)
        save_notes(notes)
        print(f"Catatan dihapus: {removed}")
    else:
        print("Indeks tidak valid.")

def update_note(index, content):
    notes = load_notes()
    if 0 <= index < len(notes):
        notes[index] = content
        save_notes(notes)
        print("Catatan diperbarui.")
    else:
        print("Indeks tidak valid.")

def main():
    parser = argparse.ArgumentParser(description="CLI sederhana untuk mencatat.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="Lihat semua catatan")

    add_parser = subparsers.add_parser("add", help="Tambah catatan")
    add_parser.add_argument("content", help="Isi catatan")

    del_parser = subparsers.add_parser("delete", help="Hapus catatan")
    del_parser.add_argument("index", type=int, help="Indeks catatan (mulai dari 1)")

    upd_parser = subparsers.add_parser("update", help="Ubah catatan")
    upd_parser.add_argument("index", type=int, help="Indeks catatan (mulai dari 1)")
    upd_parser.add_argument("content", help="Isi baru catatan")

    args = parser.parse_args()

    if args.command == "list":
        list_notes()
    elif args.command == "add":
        add_note(args.content)
    elif args.command == "delete":
        delete_note(args.index - 1)
    elif args.command == "update":
        update_note(args.index - 1, args.content)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

