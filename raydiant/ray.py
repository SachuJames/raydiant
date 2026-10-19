"""A ray: an origin and a direction."""

from __future__ import annotations

from .vec3 import Vec3


class Ray:
    __slots__ = ("origin", "direction")

    def __init__(self, origin: Vec3, direction: Vec3) -> None:
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> Vec3:
        return self.origin + t * self.direction
