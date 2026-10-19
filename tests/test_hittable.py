from raydiant.hittable import Plane, Sphere
from raydiant.material import Lambertian
from raydiant.ray import Ray
from raydiant.vec3 import Vec3

MAT = Lambertian(Vec3(0.5, 0.5, 0.5))


def test_sphere_front_face_hit():
    s = Sphere(Vec3(0, 0, 0), 1.0, MAT)
    rec = s.hit(Ray(Vec3(0, 0, -5), Vec3(0, 0, 1)), 0.001, float("inf"))
    assert rec is not None
    assert abs(rec.t - 4.0) < 1e-9
    assert rec.front_face is True
    assert rec.normal.z == -1.0


def test_sphere_miss():
    s = Sphere(Vec3(0, 0, 0), 1.0, MAT)
    rec = s.hit(Ray(Vec3(0, 3, -5), Vec3(0, 0, 1)), 0.001, float("inf"))
    assert rec is None


def test_sphere_hit_from_inside_is_back_face():
    s = Sphere(Vec3(0, 0, 0), 1.0, MAT)
    rec = s.hit(Ray(Vec3(0, 0, 0), Vec3(0, 0, 1)), 0.001, float("inf"))
    assert rec is not None
    assert abs(rec.t - 1.0) < 1e-9
    assert rec.front_face is False
    # normal points against the ray even on the back face
    assert rec.normal.z == -1.0


def test_plane_hit():
    p = Plane(Vec3(0, 0, 0), Vec3(0, 1, 0), MAT)
    rec = p.hit(Ray(Vec3(0, 2, 0), Vec3(0, -1, 0)), 0.001, float("inf"))
    assert rec is not None
    assert abs(rec.t - 2.0) < 1e-9
    assert rec.front_face is True


def test_plane_parallel_miss():
    p = Plane(Vec3(0, 0, 0), Vec3(0, 1, 0), MAT)
    rec = p.hit(Ray(Vec3(0, 2, 0), Vec3(1, 0, 0)), 0.001, float("inf"))
    assert rec is None
