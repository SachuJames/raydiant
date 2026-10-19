"""Surface materials: how a ray bounces off what it hits."""

from __future__ import annotations

import math
import random

from .ray import Ray
from .vec3 import Vec3, dot, reflect, refract, random_in_unit_sphere, random_unit_vector


class Material:
    def scatter(self, ray_in: Ray, rec, rng: random.Random):
        """Return (attenuation, scattered_ray) or None when absorbed."""
        raise NotImplementedError


class Lambertian(Material):
    """Matte surface. albedo may be a Vec3 or a texture with albedo_at(p)."""

    def __init__(self, albedo) -> None:
        self.albedo = albedo

    def scatter(self, ray_in: Ray, rec, rng: random.Random):
        color = self.albedo
        if hasattr(color, "albedo_at"):
            color = color.albedo_at(rec.p)
        scatter_dir = rec.normal + random_unit_vector(rng)
        if scatter_dir.near_zero():
            scatter_dir = rec.normal
        return color, Ray(rec.p, scatter_dir)


class CheckerTexture:
    """Two-tone checker pattern, handy for the ground."""

    def __init__(self, color1: Vec3, color2: Vec3, scale: float = 1.0) -> None:
        self.color1 = color1
        self.color2 = color2
        self.scale = scale

    def albedo_at(self, p: Vec3) -> Vec3:
        x = math.floor(p.x / self.scale)
        z = math.floor(p.z / self.scale)
        return self.color1 if (x + z) % 2 == 0 else self.color2


class Metal(Material):
    """Reflective surface. fuzz 0 is a mirror, 1 is fully rough."""

    def __init__(self, albedo: Vec3, fuzz: float = 0.0) -> None:
        self.albedo = albedo
        self.fuzz = min(fuzz, 1.0)

    def scatter(self, ray_in: Ray, rec, rng: random.Random):
        reflected = reflect(ray_in.direction.unit(), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere(rng))
        if dot(scattered.direction, rec.normal) > 0:
            return self.albedo, scattered
        return None


def _schlick(cosine: float, ref_idx: float) -> float:
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * (1 - cosine) ** 5


class Dielectric(Material):
    """Glass-like material. ref_idx is the index of refraction."""

    def __init__(self, ref_idx: float) -> None:
        self.ref_idx = ref_idx

    def scatter(self, ray_in: Ray, rec, rng: random.Random):
        attenuation = Vec3(1.0, 1.0, 1.0)
        ri = (1.0 / self.ref_idx) if rec.front_face else self.ref_idx
        unit_dir = ray_in.direction.unit()
        cos_theta = min(dot(-unit_dir, rec.normal), 1.0)
        sin_theta = math.sqrt(max(0.0, 1.0 - cos_theta * cos_theta))
        cannot_refract = ri * sin_theta > 1.0
        if cannot_refract or _schlick(cos_theta, ri) > rng.random():
            direction = reflect(unit_dir, rec.normal)
        else:
            direction = refract(unit_dir, rec.normal, ri)
        return attenuation, Ray(rec.p, direction)
