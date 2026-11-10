#!/usr/bin/env python3
"""Shelfwright product-qa: mechanical pre-launch checks for a digital product.

Usage:
    python qa_check.py PATH [--out qa-report.md] [--listing listing.md] [--max-mb 50] [--skip-content GLOB]

PATH is a folder or a .zip (the file the buyer will download).
Standard library only. Makes no network calls: external links are listed, not tested.
Exit code: 0 = no blockers, 1 = blockers found, 2 = bad input.
"""
import argparse
import fnmatch
import os
import re
import sys
import zipfile
from datetime import date

TEXT_EXT = {".md", ".txt", ".html", ".htm", ".csv", ".json", ".py", ".js", ".css",
            ".svg", ".yaml", ".yml", ".ps1", ".sh", ".xml", ".toml", ".ini"}
LINK_EXT = {".md", ".html", ".htm", ".svg", ".xml"}
JUNK_NAMES ={".ds_store", "thumbs.db", "desktop.ini"}
JUNK_DIRS = {"__macosx", "__pycache__", ".git", "node_modules", ".idea", ".vscode"}
PLACEHOLDER_RE = re.compile(r"lorem ipsum|\bTODO\b|\bFIXME\b|\bTBD\b|\[ASK USER|xxx+|<insert|\{\{\s*\w+\s*\}\}",
                            re.IGNORECASE)
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|"
                       r"-----BEGIN [A-Z ]*PRIVATE KEY-----|api[_-]?key\s*[:=]\s*['\"][^'\"]{12,})")
# (?!<) skips documentation placeholders such as C:\Users\<you> or /home/<user>/
# [U] and [h] are plain letters; written this way so the pattern doesn't match its own source text.
LOCAL_PATH_RE = re.compile(r"[A-Za-z]:\\[U]sers\\(?!<)[^\\\s]+|/[U]sers/(?!<)[^/\s]+/|/[h]ome/(?!<)[^/\s]+/")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HTML_LINK_RE = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)\"'<>\]]+")
BAD_NAME_RE = re.compile(r"[<>:\"|?*]|\s{2,}|^\s|\s$|\(\d+\)\.\w+$|copy( \d+)?\.\w+$|final[_ -]?(v?\d+|final)",
                         re.IGNORECASE)


def clean_url(u):
    """Drop escape sequences copied from source code (e.g. a literal backslash-n) and trailing punctuation."""
    u = u.split("\\", 1)[0]
    return u.rstrip(".,;:!?`*_'\"")


def load_files(path):
    """Return list of (relpath, bytes) for every file in a folder or zip."""
    files = []
    if os.path.isdir(path):
        for root, dirs, names in os.walk(path):
            for n in names:
                full = os.path.join(root, n)
                rel = os.path.relpath(full, path).replace(os.sep, "/")
                with open(full, "rb") as fh:
                    files.append((rel, fh.read()))
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if not info.is_dir():
                    files.append((info.filename, z.read(info)))
    else:
        raise ValueError("not a folder or .zip: " + path)
    return files


def check(files, listing_text=None, max_mb=50, content_ignore=()):
    blockers, warns, oks, links = [], [], [], set()
    names = {rel for rel, _ in files}
    lower_names = {os.path.basename(r).lower() for r in names}
    lower_rel = {r.lower() for r in names}

    if not files:
        blockers.append("Package is empty.")
        return blockers, warns, oks, links

    # Top-level essentials
    if not any(n.startswith("readme") for n in lower_names):
        blockers.append("No README found. Buyers need a starting point.")
    else:
        oks.append("README present.")
    if not any(n.startswith(("license", "licence")) for n in lower_names):
        blockers.append("No LICENSE/LICENCE file. State what the buyer may and may not do.")
    else:
        oks.append("Licence file present.")

    # Single top folder is fine; many loose files at top is a warning
    top = {r.split("/")[0] for r in names}
    if len(top) > 12:
        warns.append(f"{len(top)} items at the top level. Consider one folder with a README.")

    total = 0
    for rel, data in files:
        base = os.path.basename(rel)
        parts = [p.lower() for p in rel.split("/")]
        ext = os.path.splitext(base)[1].lower()
        total += len(data)

        if base.lower() in JUNK_NAMES or any(p in JUNK_DIRS for p in parts[:-1]) or base.startswith("~$"):
            blockers.append(f"Junk/system file shipped: `{rel}`")
            continue
        if len(data) == 0:
            blockers.append(f"Empty file: `{rel}`")
        if len(data) > max_mb * 1024 * 1024:
            warns.append(f"Large file ({len(data) / 1048576:.1f} MB): `{rel}`")
        if BAD_NAME_RE.search(base):
            warns.append(f"Messy file name: `{rel}` (copy/final/(1)/odd characters/extra spaces)")
        if len(rel) > 150:
            warns.append(f"Very long path ({len(rel)} chars) may fail to unzip on Windows: `{rel}`")
        if base.startswith(".") and base.lower() not in {".gitkeep", ".gitignore"}:
            warns.append(f"Hidden file: `{rel}`")

        if ext in TEXT_EXT:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = data.decode("utf-8", errors="replace")
                warns.append(f"Not valid UTF-8 (odd characters may show): `{rel}`")
            if any(fnmatch.fnmatch(rel, g) for g in content_ignore):
                continue
            for m in PLACEHOLDER_RE.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                warns.append(f"Placeholder `{m.group(0)}` in `{rel}` line {line}")
                break
            if SECRET_RE.search(text):
                blockers.append(f"Possible API key / secret in `{rel}`. Remove it.")
            if LOCAL_PATH_RE.search(text):
                warns.append(f"Personal local path in `{rel}` (e.g. a username). Use a relative path.")
            # Links
            folder = os.path.dirname(rel)
            # Only markup files have real links; in code, link-like text is usually a regex or a string.
            targets = MD_LINK_RE.findall(text) + HTML_LINK_RE.findall(text) if ext in LINK_EXT else []
            for target in targets:
                if target.startswith(("http://", "https://")):
                    links.add(clean_url(target))
                    continue
                if target.startswith(("#", "mailto:", "data:", "javascript:")):
                    continue
                t = target.split("#")[0].split("?")[0]
                if not t:
                    continue
                resolved = os.path.normpath(os.path.join(folder, t)).replace(os.sep, "/")
                if resolved.lower() not in lower_rel and not any(
                        r.lower().startswith(resolved.lower() + "/") for r in names):
                    blockers.append(f"Broken local link in `{rel}`: `{target}`")
            for u in URL_RE.findall(text):
                links.add(clean_url(u))

    oks.append(f"{len(files)} files, {total / 1048576:.2f} MB total.")

    if listing_text:
        for m in re.finditer(r"`([^`]+\.[A-Za-z0-9]{1,5})`", listing_text):
            fname = os.path.basename(m.group(1)).lower()
            if fname not in lower_names:
                blockers.append(f"Listing mentions `{m.group(1)}` but it is not in the package.")
        oks.append("Listing file names cross-checked (names in `backticks` only).")

    return blockers, warns, oks, sorted(links)


def report(path, blockers, warns, oks, links):
    verdict = "NOT READY" if blockers else "READY AFTER MANUAL PASS"
    out = [f"# QA report: {os.path.basename(os.path.normpath(path))}",
           f"_Generated {date.today().isoformat()} by product-qa/qa_check.py_", "",
           f"**Verdict (script only):** {verdict} - {len(blockers)} blocker(s), {len(warns)} warning(s)", "",
           "## Blockers"] + ([f"- {b}" for b in blockers] or ["- none"])
    out += ["", "## Warnings"] + ([f"- {w}" for w in warns] or ["- none"])
    out += ["", "## Passed"] + [f"- {o}" for o in oks]
    out += ["", "## External links (not checked by this script)"] + ([f"- {u}" for u in links] or ["- none"])
    out += ["", "## Manual pass", "_Fill in from checklists/manual-qa.md_", ""]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pre-launch QA for a digital product folder or zip.")
    ap.add_argument("path", help="product folder or .zip")
    ap.add_argument("--out", default="qa-report.md", help="report file to write (default qa-report.md)")
    ap.add_argument("--listing", help="optional listing.md to cross-check file names")
    ap.add_argument("--max-mb", type=float, default=50, help="warn above this file size (MB)")
    ap.add_argument("--skip-content", action="append", default=[], metavar="GLOB",
                    help="skip text and link checks for files matching GLOB (repeatable), "
                         "e.g. checklists that mention placeholder words on purpose")
    a = ap.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):  # never crash on odd characters in a Windows console/pipe
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    try:
        files = load_files(a.path)
    except (ValueError, OSError, zipfile.BadZipFile) as e:
        print("error:", e, file=sys.stderr)
        return 2
    listing = None
    if a.listing:
        with open(a.listing, encoding="utf-8-sig", errors="replace") as fh:
            listing = fh.read()
    b, w, o, l = check(files, listing, a.max_mb, a.skip_content)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(report(a.path, b, w, o, l))
    print(f"{len(b)} blocker(s), {len(w)} warning(s). Report: {a.out}")
    return 1 if b else 0


if __name__ == "__main__":
    sys.exit(main())
