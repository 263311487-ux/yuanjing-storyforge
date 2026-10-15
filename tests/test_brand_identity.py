import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BrandIdentityTests(unittest.TestCase):
    def test_skill_uses_the_unique_yuanjing_storyforge_identity(self):
        skill = (ROOT / "SKILL.md").read_text()
        self.assertRegex(skill, re.compile(r"^name:\s*yuanjing-storyforge$", re.M))
        self.assertIn("Yuanjing Storyforge", skill)
        self.assertIn("元境·漫界工坊", skill)

    def test_public_metadata_uses_new_repository_and_invocation(self):
        citation = (ROOT / "CITATION.cff").read_text()
        agent = (ROOT / "agents/openai.yaml").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertIn('title: "Yuanjing Storyforge:', citation)
        self.assertIn("github.com/263311487-ux/yuanjing-storyforge", citation)
        self.assertIn("display_name: \"Yuanjing Storyforge\"", agent)
        self.assertIn("$yuanjing-storyforge", agent)
        self.assertIn("github.com/263311487-ux/yuanjing-storyforge", readme)

    def test_old_name_is_retained_only_as_search_compatibility(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("ai-comic-drama", readme)
        self.assertIn("formerly", readme.lower())


if __name__ == "__main__":
    unittest.main()
