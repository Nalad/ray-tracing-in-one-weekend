import math
import random
import multiprocessing
import functools
import numpy as np

from sphere import Sphere
from hitable_list import HitableList
from hit_record import HitRecord
from vec3 import Vec3
from ray import Ray
from camera import Camera
from lambertian import Lambertian
from metal import Metal
from dielectric import Dielectric


def color(r, world, depth):
    rec = HitRecord(t=0, p=Vec3(0, 0, 0), normal=Vec3(0, 0, 0), material=None)

    if world.hit(r, 0.001, 10000, rec):
        scattered = Ray(Vec3(0, 0, 0), Vec3(0, 0, 0))
        t = rec.material.scatter(r, rec, scattered)
        if (depth < 50 and t[0]):
            return color(scattered, world, depth + 1).mul(t[1])
        else:
            return Vec3(0, 0, 0)
    else:
        unit_direction = r.B.unit_vector()

        t = 0.5 * (unit_direction.e[1] + 1.0)

        return Vec3(1.0, 1.0, 1.0) * (1 - t) + Vec3(0.5, 0.7, 1.0) * t


def random_scene():
    scene = []
    scene.append(Sphere(Vec3(0, -1000, 0), 1000,
                        Lambertian(Vec3(0.5, 0.5, 0.5))))
    i = 1
    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Vec3(a + 0.9 * random.random(),
                          0.2, b + 0.9 * random.random())
            if ((center - Vec3(4, 0.2, 0)).length > 0.9):
                if (choose_mat < 0.8):
                    scene.append(Sphere(center, 0.2, Lambertian(Vec3(random.random(
                    ) * random.random(), random.random() * random.random(), random.random() * random.random()))))
                elif (choose_mat < 0.95):
                    scene.append(Sphere(center, 0.2, Metal(Vec3(
                        0.5 * (1 + random.random()), 0.5 * (1 + random.random()), 0.5 * (1 + random.random())), 0.5 * random.random())))
                else:
                    scene.append(Sphere(center, 0.2, Dielectric(1.5)))

    scene.append(Sphere(Vec3(0, 1, 0), 1.0, Dielectric(1.5)))
    scene.append(Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.1))))
    scene.append(Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5), 0.0)))

    return scene


def pass_n_times(camera, world, nx, ny, ns, output):
    current = multiprocessing.current_process()
    image = [[0 for x in range(nx)] for y in range(ny)]
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            col = Vec3(0, 0, 0)
            for s in range(ns):
                u = (i + random.random()) / nx
                v = (j + random.random()) / ny
                r = camera.get_ray(u, v)
                p = r.point_at_parameter(2.0)
                col += color(r, world, 0)

            col /= ns
            col = Vec3(math.sqrt(col[0]),
                       math.sqrt(col[1]),
                       math.sqrt(col[2]))

            image[j][i] = col

        print("{}:\t{:.2f}%".format(current.name, (1 - j / ny) * 100))

    output.put(image)


if __name__ == '__main__':
    nx = 400
    ny = 200
    ns = 100

    num_of_processes = 2

    assert(ns % 2 != 0)

    with open('output.ppm', 'w') as out:
        out.write(f"P3\n{nx} {ny}\n255\n")

        sphere_list = []

        sphere_list.append(Sphere(Vec3(1.0, 0.0, -1.0), 0.5,
                                  Lambertian(Vec3(0.1, 0.2, 0.5))))
        sphere_list.append(Sphere(Vec3(0.0, 0.0, -1.0), 0.5,
                                  Metal(Vec3(0.8, 0.8, 0.8), 1.0)))
        sphere_list.append(Sphere(Vec3(0.0, -100.5, -1), 100,
                                  Lambertian(Vec3(0.8, 0.8, 0.0))))

        sphere_list.append(Sphere(Vec3(-1.0, 0.0, -1.0), 0.5,
                                  Dielectric(1.5)))
        sphere_list.append(Sphere(Vec3(-1.0, 0.0, -1.0), -0.45,
                                  Dielectric(1.5)))

        world = HitableList(sphere_list)
        lookfrom = Vec3(3, 3, 2)
        lookat = Vec3(0, 0, -1)
        dist_to_focus = (lookfrom - lookat).length
        aperture = 1.0

        camera = Camera(lookfrom, lookat, Vec3(0, 1, 0), 30,
                        nx / ny, aperture, dist_to_focus)

        output = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=pass_n_times, args=(
            camera, world, nx, ny, int(ns / num_of_processes), output)) for x in range(num_of_processes)]
        for p in processes:
            p.start()

        results = []
        for p in processes:
            results.append(np.array(output.get()))
        for p in processes:
            p.join()

        result = functools.reduce(np.add, results) / num_of_processes

        for j in range(ny - 1, -1, -1):
            for i in range(nx):
                col = result[j][i]
                ir = int(255.99 * col[0])
                ig = int(255.99 * col[1])
                ib = int(255.99 * col[2])
                out.write(f"{ir} {ig} {ib}\n")
