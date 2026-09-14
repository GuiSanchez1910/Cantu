"""Gera versões WebP menores das fotos do site.

Exemplo:
    python scripts/compress_images.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
QUALITY = 80
HERO_FILES = {"variaspolos2.png", "variascamisetas.png", "kit.png"}
LOGO_FILES = {"logo.png", "logo-header.png"}
CROP_OPAQUE_FILES = {"logo.png", "logo-header.png"}
WHITE_MATTE = (255, 255, 255, 255)
NAVY_MATTE = (5, 21, 46, 255)


def max_side_for(path: Path) -> int:
    """Define o lado máximo de cada tipo de imagem."""
    name = path.name.lower()
    if name in LOGO_FILES:
        return 360
    if name in HERO_FILES:
        return 1200
    return 800


def resized_copy(image: Image.Image, max_side: int) -> Image.Image:
    """Reduz a imagem se ela passar do lado máximo."""
    width, height = image.size
    longest = max(width, height)
    if longest <= max_side:
        return image
    ratio = max_side / longest
    size = (max(1, round(width * ratio)), max(1, round(height * ratio)))
    return image.resize(size, Image.Resampling.LANCZOS)


SKIP_WEBP = {
    "iconenavegador.png",
    "favicon-32.png",
    "apple-touch-icon.png",
    "icon-192.png",
}


def matte_for(path: Path) -> tuple[int, int, int, int]:
    """Escolhe o fundo sólido no qual a transparência deve ser achatada."""
    name = path.name.lower()
    if name in LOGO_FILES or name in HERO_FILES:
        return NAVY_MATTE
    return WHITE_MATTE


def crop_to_opaque(image: Image.Image, padding: int = 4) -> Image.Image:
    """Corta a margem transparente para a logo não alongar o header."""
    rgba = image.convert("RGBA")
    box = rgba.getbbox()
    if box is None:
        return image
    left, top, right, bottom = box
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(rgba.width, right + padding)
    bottom = min(rgba.height, bottom + padding)
    return rgba.crop((left, top, right, bottom))


def flatten_on_matte(image: Image.Image, matte: tuple[int, int, int, int]) -> Image.Image:
    """Cobre transparência para o WebP lossy não vazar fundo verde."""
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", rgba.size, matte)
    return Image.alpha_composite(background, rgba).convert("RGB")


def prepared_source(image: Image.Image) -> Image.Image:
    """Converte paleta com transparência para RGBA antes de redimensionar."""
    if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
        return image.convert("RGBA")
    return image.convert("RGB")


def to_rgb_for_webp(image: Image.Image, matte: tuple[int, int, int, int]) -> Image.Image:
    """Garante RGB opaco antes de gravar WebP."""
    return flatten_on_matte(image, matte)


def image_for_webp(image: Image.Image, path: Path) -> Image.Image:
    """Recorta a logo e achata o fundo antes de gravar o WebP."""
    source = crop_to_opaque(image) if path.name.lower() in CROP_OPAQUE_FILES else image
    return to_rgb_for_webp(source, matte_for(path))


def save_webp(image: Image.Image, destination: Path, quality: int = QUALITY) -> None:
    """Grava WebP com transparência quando a origem tem alfa."""
    image.save(destination, "WEBP", quality=quality, method=6)


def export_sized_webp(source: Path, destination: Path, max_side: int, quality: int) -> Path:
    """Gera um WebP com lado máximo e qualidade específicos."""
    with Image.open(source) as image:
        rgb = image_for_webp(image, source)
        save_webp(resized_copy(rgb, max_side), destination, quality)
    return destination


def export_first_paint_images() -> None:
    """Gera as fotos leves usadas só na primeira pintura da página."""
    hero = IMAGES / "vestuario" / "variaspolos2.png"
    export_sized_webp(hero, IMAGES / "vestuario" / "variaspolos2-480.webp", 480, 68)
    export_sized_webp(hero, IMAGES / "vestuario" / "variaspolos2-800.webp", 800, 72)
    header = IMAGES / "logo" / "logo-header.png"
    export_sized_webp(header, IMAGES / "logo" / "logo-header-280.webp", 280, 76)


def export_webp(source: Path) -> Path:
    """Cria o .webp ao lado do PNG original."""
    destination = source.with_suffix(".webp")
    with Image.open(source) as image:
        rgb = image_for_webp(image, source)
        save_webp(resized_copy(rgb, max_side_for(source)), destination)
    return destination


def export_png_icon(source: Path, destination: Path, size: int) -> None:
    """Gera ícone PNG quadrado para favicon e PWA."""
    with Image.open(source) as image:
        icon = image.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
        icon.save(destination, "PNG", optimize=True)


def png_sources() -> list[Path]:
    """Lista PNGs únicos em images/, ignorando duplicata de caixa."""
    found: dict[str, Path] = {}
    for path in IMAGES.rglob("*.png"):
        found[str(path).lower()] = path
    return sorted(found.values())


def main() -> None:
    """Comprime as fotos de conteúdo e gera ícones leves."""
    logo_icon = IMAGES / "logo" / "iconenavegador.png"
    export_png_icon(logo_icon, IMAGES / "logo" / "favicon-32.png", 32)
    export_png_icon(logo_icon, IMAGES / "logo" / "apple-touch-icon.png", 180)
    export_png_icon(logo_icon, IMAGES / "logo" / "icon-192.png", 192)
    export_first_paint_images()

    total_before = 0
    total_after = 0
    for source in png_sources():
        if source.name.lower() in SKIP_WEBP:
            continue
        total_before += source.stat().st_size
        destination = export_webp(source)
        total_after += destination.stat().st_size
        print(f"{source.relative_to(ROOT)} -> {destination.name} ({destination.stat().st_size // 1024} KB)")

    print(f"PNG origem: {total_before // 1024} KB")
    print(f"WebP gerado: {total_after // 1024} KB")


if __name__ == "__main__":
    main()
