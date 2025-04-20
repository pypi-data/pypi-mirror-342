from __future__ import annotations

import functools
import itertools
from typing import NamedTuple

from babi.color import Color


def _square_distance(c1: Color, c2: Color) -> int:
    return (c1.r - c2.r) ** 2 + (c1.g - c2.g) ** 2 + (c1.b - c2.b) ** 2


class KD(NamedTuple):
    color: Color
    n: int
    left: KD | None
    right: KD | None


def _build(colors: list[tuple[Color, int]], depth: int = 0) -> KD | None:
    if not colors:
        return None

    axis = depth % 3
    colors.sort(key=lambda kv: kv[0][axis])
    pivot = len(colors) // 2

    return KD(
        *colors[pivot],
        _build(colors[:pivot], depth=depth + 1),
        _build(colors[pivot + 1:], depth=depth + 1),
    )


def nearest(color: Color, colors: KD | None) -> int:
    best = 0
    dist = 2 ** 32

    def _search(kd: KD | None, *, depth: int) -> None:
        nonlocal best
        nonlocal dist

        if kd is None:
            return

        cand_dist = _square_distance(color, kd.color)
        if cand_dist < dist:
            best, dist = kd.n, cand_dist

        axis = depth % 3
        diff = color[axis] - kd.color[axis]
        if diff > 0:
            _search(kd.right, depth=depth + 1)
            if diff ** 2 < dist:
                _search(kd.left, depth=depth + 1)
        else:
            _search(kd.left, depth=depth + 1)
            if diff ** 2 < dist:
                _search(kd.right, depth=depth + 1)

    _search(colors, depth=0)
    return best


@functools.lru_cache(maxsize=1)
def make_256() -> KD | None:
    vals = (0, 95, 135, 175, 215, 255)
    colors = [
        (Color(r, g, b), i)
        for i, (r, g, b) in enumerate(itertools.product(vals, vals, vals), 16)
    ]
    for i in range(24):
        v = 10 * i + 8
        colors.append((Color(v, v, v), 232 + i))

    return _build(colors)
