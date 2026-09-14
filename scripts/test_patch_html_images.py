"""Testes da troca de PNG por WebP e do adiamento de fotos."""

from __future__ import annotations

import unittest

from patch_html_images import (
    defer_inactive_gallery_images,
    defer_inactive_hero_images,
    defer_product_cover_images,
    to_webp_src,
)


class ToWebpSrcTests(unittest.TestCase):
    """Garante que só o src local das imagens vira WebP."""

    def test_converts_local_png_src(self) -> None:
        html = '<img src="./images/vestuario/polo1.png" alt="Polo">'
        self.assertIn('src="./images/vestuario/polo1.webp"', to_webp_src(html))

    def test_keeps_footer_logo_png(self) -> None:
        html = '<img src="./images/logo/logo.png" class="footer-logo" alt="Cantu">'
        self.assertIn('src="./images/logo/logo.png"', to_webp_src(html))

    def test_keeps_remote_png_urls(self) -> None:
        html = '<meta property="og:image" content="https://www.cantubrindes.com.br/images/vestuario/variaspolos2.png">'
        self.assertEqual(to_webp_src(html), html)


class DeferGalleryTests(unittest.TestCase):
    """Garante que fotos extras do produto não têm src."""

    def test_defers_extra_photos_and_keeps_cover_for_next_pass(self) -> None:
        html = """
        <div class="prod-images">
          <img src="./images/vestuario/polo1.webp" class="active" alt="Polo">
          <img src="./images/vestuario/polo2.webp" alt="Polo 2" loading="lazy">
        </div>
        """
        result = defer_inactive_gallery_images(html)
        self.assertIn('src="./images/vestuario/polo1.webp"', result)
        self.assertIn('data-src="./images/vestuario/polo2.webp"', result)


class DeferCoverTests(unittest.TestCase):
    """Garante que a capa também espera o card aparecer."""

    def test_defers_active_cover_until_scroll(self) -> None:
        html = '<img src="./images/vestuario/polo1.webp" class="active" alt="Polo" loading="lazy">'
        result = defer_product_cover_images(html)
        self.assertIn('data-src="./images/vestuario/polo1.webp"', result)
        self.assertNotIn(' src="./images/vestuario/polo1.webp"', result)
        self.assertNotIn('loading="lazy"', result)


class DeferHeroTests(unittest.TestCase):
    """Garante que os slides ocultos do hero usam data-src."""

    def test_defers_secondary_hero_photos(self) -> None:
        html = (
            '<img src="./images/vestuario/variascamisetas.webp" alt="Camisetas">'
            '<img src="./images/escritorio/kit.webp" alt="Kit">'
        )
        result = defer_inactive_hero_images(html)
        self.assertIn("data-src=\"./images/vestuario/variascamisetas.webp\"", result)
        self.assertIn("data-src=\"./images/escritorio/kit.webp\"", result)


if __name__ == "__main__":
    unittest.main()
