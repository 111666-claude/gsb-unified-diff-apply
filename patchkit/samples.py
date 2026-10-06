"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "context":
        patch = "@@ -1,2 +1,2 @@\n a\n z\n"
        out = core.apply(["a", "b"], patch, core.Counter())
        _line({"status": out["status"], "lines": out["lines"]})
        return 0
    if name == "offset":
        patch = "@@ -1,1 +1,2 @@\n+x\n@@ -3,1 +4,1 @@\n-c\n+C\n"
        out = core.apply(["a", "b", "c"], patch, core.Counter())
        _line({"lines": out["lines"]})
        return 0
    if name == "len":
        patch = "@@ -1,5 +1,1 @@\n-a\n"
        out = core.apply(["a", "b"], patch, core.Counter())
        _line({"status": out["status"]})
        return 0
    if name == "work":
        source = ["l%04d" % i for i in range(1000)]
        patch = "".join("@@ -1,1 +1,1 @@\n-%s\n+%s\n" % (source[0], source[0]) for _ in range(1000))
        out = core.apply(source, patch, core.Counter())
        _line({"hunks": 1000, "scanned": out["scanned"]})
        return 0
    raise SystemExit("未知场景：" + name)
