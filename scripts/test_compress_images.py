"""Testes das regras de compressão de imagens."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from compress_images import (
    WHITE_MATTE,
    crop_to_opaque,
    export_png_icon,
    export_sized_webp,
    flatten_on_matte,
    matte_for,
    max_side_for,
    prepared_source,
    resized_copy,
    save_webp,
)


class MaxSideForTests(unittest.TestCase):
    """Garante o teto certo por tipo de arquivo."""

    def test_logo_uses_360(self) -> None:
        self.assertEqual(max_side_for(Path("logo-header.png")), 360)

    def test_hero_uses_1200(self) -> None:
        self.assertEqual(max_side_for(Path("variaspolos2.png")), 1200)

    def test_product_uses_800(self) -> None:
        self.assertEqual(max_side_for(Path("polo1.png")), 800)


class ResizedCopyTests(unittest.TestCase):
    """Garante que a redução preserva proporção e não amplia."""

    def test_does_not_upscale_small_images(self) -> None:
        image = Image.new("RGB", (100, 80), color="white")
        self.assertEqual(resized_copy(image, 800).size, (100, 80))

    def test_scales_by_longest_side(self) -> None:
        image = Image.new("RGB", (1600, 800), color="white")
        self.assertEqual(resized_copy(image, 800).size, (800, 400))


class ExportSizedWebpTests(unittest.TestCase):
    """Garante o recorte da foto da primeira pintura."""

    def test_caps_longest_side(self) -> None:
        with TemporaryDirectory() as folder:
            origin = Path(folder) / "origem.png"
            destination = Path(folder) / "saida.webp"
            Image.new("RGB", (1000, 1000), color="white").save(origin)
            export_sized_webp(origin, destination, 480, 70)
            with Image.open(destination) as output:
                self.assertEqual(max(output.size), 480)


class SaveWebpTests(unittest.TestCase):
    """Garante que o arquivo WebP é gravado."""

    def test_writes_webp_file(self) -> None:
        image = Image.new("RGB", (8, 8), color="white")
        with TemporaryDirectory() as folder:
            destination = Path(folder) / "foto.webp"
            save_webp(image, destination)
            self.assertGreater(destination.stat().st_size, 0)


class ExportPngIconTests(unittest.TestCase):
    """Garante o tamanho quadrado do favicon gerado."""

    def test_resizes_to_requested_square(self) -> None:
        source = Image.new("RGBA", (64, 64), color=(0, 0, 0, 255))
        with TemporaryDirectory() as folder:
            origin = Path(folder) / "origem.png"
            destination = Path(folder) / "icon.png"
            source.save(origin)
            export_png_icon(origin, destination, 32)
            with Image.open(destination) as icon:
                self.assertEqual(icon.size, (32, 32))


class CropToOpaqueTests(unittest.TestCase):
    """Garante que a margem transparente da logo é recortada."""

    def test_drops_empty_rows_and_columns(self) -> None:
        image = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
        image.putpixel((8, 8), (255, 255, 255, 255))
        cropped = crop_to_opaque(image, padding=0)
        self.assertEqual(cropped.size, (1, 1))

    def test_header_logo_export_is_wider_than_tall(self) -> None:
        with TemporaryDirectory() as folder:
            origin = Path(folder) / "logo-header.png"
            image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
            for x in range(2, 38):
                for y in range(16, 22):
                    image.putpixel((x, y), (255, 255, 255, 255))
            image.save(origin)
            destination = Path(folder) / "saida.webp"
            export_sized_webp(origin, destination, 280, 70)
            with Image.open(destination) as output:
                self.assertGreater(output.size[0], output.size[1])


class FlattenOnMatteTests(unittest.TestCase):
    """Garante que transparência verde vira o fundo sólido certo."""

    def test_transparent_green_becomes_white(self) -> None:
        image = Image.new("RGBA", (2, 2), (0, 255, 0, 0))
        flattened = flatten_on_matte(image, WHITE_MATTE)
        self.assertEqual(flattened.getpixel((0, 0)), (255, 255, 255))

    def test_product_uses_white_matte(self) -> None:
        self.assertEqual(matte_for(Path("polo1.png")), WHITE_MATTE)


class PreparedSourceTests(unittest.TestCase):
    """Garante conversão de paleta com transparência."""

    def test_palette_with_transparency_becomes_rgba(self) -> None:
        image = Image.new("P", (2, 2))
        image.info["transparency"] = 0
        self.assertEqual(prepared_source(image).mode, "RGBA")


if __name__ == "__main__":
    unittest.main()
