"""Command line interface."""

from __future__ import annotations

import argparse

from .camera import Camera
from .render import render_to_file
from .scenes import SCENES
from .vec3 import Vec3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="raydiant", description="A small ray tracer in pure Python")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("render", help="render a scene to an image file")
    r.add_argument("--scene", choices=sorted(SCENES), default="trio")
    r.add_argument("--width", type=int, default=800)
    r.add_argument("--spp", type=int, default=32, help="samples per pixel")
    r.add_argument("--depth", type=int, default=20, help="max ray bounce depth")
    r.add_argument("--seed", type=int, default=7)
    r.add_argument("--jobs", type=int, default=2, help="parallel worker processes")
    r.add_argument("--out", default="renders/trio.png")
    return p


def cmd_render(args) -> None:
    world, cam = SCENES[args.scene]()
    height = int(args.width * 9 / 16)
    camera = Camera(
        lookfrom=cam["lookfrom"],
        lookat=cam["lookat"],
        vup=cam["vup"],
        vfov=cam["vfov"],
        aspect=args.width / height,
        image_width=args.width,
        image_height=height,
        aperture=cam.get("aperture", 0.0),
        focus_dist=cam.get("focus_dist", 10.0),
    )
    print(f"scene={args.scene} {args.width}x{height} spp={args.spp} "
          f"depth={args.depth} seed={args.seed} jobs={args.jobs}")
    render_to_file(world, camera, args.width, height, args.spp, args.depth,
                   args.seed, args.jobs, args.out)


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "render":
        cmd_render(args)


if __name__ == "__main__":
    main()
