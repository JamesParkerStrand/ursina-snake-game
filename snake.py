from ursina import *
import numpy as np
from random import uniform
from math import sqrt

app = Ursina()

y_mov = 0
x_mov = 1

cube = load_model("cube", use_deepcopy=True)
list1 = np.asarray([])

resized_cube = np.asarray(cube.vertices) * 0.2
game_over = False
speed = 1
body = []
iteration = 0

def update():
    global y_mov, x_mov, snake_limit, list1, game_over, iteration, snake_model, speed
    if not game_over:
        for x in range(speed):
            snake_head.y += y_mov * time.dt
            snake_head.x += x_mov * time.dt
            orx = snake_head.x + (x_mov * 0.11)
            ory = snake_head.y + (y_mov * 0.11)
            iteration += 0.7

            if iteration > 5 and snake_limit != 0:
                iteration = 0
                base_cube = np.copy(resized_cube[:])
                base_cube[:, 0] += snake_head.x
                base_cube[:, 1] += snake_head.y
                list1 = np.append(list1, base_cube)

                shaper = len(list1) // 3
                list1 = list1.reshape((int(shaper), 3))
                list1 = np.ndarray.tolist(list1)
                snake_model.model.vertices = [tuple(e) for e in list1]

                # Create normals and uvs to match the number of vertices
                snake_model.model.normals = [Vec3(0, 0, 1)] * len(snake_model.model.vertices)
                snake_model.model.uvs = [(0, 0)] * len(snake_model.model.vertices)

                if len(list1) > 36 * snake_limit:
                    del list1[0:36]

                snake_model.model.generate()
                snake_model.collider = MeshCollider(snake_model, mesh=snake_model.model)

            hit = boxcast(origin=LVector3f(orx, ory, 0), direction=LVector3f(x_mov, y_mov, 0), distance=0.03, thickness=(0.2, 0.2))
            if hit.hit:
                if hit.entity in border or hit.entity == snake_model:
                    game_over = True
                if hit.entity == food:
                    snake_limit += 1
                    if snake_limit % 10 == 0:
                        speed += 1
                    food.y = uniform(-3.2, 3.2)
                    food.x = uniform(-6.5, 6.5)

def input(key):
    global y_mov, x_mov
    if key == "w":
        y_mov = 1
        x_mov = 0
    if key == "s":
        y_mov = -1
        x_mov = 0
    if key == "d":
        x_mov = 1
        y_mov = 0
    if key == "a":
        x_mov = -1
        y_mov = 0

snake_number = 0
snake_limit = 0

border = [Entity(model="cube", scale=(15,0.5,1), position=(0,4.2,0), collider="box", color=color.red),
          Entity(model="cube", scale=(15,0.5,1), position=(0,-4.2,0), collider="box", color=color.red),
          Entity(model="cube", scale=(0.5,15,1), position=(7.5,0,0), collider="box", color=color.red),
          Entity(model="cube", scale=(0.5,15,1), position=(-7.5,0,0), collider="box", color=color.red)]

snake_model = Entity(model=cube, color=color.yellow, scale=1)
snake_model.collider = MeshCollider(snake_model, mesh=snake_model.model)
snake_model.model.vertices = []

snake_model.model.generate()

snake_model.collider = MeshCollider(snake_model,mesh=snake_model.model)

snake_head = Entity(model="cube", color=color.yellow, scale=0.2)
food = Entity(model="cube", color=color.blue, scale=0.2, y=uniform(-3.2, 3.2), x=uniform(-6.5, 6.5), collider="box")

Sky()

app.run()
