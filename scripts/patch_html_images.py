"""Atualiza o HTML para WebP e adia fotos invisíveis do carrossel."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"


def to_webp_src(html: str) -> str:
    """Troca PNG locais das tags img pelo WebP correspondente."""
    keep_png = {"logo.png", "favicon-32.png", "apple-touch-icon.png", "icon-192.png"}

    def replace_src(match: re.Match[str]) -> str:
        prefix, path = match.group(1), match.group(2)
        filename = path.rsplit("/", 1)[-1] + ".png"
        if filename in keep_png:
            return match.group(0)
        return f'{prefix}src="{path}.webp"'

    return re.sub(
        r'(<(?:img)\b[^>]*?\s)src="(\./images/[^"]+)\.png"',
        replace_src,
        html,
    )


def defer_inactive_gallery_images(html: str) -> str:
    """Só a foto ativa de cada produto baixa na primeira pintura."""

    def patch_block(match: re.Match[str]) -> str:
        block = match.group(0)

        def patch_img(img_match: re.Match[str]) -> str:
            tag = img_match.group(0)
            if "class=\"active\"" in tag:
                return tag
            tag = tag.replace(" src=", " data-src=", 1)
            tag = tag.replace(' loading="lazy"', "")
            return tag

        return re.sub(r"<img\b[^>]*>", patch_img, block)

    return re.sub(
        r'<div class="prod-images">.*?</div>',
        patch_block,
        html,
        flags=re.S,
    )


def defer_product_cover_images(html: str) -> str:
    """Adia a capa de cada produto até o card entrar na tela."""
    html = re.sub(
        r'<img src="(\./images/[^"]+\.webp)" class="active"',
        r'<img data-src="\1" class="active"',
        html,
    )
    return re.sub(
        r'(<img data-src="\./images/[^"]+" class="active"[^>]*) loading="lazy"',
        r'\1',
        html,
    )


def defer_inactive_hero_images(html: str) -> str:
    """Adia as fotos dos slides do hero que ainda não estão visíveis."""
    html = html.replace(
        'src="./images/vestuario/variascamisetas.webp"',
        'data-src="./images/vestuario/variascamisetas.webp"',
        1,
    )
    html = html.replace(
        'src="./images/escritorio/kit.webp"',
        'data-src="./images/escritorio/kit.webp"',
        1,
    )
    return html


def main() -> None:
    """Reescreve index.html com WebP e carregamento sob demanda."""
    html = HTML_PATH.read_text(encoding="utf-8")
    html = to_webp_src(html)
    html = defer_inactive_gallery_images(html)
    html = defer_product_cover_images(html)
    html = defer_inactive_hero_images(html)
    HTML_PATH.write_text(html, encoding="utf-8")
    print("index.html atualizado")


if __name__ == "__main__":
    main()
