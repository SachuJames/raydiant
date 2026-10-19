"""The two built-in scenes. Each returns (world, camera_kwargs)."""

from __future__ import annotations

import random

from .hittable import HittableList, Plane, Sphere
from .material import CheckerTexture, Dielectric, Lambertian, Metal
from .vec3 import Vec3, random_double


def trio():
    """The hero: three big spheres on a checker floor, some small ones."""
    world = HittableList()
    ground = Lambertian(CheckerTexture(Vec3(0.85, 0.85, 0.85), Vec3(0.12, 0.12, 0.14), 1.0))
    world.add(Plane(Vec3(0, 0, 0), Vec3(0, 1, 0), ground))

    world.add(Sphere(Vec3(-2.6, 1.0, 0.0), 1.0, Dielectric(1.5)))
    world.add(Sphere(Vec3(0.0, 1.0, 0.0), 1.0, Lambertian(Vec3(0.72, 0.28, 0.14))))
    world.add(Sphere(Vec3(2.6, 1.0, 0.0), 1.0, Metal(Vec3(0.82, 0.86, 0.90), 0.05)))

    world.add(Sphere(Vec3(-4.6, 0.40, 2.6), 0.40, Lambertian(Vec3(0.15, 0.35, 0.75))))
    world.add(Sphere(Vec3(4.4, 0.50, -1.6), 0.50, Metal(Vec3(0.85, 0.65, 0.25), 0.25)))
    world.add(Sphere(Vec3(1.9, 0.30, 3.2), 0.30, Dielectric(1.5)))
    world.add(Sphere(Vec3(-1.4, 0.35, 4.1), 0.35, Lambertian(Vec3(0.20, 0.60, 0.30))))
    world.add(Sphere(Vec3(-4.9, 0.25, -2.8), 0.25, Metal(Vec3(0.9, 0.9, 0.9), 0.0)))

    camera = dict(
        lookfrom=Vec3(0.0, 2.6, 9.6),
        lookat=Vec3(0.0, 1.0, 0.0),
        vup=Vec3(0, 1, 0),
        vfov=42.0,
        aperture=0.55,
        focus_dist=9.8,
    )
    return world, camera


def cover(seed: int = 42):
    """A field of small random spheres with three big ones, fixed seed."""
    rng = random.Random(seed)
    world = HittableList()
    ground = Lambertian(CheckerTexture(Vec3(0.9, 0.9, 0.9), Vec3(0.2, 0.2, 0.22), 2.0))
    world.add(Plane(Vec3(0, 0, 0), Vec3(0, 1, 0), ground))

    world.add(Sphere(Vec3(0, 1, 0), 1.0, Dielectric(1.5)))
    world.add(Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.1))))
    world.add(Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5), 0.0)))

    for a in range(-11, 11, 2):
        for b in range(-11, 11, 2):
            cx = a + 0.9 * rng.random()
            cz = b + 0.9 * rng.random()
            if (cx - 4) * (cx - 4) + cz * cz < 0.81:
                continue
            center = Vec3(cx, 0.2, cz)
            pick = rng.random()
            if pick < 0.75:
                color = Vec3(rng.random() ** 2, rng.random() ** 2, rng.random() ** 2)
                material = Lambertian(color)
            elif pick < 0.93:
                color = Vec3(
                    random_double(rng, 0.5, 1.0),
                    random_double(rng, 0.5, 1.0),
                    random_double(rng, 0.5, 1.0),
                )
                material = Metal(color, random_double(rng, 0.0, 0.5))
            else:
                material = Dielectric(1.5)
            world.add(Sphere(center, 0.2, material))

    camera = dict(
        lookfrom=Vec3(13.0, 2.0, 3.0),
        lookat=Vec3(0.0, 0.0, 0.0),
        vup=Vec3(0, 1, 0),
        vfov=20.0,
        aperture=0.1,
        focus_dist=10.0,
    )
    return world, camera


SCENES = {"trio": trio, "cover": cover}
