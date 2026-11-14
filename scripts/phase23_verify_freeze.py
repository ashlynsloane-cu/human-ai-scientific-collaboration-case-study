"""Validate private frozen Phase 23 membership snapshot without altering it."""
import csv
import hashlib
from collections import Counter
from pathlib import Path


def verify_snapshot(ledger_path, include_path, exclude_path, manifest):
    ledger_path, include_path, exclude_path = map(Path, (ledger_path,include_path,exclude_path))
    with ledger_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 597 or len(set(r["conversation_id"] for r in rows)) != 597:
        raise ValueError("wrong number or duplicate conversation identifiers")
    counts = Counter(r["phase20_effective_label"] for r in rows)
    if counts != {"include":245,"exclude":352}:
        raise ValueError("invalid label counts")
    for label, path, hash_key, num in (
        ("include",include_path,"locked_roster_sha256",245),
        ("exclude",exclude_path,"locked_exclusion_roster_sha256",352),
    ):
        if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest[hash_key]:
            raise ValueError("frozen roster checksum mismatch")
        with path.open(newline="") as f:
            rr=list(csv.DictReader(f))
        if len(rr)!=num or [r["conversation_id"] for r in rr]!=sorted(r["conversation_id"] for r in rows if r["phase20_effective_label"]==label):
            raise ValueError("roster membership mismatch")
    if hashlib.sha256(ledger_path.read_bytes()).hexdigest()!=manifest["locked_full_ledger_sha256"]:
        raise ValueError("baseline ledger checksum mismatch")
    return counts
