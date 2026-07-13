import unittest
from pathlib import Path

from tech.chatflow.poc.ground import (
    WIKI_NODE_DIR,
    extract_markdown_section,
    extract_source_refs,
    normalized_case_anchor,
    resolve_source_ref,
)


class ExtractMarkdownSectionTests(unittest.TestCase):
    def test_composite_anchor_selects_case_within_parent_month(self) -> None:
        markdown = """\
## 2024年11月

### 案例一

2024年的案例。

## 2023年11月

### 案例一

2023年的案例。

### 案例二

不应返回的相邻案例。
"""

        section = extract_markdown_section(markdown, "2023年11月/案例1")

        self.assertIn("2023年的案例。", section)
        self.assertNotIn("2024年的案例。", section)
        self.assertNotIn("不应返回的相邻案例。", section)

    def test_composite_anchor_does_not_match_case_number_prefix(self) -> None:
        markdown = """\
## 2023年6月

### 案例1

第一个案例。

### 案例10

第十个案例。
"""

        section = extract_markdown_section(markdown, "2023年6月/案例10")

        self.assertIn("第十个案例。", section)
        self.assertNotIn("第一个案例。", section)

    def test_composite_anchor_rejects_duplicate_parent_sections(self) -> None:
        markdown = """\
## 2023年6月

### 案例1

第一批。

## 2023年6月

### 案例1

第二批。
"""

        section = extract_markdown_section(markdown, "2023年6月/案例1")

        self.assertEqual(section, "")


class DomesticViolenceCaseReferenceTests(unittest.TestCase):
    def test_node_case_references_resolve_to_the_declared_case(self) -> None:
        refs: list[tuple[Path, str]] = []
        for node_path in sorted(WIKI_NODE_DIR.glob("*.md")):
            node_text = node_path.read_text(encoding="utf-8")
            refs.extend(
                (node_path, ref)
                for ref in extract_source_refs(node_text)
                if "家暴典型案例.md#" in ref
            )

        self.assertTrue(refs)
        for node_path, ref in refs:
            with self.subTest(node=node_path.name, ref=ref):
                anchor = ref.split("#", 1)[1]
                self.assertRegex(anchor, r"^202\d年\d+月(?:\d+日)?/案例\d+$")
                expected_case = normalized_case_anchor(anchor.split("/", 1)[1])
                heading = resolve_source_ref(ref).text.splitlines()[0]
                actual_case = normalized_case_anchor(heading.removeprefix("### "))
                self.assertRegex(actual_case, rf"^{expected_case}(?:$|\D)")


if __name__ == "__main__":
    unittest.main()
