Exit code: 0
Wall time: 0.2 seconds
Output:
"""Record a user's approval for the current rendered recap proxy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from render_proxy import plan_fingerprint, proxy_render_record, sha256_file


def approve_proxy(job_root: Path) -> Path:
    job_root = Path(job_root).resolve()
    proxy = job_root / "build" / "proxy.mp4"
    if not proxy.is_file():
        raise FileNotFoundError("proxy approval requires build/proxy.mp4")
    current_record = proxy_render_record(proxy, plan_fingerprint(job_root))
    manifest_path = job_root / "build" / "proxy-render.json"
    if not manifest_path.is_file():
        raise ValueError("proxy render manifest is missing; rerender the proxy before approval")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("proxy render manifest is invalid; rerender the proxy before approval") from error
    if manifest != current_record:
        raise ValueError("proxy render manifest is stale; rerender the proxy before approval")
    approval_path = job_root / "build" / "proxy-approval.json"
    approval_path.write_text(json.dumps(current_record, indent=2) + "\n", encoding="utf-8")
    return approval_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("job_root", type=Path)
    args = parser.parse_args()
    print(approve_proxy(args.job_root))


if __name__ == "__main__":
    main()

