"""A 3D vector, used for points, directions and colors."""

from __future__ import annotations

import math
import random


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, t: float) -> Vec3:
        return Vec3(self.x * t, self.y * t, self.z * t)

    __rmul__ = __mul__

    def __truediv__(self, t: float) -> Vec3:
        return Vec3(self.x / t, self.y / t, self.z / t)

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def __repr__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def unit(self) -> Vec3:
        return self / self.length()

    def near_zero(self) -> bool:
        s = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s


def dot(a: Vec3, b: Vec3) -> float:
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a: Vec3, b: Vec3) -> Vec3:
    return Vec3(
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x,
    )


def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2 * dot(v, n) * n


def refract(uv: Vec3, n: Vec3, eta: float) -> Vec3:
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perp = eta * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
    return r_out_perp + r_out_parallel


def random_in_unit_sphere(rng: random.Random) -> Vec3:
    while True:
        p = Vec3(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        if p.length_squared() < 1.0:
            return p


def random_unit_vector(rng: random.Random) -> Vec3:
    return random_in_unit_sphere(rng).unit()


def random_in_unit_disk(rng: random.Random) -> Vec3:
    while True:
        p = Vec3(rng.uniform(-1, 1), rng.uniform(-1, 1), 0.0)
        if p.length_squared() < 1.0:
            return p


def random_double(rng: random.Random, lo: float, hi: float) -> float:
    return lo + (hi - lo) * rng.random()
