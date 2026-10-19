"""The path tracing loop. Rows are independent, so they can go parallel."""

from __future__ import annotations

import math
import random
import sys
import time
from multiprocessing import Pool

from .image import write_png, write_ppm
from .ray import Ray
from .vec3 import Vec3

_SKY_TOP = Vec3(0.5, 0.7, 1.0)
_SKY_BOTTOM = Vec3(1.0, 1.0, 1.0)


def _sky_color(direction: Vec3) -> Vec3:
    t = 0.5 * (direction.unit().y + 1.0)
    return (1.0 - t) * _SKY_BOTTOM + t * _SKY_TOP


def ray_color(ray: Ray, world, depth: int, rng: random.Random) -> Vec3:
    if depth <= 0:
        return Vec3(0, 0, 0)
    rec = world.hit(ray, 0.001, float("inf"))
    if rec is not None:
        result = rec.material.scatter(ray, rec, rng)
        if result is None:
            return Vec3(0, 0, 0)
        attenuation, scattered = result
        r = ray_color(scattered, world, depth - 1, rng)
        return Vec3(
            attenuation.x * r.x, attenuation.y * r.y, attenuation.z * r.z
        )
    return _sky_color(ray.direction)


def _render_row(args) -> tuple:
    y, width, height, spp, max_depth, seed, world, camera = args
    rng = random.Random(seed * 100003 + y)
    get_ray = camera.get_ray
    row = []
    for x in range(width):
        pixel = Vec3(0, 0, 0)
        for _ in range(spp):
            sx = x + rng.random()
            sy = y + rng.random()
            ray = get_ray(rng, sx, sy)
            c = ray_color(ray, world, max_depth, rng)
            pixel = pixel + c
        scale = 1.0 / spp
        r = min(255, max(0, int(256 * math.sqrt(pixel.x * scale))))
        g = min(255, max(0, int(256 * math.sqrt(pixel.y * scale))))
        b = min(255, max(0, int(256 * math.sqrt(pixel.z * scale))))
        row.append((r, g, b))
    return y, row


def render(world, camera, width: int, height: int, spp: int, max_depth: int,
           seed: int, jobs: int = 1):
    """Render the scene. Returns rows of (r, g, b) ints, top row first."""
    start = time.time()
    tasks = [
        (y, width, height, spp, max_depth, seed, world, camera)
        for y in range(height)
    ]
    rows = [None] * height
    done = 0
    if jobs <= 1:
        for task in tasks:
            y, row = _render_row(task)
            rows[y] = row
            done += 1
            if done % max(1, height // 10) == 0 or done == height:
                print(f"  {done}/{height} rows", file=sys.stderr)
    else:
        with Pool(jobs) as pool:
            for y, row in pool.imap_unordered(_render_row, tasks, chunksize=4):
                rows[y] = row
                done += 1
                if done % max(1, height // 10) == 0 or done == height:
                    print(f"  {done}/{height} rows", file=sys.stderr)
    elapsed = time.time() - start
    print(f"rendered {width}x{height}, {spp} spp, depth {max_depth} in {elapsed:.1f}s",
          file=sys.stderr)
    return rows


def render_to_file(world, camera, width: int, height: int, spp: int,
                   max_depth: int, seed: int, jobs: int, out: str) -> None:
    rows = render(world, camera, width, height, spp, max_depth, seed, jobs)
    if out.lower().endswith(".png"):
        write_png(out, width, height, rows)
    else:
        write_ppm(out, width, height, rows)
    print(f"wrote {out}")
