"""Catch citation or skill version drift from the documented release."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_python_package_metadata_declares_installable_compatibility_package(self):
        text = (ROOT / 'pyproject.toml').read_text(encoding="utf-8")
        self.assertIn('name = "yuanjing-storyforge"', text)
        self.assertIn('packages = ["ai_comic_drama"]', text)
        for file in ('README.md', 'README_EN.md'):
            self.assertIn('python3 -m pip install .', (ROOT / file).read_text(encoding="utf-8"))

    def test_ci_covers_supported_desktop_platforms_and_install_smoke(self):
        text = (ROOT / '.github/workflows/ci.yml').read_text(encoding="utf-8")
        self.assertIn('ubuntu-latest', text)
        self.assertIn('macos-latest', text)
        self.assertIn('windows-latest', text)
        self.assertIn('pip install .', text)

    def test_citation_and_skill_identify_the_current_changelog_release(self):
        release = re.search(r'^## (\d+\.\d+\.\d+)\s*$', (ROOT / 'CHANGELOG.md').read_text(encoding="utf-8"), re.M).group(1)
        for file in ('CITATION.cff', 'SKILL.md'):
            with self.subTest(file=file):
                version = re.search(r'^\s*version:\s*(\S+)', (ROOT / file).read_text(encoding="utf-8"), re.M).group(1)
                self.assertEqual(version, release, f'{file} misidentifies the release users cite or load')
