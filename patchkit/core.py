"""解析并应用统一 diff。"""


class Counter:
    """记录本轮检查过的目标文件行数。"""

    def __init__(self):
        self.scanned = 0


def parse_hunks(patch):
    hunks = []
    for line in patch.splitlines():
        if line.startswith("@@"):
            head = line.split("@@")[1].strip().split(" ")[0]
            body = head[1:]
            parts = body.split(",")
            start = int(parts[0])
            length = int(parts[1]) if len(parts) > 1 else 1
            hunks.append({"start": start, "len": length, "lines": []})
        elif hunks:
            hunks[-1]["lines"].append(line)
    return hunks


def apply(source, patch, counter):
    lines = list(source)
    for hunk in parse_hunks(patch):
        pos = hunk["start"] - 1
        for line in hunk["lines"]:
            for _ in lines:
                counter.scanned += 1
            tag, text = line[0], line[1:]
            if tag == " ":
                lines[pos] = text
                pos += 1
            elif tag == "-":
                del lines[pos]
            elif tag == "+":
                lines.insert(pos, text)
                pos += 1
    return {"status": "ok", "lines": lines, "scanned": counter.scanned}


def render(result):
    if result["status"] != "ok":
        return "conflict: " + (result.get("reason") or "")
    return "\n".join(result["lines"])
