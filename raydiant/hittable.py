"""Things a ray can hit: spheres, planes, and lists of them."""

from __future__ import annotations

import math

from .ray import Ray
from .vec3 import Vec3, dot


class HitRecord:
    __slots__ = ("p", "normal", "t", "front_face", "material")

    def __init__(self) -> None:
        self.p: Vec3 = Vec3()
        self.normal: Vec3 = Vec3()
        self.t: float = 0.0
        self.front_face: bool = True
        self.material = None

    def set_face_normal(self, ray: Ray, outward_normal: Vec3) -> None:
        self.front_face = dot(ray.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Sphere:
    __slots__ = ("center", "radius", "material")

    def __init__(self, center: Vec3, radius: float, material) -> None:
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray: Ray, t_min: float, t_max: float):
        oc = ray.origin - self.center
        d = ray.direction
        a = d.length_squared()
        half_b = dot(oc, d)
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return None
        sqrtd = math.sqrt(discriminant)
        root = (-half_b - sqrtd) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrtd) / a
            if root < t_min or root > t_max:
                return None
        rec = HitRecord()
        rec.t = root
        rec.p = ray.at(root)
        outward = (rec.p - self.center) / self.radius
        rec.set_face_normal(ray, outward)
        rec.material = self.material
        return rec


class Plane:
    """An infinite plane through a point with a given normal."""

    __slots__ = ("point", "normal", "material")

    def __init__(self, point: Vec3, normal: Vec3, material) -> None:
        self.point = point
        self.normal = normal.unit()
        self.material = material

    def hit(self, ray: Ray, t_min: float, t_max: float):
        denom = dot(ray.direction, self.normal)
        if abs(denom) < 1e-8:
            return None
        t = dot(self.point - ray.origin, self.normal) / denom
        if t < t_min or t > t_max:
            return None
        rec = HitRecord()
        rec.t = t
        rec.p = ray.at(t)
        rec.set_face_normal(ray, self.normal)
        rec.material = self.material
        return rec


class HittableList:
    def __init__(self) -> None:
        self.objects: list = []

    def add(self, obj) -> None:
        self.objects.append(obj)

    def hit(self, ray: Ray, t_min: float, t_max: float):
        closest = t_max
        hit_any = None
        for obj in self.objects:
            rec = obj.hit(ray, t_min, closest)
            if rec is not None:
                closest = rec.t
                hit_any = rec
        return hit_any
