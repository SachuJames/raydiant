import math

import pytest

from raydiant.vec3 import Vec3, cross, dot, reflect, refract


def approx(a, b, tol=1e-9):
    return abs(a - b) < tol


def test_dot():
    assert dot(Vec3(1, 2, 3), Vec3(4, -5, 6)) == 12


def test_cross():
    c = cross(Vec3(1, 0, 0), Vec3(0, 1, 0))
    assert (c.x, c.y, c.z) == (0, 0, 1)


def test_length_and_unit():
    v = Vec3(3, 0, 4)
    assert approx(v.length(), 5.0)
    u = v.unit()
    assert approx(u.length(), 1.0)
    assert approx(u.x, 0.6) and approx(u.z, 0.8)


def test_reflect():
    r = reflect(Vec3(1, -1, 0), Vec3(0, 1, 0))
    assert approx(r.x, 1) and approx(r.y, 1) and approx(r.z, 0)


def test_refract_normal_incidence_goes_straight():
    r = refract(Vec3(0, -1, 0), Vec3(0, 1, 0), 1.5)
    assert approx(r.x, 0) and approx(r.y, -1) and approx(r.z, 0)


def test_schlick_bounds():
    from raydiant.material import _schlick

    assert approx(_schlick(0.0, 1.5), 1.0)  # grazing: total reflection
    r0 = ((1 - 1.5) / (1 + 1.5)) ** 2
    assert approx(_schlick(1.0, 1.5), r0)  # head on: almost all passes through
