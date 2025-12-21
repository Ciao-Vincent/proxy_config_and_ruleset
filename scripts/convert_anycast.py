#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("Usage: convert_anycast.py <input_file> <output_file>")
        sys.exit(2)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    ip_list = []
    # 示例行：ip-cidr, 1.0.0.0/24, Anycast
    pattern = re.compile(r'^\s*(ip-cidr|ip6-cidr)\s*,\s*([^,\s]+)\s*,\s*Anycast\s*$', re.IGNORECASE)

    for line in input_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        m = pattern.match(line)
        if not m:
            # 不符合格式的行直接跳过（也可改成报错）
            continue
        ip_list.append(m.group(1))

    data = {
        "version": 4,
        "rules": [
            {
                "ip_cidr": ip_list
            }
        ]
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
