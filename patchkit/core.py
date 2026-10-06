"""解析并应用统一 diff。"""


class Counter:
    """记录本轮检查过的目标文件行数。"""

    def __init__(self):
        self.scanned = 0


def parse_hunks(patch):
    hunks = []
    for line in patch.splitlines():
        if line.startswith("@@"):
            head = line.split("@@")[1].strip().split(" ")
            old_start, old_len = _parse_range(head[0])
            new_start, new_len = _parse_range(head[1])
            hunks.append({
                "start": old_start,
                "len": old_len,
                "new_start": new_start,
                "new_len": new_len,
                "lines": [],
            })
        elif hunks:
            hunks[-1]["lines"].append(line)
    return hunks


def _parse_range(token):
    body = token[1:]
    parts = body.split(",")
    start = int(parts[0])
    length = int(parts[1]) if len(parts) > 1 else 1
    return start, length


def _conflict(reason, counter):
    return {"status": "conflict", "reason": reason, "scanned": counter.scanned}


def apply(source, patch, counter):
    lines = list(source)
    offset = 0
    for hunk in parse_hunks(patch):
        pos = hunk["start"] - 1 + offset
        if pos < 0 or pos + hunk["len"] > len(lines):
            return _conflict("hunk 声明的旧长度与原文不符", counter)
        for line in hunk["lines"]:
            tag, text = (line[0], line[1:]) if line else (" ", "")
            if tag == " ":
                counter.scanned += 1
                if pos >= len(lines) or lines[pos] != text:
                    return _conflict("上下文与原文不符", counter)
                pos += 1
            elif tag == "-":
                counter.scanned += 1
                if pos >= len(lines):
                    return _conflict("删除行超出原文范围", counter)
                del lines[pos]
            elif tag == "+":
                lines.insert(pos, text)
                pos += 1
        offset += hunk["new_len"] - hunk["len"]
    return {"status": "ok", "lines": lines, "scanned": counter.scanned}


def render(result):
    if result["status"] != "ok":
        return "conflict: " + (result.get("reason") or "")
    return "\n".join(result["lines"])
