"""raydiant: a small ray tracer in pure Python, standard library only."""

from .camera import Camera
from .hittable import HitRecord, HittableList, Plane, Sphere
from .image import write_png, write_ppm
from .material import CheckerTexture, Dielectric, Lambertian, Material, Metal
from .ray import Ray
from .render import ray_color, render
from .scenes import SCENES, cover, trio
from .vec3 import Vec3, cross, dot, reflect, refract

__all__ = [
    "Camera", "HitRecord", "HittableList", "Plane", "Sphere",
    "CheckerTexture", "Dielectric", "Lambertian", "Material", "Metal",
    "Ray", "Vec3", "cross", "dot", "reflect", "refract",
    "ray_color", "render", "write_png", "write_ppm",
    "SCENES", "cover", "trio",
]
