import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NODES = ROOT / "knowledge" / "wiki" / "nodes"


class AcademicNodeSchemaTest(unittest.TestCase):
    def test_psychological_violence_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "psychological-violence-concept.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F1", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[domestic-violence-definition]]", text)

        for heading in (
            "## 原子结论",
            "## 核心定义与学界共识",
            "## 主要争议与分歧",
            "## 具体行为/情形列举",
            "## 立法背景与域外借鉴",
            "## 司法现实与认定困境",
            "## 学界倡议的改进方向",
            "## 适用边界",
            "## 机制关系",
            "## 来源依据",
        ):
            self.assertIn(heading, text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 3)

    def test_economic_control_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "economic-control-concept.md").read_text(encoding="utf-8")

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F1", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[domestic-violence-definition]]", text)
        self.assertIn("独断行为", text)
        self.assertIn("剥夺行为", text)
        self.assertIn("阻碍行为", text)
        self.assertIn("羞辱行为", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 3)

    def test_scope_extension_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "dv-scope-extension.md").read_text(encoding="utf-8")

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F1", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[domestic-violence-definition]]", text)
        self.assertIn("共同生活", text)
        self.assertIn("前配偶", text)
        self.assertIn("妇女权益保障法", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 3)

    def test_legislative_history_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "dv-law-legislative-history.md").read_text(encoding="utf-8")

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F2", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn(
            "`traces_legislative_origin_of` → [[domestic-violence-definition]]",
            text,
        )
        self.assertIn("立法参与者同期陈述", text)
        self.assertIn("证据不足", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 3)

    def test_coercive_control_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "coercive-control-comparative.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F2", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[domestic-violence-definition]]", text)
        self.assertIn("行为模式", text)
        self.assertIn("不能证明", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 3)

    def test_international_standards_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "international-human-rights-standards.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F2", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[domestic-violence-definition]]", text)
        self.assertIn("一般性建议", text)
        self.assertIn("结论性意见", text)
        self.assertIn("论文库证据不足", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 4)

    def test_judicial_gap_node_has_required_schema_and_anchors(self) -> None:
        text = (NODES / "judicial-recognition-gap.md").read_text(encoding="utf-8")

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F3", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn(
            "`contextualizes_reality_of` → [[protection-order-evidence]]", text
        )
        self.assertIn("`contextualizes_reality_of` → [[divorce-and-dv]]", text)
        self.assertIn(
            "`contextualizes_reality_of` → [[personal-safety-protection-order]]",
            text,
        )
        self.assertIn("不可外推", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 4)

    def test_victim_barriers_node_has_required_schema_and_anchors(self) -> None:
        text = (NODES / "victim-agency-barriers.md").read_text(encoding="utf-8")

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F3", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[domestic-violence-definition]]", text)
        self.assertIn(
            "`contextualizes_reality_of` → [[protection-order-evidence]]", text
        )
        self.assertIn(
            "`contextualizes_reality_of` → [[judicial-recognition-gap]]", text
        )
        self.assertIn("受害者能动性", text)
        self.assertIn("不是个体诊断", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 4)

    def test_state_intervention_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "state-intervention-limits.md").read_text(encoding="utf-8")

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F4", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[public-security-response-duty]]", text)
        self.assertIn("公私领域", text)
        self.assertIn("不得用于建议调解", text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 4)

    def test_constitutional_obligation_node_has_required_schema_and_anchors(
        self,
    ) -> None:
        text = (NODES / "constitutional-protection-obligation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F4", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[public-security-response-duty]]", text)
        self.assertIn("`deepens` → [[liability-ladder]]", text)
        self.assertIn("基本权三角关系", text)
        self.assertIn("不能直接替代部门法诉请", text)

        for heading in (
            "## 原子结论",
            "## 核心定义与学界共识",
            "## 主要争议与分歧",
            "## 具体行为/情形列举",
            "## 立法背景与域外借鉴",
            "## 司法现实与认定困境",
            "## 学界倡议的改进方向",
            "## 适用边界",
            "## 机制关系",
            "## 来源依据",
        ):
            self.assertIn(heading, text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 3)

    def test_gender_power_node_has_required_schema_and_anchor(self) -> None:
        text = (NODES / "gender-power-analysis.md").read_text(encoding="utf-8")

        self.assertIn("node_kind: concept-depth", text)
        self.assertIn("epistemic_function: F5", text)
        self.assertIn("academic_binding: none", text)
        self.assertRegex(text, r"temporal_note:\s*\S")
        self.assertIn("无法律强制力", text)
        self.assertIn("`deepens` → [[domestic-violence-definition]]", text)
        self.assertIn("AI 隐性认知底色", text)
        self.assertIn("不进入胶囊 ground", text)
        self.assertIn("生态谬误", text)
        self.assertIn("不能推出所有男性都是施暴者", text)
        self.assertIn("避免受害者归责", text)

        for heading in (
            "## 原子结论",
            "## 核心定义与学界共识",
            "## 主要争议与分歧",
            "## 具体行为/情形列举",
            "## 立法背景与域外借鉴",
            "## 司法现实与认定困境",
            "## 学界倡议的改进方向",
            "## 适用边界",
            "## 机制关系",
            "## 来源依据",
        ):
            self.assertIn(heading, text)

        source_refs = re.findall(
            r'"knowledge/source/論文_pdf/[^"\n]+\.pdf#[^"\n]+"', text
        )
        self.assertGreaterEqual(len(source_refs), 4)


if __name__ == "__main__":
    unittest.main()
