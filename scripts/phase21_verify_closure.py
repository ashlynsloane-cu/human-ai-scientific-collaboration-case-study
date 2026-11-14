import csv, hashlib, json, pathlib

def check_ledger(rows):
    ids = [r["conversation_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source conversation")
    if len(rows) != 597:
        raise ValueError("Population mismatch")
    labels = [r["phase20_effective_label"] for r in rows]
    if labels.count("include") != 245 or labels.count("exclude") != 352 or set(labels) - {"include", "exclude"}:
        raise ValueError("Classification mismatch")
    return {"total": len(rows), "include": labels.count("include"), "exclude": labels.count("exclude")}

def verify_shards(root, expected_csv):
    with open(expected_csv, newline="") as f:
        manifest = list(csv.DictReader(f))
    for r in manifest:
        b = (pathlib.Path(root) / r["filename"]).read_bytes()
        if len(b) != int(r["size_bytes"]) or hashlib.sha256(b).hexdigest() != r["sha256"]:
            raise ValueError("Source shard mismatch: " + r["filename"])
    return len(manifest)
