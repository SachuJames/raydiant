from raydiant.camera import Camera
from raydiant.hittable import HittableList, Plane, Sphere
from raydiant.material import Dielectric, Lambertian, Metal
from raydiant.render import render
from raydiant.vec3 import Vec3


def _tiny_scene():
    world = HittableList()
    world.add(Plane(Vec3(0, 0, 0), Vec3(0, 1, 0), Lambertian(Vec3(0.5, 0.5, 0.5))))
    world.add(Sphere(Vec3(0, 1, 0), 1.0, Dielectric(1.5)))
    world.add(Sphere(Vec3(-2.2, 0.5, -1), 0.5, Metal(Vec3(0.8, 0.8, 0.8), 0.0)))
    camera = Camera(
        lookfrom=Vec3(0, 2.5, 7),
        lookat=Vec3(0, 1, 0),
        vup=Vec3(0, 1, 0),
        vfov=40.0,
        aspect=16 / 9,
        image_width=24,
        image_height=13,
        aperture=0.0,
        focus_dist=7.0,
    )
    return world, camera


def _run(jobs):
    world, camera = _tiny_scene()
    return render(world, camera, 24, 13, spp=2, max_depth=4, seed=11, jobs=jobs)


def test_render_buffer_shape():
    rows = _run(jobs=1)
    assert len(rows) == 13
    assert all(len(row) == 24 for row in rows)
    for row in rows:
        for (r, g, b) in row:
            assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255


def test_render_deterministic_same_seed():
    assert _run(jobs=1) == _run(jobs=1)


def test_render_same_across_job_counts():
    assert _run(jobs=1) == _run(jobs=2)


def test_sky_pixel_is_bluish():
    rows = _run(jobs=1)
    r, g, b = rows[0][12]  # top center looks at the sky
    assert b > r
