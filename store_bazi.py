"""
store_bazi.py
八字命盘本地存储管理

存储路径: ~/.bazi_skill/profiles/
每个人一个 JSON 文件，文件名为 slug（拼音或自定义名称）

用法（CLI）:
  # 保存
  python store_bazi.py save --name "张三" --slug "zhangsan" --data '<json>'

  # 读取
  python store_bazi.py load --slug "zhangsan"

  # 列出所有
  python store_bazi.py list

  # 删除
  python store_bazi.py delete --slug "zhangsan"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

STORE_DIR = Path.home() / ".bazi_skill" / "profiles"


def _ensure_dir():
    STORE_DIR.mkdir(parents=True, exist_ok=True)


def _path(slug: str) -> Path:
    return STORE_DIR / f"{slug}.json"


def save(name: str, slug: str, data: dict, memo: str = "") -> dict:
    """保存命盘到本地文件"""
    _ensure_dir()
    record = {
        "name": name,
        "slug": slug,
        "memo": memo,
        "saved_at": datetime.now().isoformat(),
        "bazi_data": data,
    }
    path = _path(slug)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return {"status": "saved", "path": str(path), "name": name, "slug": slug}


def load(slug: str) -> dict:
    """读取指定命盘"""
    path = _path(slug)
    if not path.exists():
        return {"status": "not_found", "slug": slug}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_all() -> list:
    """列出所有已存储的命盘"""
    _ensure_dir()
    results = []
    for p in sorted(STORE_DIR.glob("*.json")):
        try:
            with open(p, encoding="utf-8") as f:
                rec = json.load(f)
            chart = rec.get("bazi_data", {}).get("original_chart", {})
            pillars = "".join([
                rec["bazi_data"]["original_chart"].get(k, {}).get("tian_gan", {}).get("value", "") +
                rec["bazi_data"]["original_chart"].get(k, {}).get("di_zhi", {}).get("value", "")
                for k in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]
            ]) if "bazi_data" in rec else ""
            results.append({
                "name": rec.get("name", ""),
                "slug": rec.get("slug", p.stem),
                "memo": rec.get("memo", ""),
                "saved_at": rec.get("saved_at", ""),
                "four_pillars": pillars,
                "ri_zhu": rec.get("bazi_data", {}).get("original_chart", {}).get("ri_zhu_tian_gan", ""),
            })
        except Exception:
            continue
    return results


def delete(slug: str) -> dict:
    """删除指定命盘"""
    path = _path(slug)
    if not path.exists():
        return {"status": "not_found", "slug": slug}
    path.unlink()
    return {"status": "deleted", "slug": slug}


# ── CLI 入口 ──────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="八字命盘存储管理")
    sub = parser.add_subparsers(dest="cmd")

    # save
    p_save = sub.add_parser("save")
    p_save.add_argument("--name", required=True)
    p_save.add_argument("--slug", required=True)
    p_save.add_argument("--data", required=True, help="calculate_bazi 输出的 JSON 字符串")
    p_save.add_argument("--memo", default="", help="备注（关系、用途等）")

    # load
    p_load = sub.add_parser("load")
    p_load.add_argument("--slug", required=True)

    # list
    sub.add_parser("list")

    # delete
    p_del = sub.add_parser("delete")
    p_del.add_argument("--slug", required=True)

    args = parser.parse_args()

    if args.cmd == "save":
        data = json.loads(args.data)
        result = save(args.name, args.slug, data, args.memo)
    elif args.cmd == "load":
        result = load(args.slug)
    elif args.cmd == "list":
        result = list_all()
    elif args.cmd == "delete":
        result = delete(args.slug)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
