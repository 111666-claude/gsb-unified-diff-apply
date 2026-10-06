"""命令行入口。"""

import argparse

from . import core, samples


def main(argv=None):
    ap = argparse.ArgumentParser(prog="patchkit")
    ap.add_argument("--sample", choices=["context", "offset", "len", "work"])
    sub = ap.add_subparsers(dest="cmd")
    apply_parser = sub.add_parser("apply")
    apply_parser.add_argument("--source", required=True)
    apply_parser.add_argument("--patch", required=True)
    args = ap.parse_args(argv)

    if args.sample:
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    with open(args.source, encoding="utf-8") as fh:
        source = fh.read().splitlines()
    with open(args.patch, encoding="utf-8") as fh:
        patch = fh.read()
    print(core.render(core.apply(source, patch, core.Counter())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
