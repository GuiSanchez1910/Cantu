"""Regra compartilhada com main.js para baixar foto só perto da tela."""


def is_near_viewport(
    left: float,
    right: float,
    top: float,
    bottom: float,
    view_width: float,
    view_height: float,
    extra: float = 160,
) -> bool:
    """Retorna True quando o card está visível ou a poucos pixels da viewport."""
    return right > 0 and left < view_width and bottom > -extra and top < view_height + extra
