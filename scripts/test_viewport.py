"""Testes da regra de proximidade da viewport."""

from __future__ import annotations

import unittest

from viewport import is_near_viewport


class IsNearViewportTests(unittest.TestCase):
    """Garante quando a capa do produto pode ser baixada."""

    def test_card_inside_screen_is_near(self) -> None:
        self.assertTrue(is_near_viewport(20, 300, 40, 400, 1200, 800))

    def test_card_far_below_is_not_near(self) -> None:
        self.assertFalse(is_near_viewport(0, 300, 2000, 2400, 1200, 800))

    def test_card_just_below_margin_is_near(self) -> None:
        self.assertTrue(is_near_viewport(0, 300, 900, 1100, 1200, 800, extra=160))
