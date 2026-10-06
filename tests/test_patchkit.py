import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patchkit import core


class PatchTest(unittest.TestCase):
    def test_parse_single_hunk(self):
        hunks = core.parse_hunks("@@ -1,2 +1,2 @@\n a\n b\n")
        self.assertEqual(len(hunks), 1)
        self.assertEqual(hunks[0]["start"], 1)
        self.assertEqual(hunks[0]["len"], 2)

    def test_parse_two_hunks(self):
        hunks = core.parse_hunks("@@ -1,1 +1,1 @@\n a\n@@ -5,1 +5,1 @@\n b\n")
        self.assertEqual(len(hunks), 2)

    def test_pure_addition(self):
        out = core.apply(["b"], "@@ -1,1 +1,2 @@\n+x\n b\n", core.Counter())
        self.assertEqual(out["lines"], ["x", "b"])

    def test_empty_patch(self):
        out = core.apply(["a"], "", core.Counter())
        self.assertEqual(out["lines"], ["a"])

    def test_render_joins_lines(self):
        out = core.apply(["a"], "", core.Counter())
        self.assertEqual(core.render(out), "a")


if __name__ == "__main__":
    unittest.main()
