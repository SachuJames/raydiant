import random

from raydiant.hittable import HitRecord
from raydiant.material import Dielectric, Lambertian, Metal
from raydiant.ray import Ray
from raydiant.vec3 import Vec3, dot, reflect


def _rec(normal):
    rec = HitRecord()
    rec.p = Vec3(0, 0, 0)
    rec.normal = normal
    rec.front_face = True
    return rec


def test_lambertian_scatter_stays_in_hemisphere():
    mat = Lambertian(Vec3(0.7, 0.3, 0.1))
    rec = _rec(Vec3(0, 1, 0))
    for seed in range(20):
        rng = random.Random(seed)
        attenuation, scattered = mat.scatter(Ray(Vec3(0, 2, 0), Vec3(0, -1, 0)), rec, rng)
        assert dot(scattered.direction, rec.normal) > 0
        assert (attenuation.x, attenuation.y, attenuation.z) == (0.7, 0.3, 0.1)


def test_metal_mirror_with_zero_fuzz():
    mat = Metal(Vec3(0.8, 0.8, 0.8), fuzz=0.0)
    rec = _rec(Vec3(0, 1, 0))
    rng = random.Random(1)
    attenuation, scattered = mat.scatter(Ray(Vec3(0, 2, 0), Vec3(1, -1, 0)), rec, rng)
    expected = reflect(Vec3(1, -1, 0).unit(), rec.normal)
    assert abs(scattered.direction.x - expected.x) < 1e-9
    assert abs(scattered.direction.y - expected.y) < 1e-9


class _FixedRandom:
    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value


def test_dielectric_forced_reflection():
    mat = Dielectric(1.5)
    rec = _rec(Vec3(0, 1, 0))
    ray = Ray(Vec3(0, 2, 0), Vec3(0, -1, 0))
    _, scattered = mat.scatter(ray, rec, _FixedRandom(0.0))
    expected = reflect(ray.direction.unit(), rec.normal)
    assert abs(scattered.direction.x - expected.x) < 1e-9
    assert abs(scattered.direction.y - expected.y) < 1e-9


def test_dielectric_forced_refraction_at_normal_incidence():
    mat = Dielectric(1.5)
    rec = _rec(Vec3(0, 1, 0))
    ray = Ray(Vec3(0, 2, 0), Vec3(0, -1, 0))
    _, scattered = mat.scatter(ray, rec, _FixedRandom(1.0))
    # head on into glass: passes straight through
    assert abs(scattered.direction.x) < 1e-9
    assert abs(scattered.direction.z) < 1e-9
    assert scattered.direction.y < 0
