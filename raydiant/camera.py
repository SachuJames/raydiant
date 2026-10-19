"""A positionable camera with defocus blur."""

from __future__ import annotations

import math
import random

from .ray import Ray
from .vec3 import Vec3, cross, random_in_unit_disk


class Camera:
    def __init__(
        self,
        lookfrom: Vec3,
        lookat: Vec3,
        vup: Vec3,
        vfov: float,
        aspect: float,
        image_width: int,
        image_height: int,
        aperture: float = 0.0,
        focus_dist: float = 10.0,
    ) -> None:
        self.center = lookfrom

        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * focus_dist
        viewport_width = viewport_height * aspect

        w = (lookfrom - lookat).unit()
        u = cross(vup, w).unit()
        v = cross(w, u)

        viewport_u = viewport_width * u
        viewport_v = viewport_height * -v
        self.pixel_delta_u = viewport_u / image_width
        self.pixel_delta_v = viewport_v / image_height

        upper_left = (
            self.center - focus_dist * w - viewport_u / 2 - viewport_v / 2
        )
        self.pixel00 = upper_left + (self.pixel_delta_u + self.pixel_delta_v) / 2

        self.defocus_radius = (aperture / 2) * focus_dist
        self.defocus_disk_u = u * self.defocus_radius
        self.defocus_disk_v = v * self.defocus_radius

    def _defocus_sample(self, rng: random.Random) -> Vec3:
        p = random_in_unit_disk(rng)
        return self.center + p.x * self.defocus_disk_u + p.y * self.defocus_disk_v

    def get_ray(self, rng: random.Random, sx: float, sy: float) -> Ray:
        pixel_center = self.pixel00 + sx * self.pixel_delta_u + sy * self.pixel_delta_v
        if self.defocus_radius > 0:
            origin = self._defocus_sample(rng)
        else:
            origin = self.center
        return Ray(origin, pixel_center - origin)
