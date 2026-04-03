#!/usr/bin/env python3
import argparse
import difflib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class CasePair:
    key: str
    input_path: Path
    expected_path: Path


def is_text_case_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in {".txt", ".in", ".out"}


def split_role_and_suffix(stem: str) -> Tuple[Optional[str], Optional[str]]:
    lowered = stem.lower()
    for role in ("input", "output", "expected"):
        if lowered.startswith(role):
            return role, stem[len(role) :]
    return None, None


def normalize_suffix(suffix: str) -> str:
    trimmed = suffix.strip("_- .")
    return re.sub(r"[^a-zA-Z0-9]+", "", trimmed).lower()


def numeric_canonical(key: str) -> Optional[str]:
    m = re.fullmatch(r"(\d+)", key)
    if not m:
        return None
    return str(int(m.group(1)))


def discover_io_files(target_dir: Path) -> Tuple[Dict[str, List[Path]], Dict[str, List[Path]]]:
    inputs: Dict[str, List[Path]] = {}
    outputs: Dict[str, List[Path]] = {}
    for path in target_dir.rglob("*"):
        if not is_text_case_file(path):
            continue
        role, suffix = split_role_and_suffix(path.stem)
        if role is None or suffix is None:
            continue
        key = normalize_suffix(suffix)
        if not key:
            continue
        if role == "input":
            inputs.setdefault(key, []).append(path)
        else:
            outputs.setdefault(key, []).append(path)
    return inputs, outputs


def choose_best_output(inp: Path, candidates: List[Path]) -> Path:
    inp_parts = set(inp.parent.parts)
    best = candidates[0]
    best_score = -10**9
    for cand in candidates:
        cand_parts = set(cand.parent.parts)
        overlap = len(inp_parts & cand_parts)
        dist = abs(len(inp.parent.parts) - len(cand.parent.parts))
        score = overlap * 10 - dist
        if score > best_score:
            best_score = score
            best = cand
    return best


def build_case_pairs(target_dir: Path) -> List[CasePair]:
    inputs, outputs = discover_io_files(target_dir)
    pairs: List[CasePair] = []
    used_outputs: set[Path] = set()

    output_by_numeric: Dict[str, List[Path]] = {}
    for k, v in outputs.items():
        n = numeric_canonical(k)
        if n is not None:
            output_by_numeric.setdefault(n, []).extend(v)

    for key in sorted(inputs.keys()):
        out_candidates = outputs.get(key, [])
        if not out_candidates:
            n = numeric_canonical(key)
            if n is not None:
                out_candidates = output_by_numeric.get(n, [])
        if not out_candidates:
            continue
        for inp in sorted(inputs[key]):
            out = choose_best_output(inp, out_candidates)
            if out in used_outputs:
                continue
            used_outputs.add(out)
            pairs.append(CasePair(key=key, input_path=inp, expected_path=out))
    return pairs


def choose_source_file(target_dir: Path, explicit: Optional[str]) -> Path:
    if explicit:
        src = target_dir / explicit
        if not src.exists():
            raise FileNotFoundError(f"source file not found: {src}")
        return src

    cpp_files = sorted(target_dir.glob("*.cpp"))
    if not cpp_files:
        raise FileNotFoundError(f"no .cpp files found in {target_dir}")

    preferred = target_dir / f"{target_dir.name}.cpp"
    if preferred in cpp_files and has_main_function(preferred):
        return preferred

    if len(cpp_files) == 1:
        return cpp_files[0]

    with_main = [p for p in cpp_files if has_main_function(p)]
    if len(with_main) == 1:
        return with_main[0]
    if preferred in with_main:
        return preferred

    filtered = [p for p in cpp_files if not re.search(r"(test|case|tri|tr)", p.stem, re.IGNORECASE)]
    if len(filtered) == 1:
        return filtered[0]

    raise RuntimeError(
        "multiple .cpp files found; please specify one with --source. "
        f"Candidates: {', '.join(p.name for p in cpp_files)}"
    )


def has_main_function(path: Path) -> bool:
    content = path.read_text(encoding="utf-8", errors="replace")
    return re.search(r"\bint\s+main\s*\(", content) is not None


def compile_source(source: Path, target_dir: Path, binary_name: str) -> Path:
    out = target_dir / binary_name
    cmd = ["g++", "-std=c++17", str(source), "-O2", "-o", str(out)]
    cp = subprocess.run(cmd, capture_output=True, text=True, cwd=str(target_dir))
    if cp.returncode != 0:
        raise RuntimeError(f"compile failed:\n{cp.stderr}")
    return out


def read_normalized_lines(path: Path, ignore_blank_lines: bool) -> List[str]:
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    if ignore_blank_lines:
        lines = [line for line in lines if line != ""]
    return lines


def run_one_case(
    binary: Path, case: CasePair, actual_path: Path, cwd: Path, ignore_blank_lines: bool
) -> Tuple[bool, str]:
    with case.input_path.open("r", encoding="utf-8", errors="replace") as fin, actual_path.open(
        "w", encoding="utf-8"
    ) as fout:
        proc = subprocess.run([str(binary)], stdin=fin, stdout=fout, stderr=subprocess.STDOUT, cwd=str(cwd))
    if proc.returncode != 0:
        return False, f"program exited with code {proc.returncode}"

    actual_lines = read_normalized_lines(actual_path, ignore_blank_lines)
    expected_lines = read_normalized_lines(case.expected_path, ignore_blank_lines)
    if actual_lines == expected_lines:
        return True, ""

    diff = "\n".join(
        difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile=str(case.expected_path),
            tofile=str(actual_path),
            lineterm="",
            n=2,
        )
    )
    return False, diff


def main() -> int:
    parser = argparse.ArgumentParser(description="Run C++ tests for lab/PA folders with flexible structures.")
    parser.add_argument("target", help="target directory, e.g. pa2 or lab3")
    parser.add_argument("--source", help="explicit source .cpp filename inside target directory")
    parser.add_argument("--keep-binary", action="store_true", help="do not delete compiled binary after testing")
    parser.add_argument("--show-pass", action="store_true", help="print each passing case")
    parser.add_argument(
        "--strict-whitespace",
        action="store_true",
        help="do not ignore blank lines and trailing spaces while comparing outputs",
    )
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    if not target_dir.is_dir():
        print(f"target directory not found: {target_dir}")
        return 1

    try:
        source = choose_source_file(target_dir, args.source)
    except Exception as e:
        print(f"source selection error: {e}")
        return 1

    binary_name = ".autotest_bin"
    binary_path = target_dir / binary_name
    try:
        binary = compile_source(source, target_dir, binary_name)
    except Exception as e:
        print(str(e))
        return 1

    cases = build_case_pairs(target_dir)
    if not cases:
        print("no matched input/output case pairs found")
        if binary_path.exists() and not args.keep_binary:
            binary_path.unlink()
        return 1

    print(f"source: {source.name}")
    print(f"detected cases: {len(cases)}")

    passed = 0
    for i, case in enumerate(cases, start=1):
        actual_path = case.input_path.parent / f"actual_{case.input_path.name}"
        ok, info = run_one_case(binary, case, actual_path, target_dir, not args.strict_whitespace)
        if ok:
            passed += 1
            if args.show_pass:
                print(f"[PASS {i:02d}] {case.input_path.name} -> {case.expected_path.name}")
        else:
            print(f"[FAIL {i:02d}] {case.input_path} -> {case.expected_path}")
            if info:
                print(info)

    print(f"result: {passed}/{len(cases)} passed, {len(cases) - passed} failed")

    if binary_path.exists() and not args.keep_binary:
        binary_path.unlink()
    return 0 if passed == len(cases) else 2


if __name__ == "__main__":
    sys.exit(main())
