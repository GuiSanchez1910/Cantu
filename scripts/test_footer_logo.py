"""Garante que a logo do rodapé usa a mesma marca do header."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def homepage_html() -> str:
    """Lê o HTML da homepage.

    Exemplo: `assert "footer-logo" in homepage_html()`
    """
    return (ROOT / "index.html").read_text(encoding="utf-8")


class FooterLogoTests(unittest.TestCase):
    """A logo do rodapé deve ser o mesmo arquivo do header."""

    def test_footer_uses_header_lockup(self) -> None:
        html = homepage_html()
        self.assertIn('class="logo-image" src="./images/logo/logo-header-280.webp"', html)
        self.assertIn('src="./images/logo/logo-header-280.webp"', html)
        self.assertIn('class="footer-logo"', html)
        self.assertIn('srcset="./images/logo/logo.webp"', html)
        self.assertIn('class="footer-brand"', html)
        self.assertNotIn('data-src="./images/logo/logo.png"', html)


if __name__ == "__main__":
    unittest.main()
