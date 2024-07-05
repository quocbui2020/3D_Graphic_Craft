# https://chatgpt.com/c/3b8b1524-f109-46f4-a8ff-96227603963e
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Create Agents (Hiders and Seekers)
class Agent(Entity):
    def __init__(self, position, color):
        super().__init__(model='cube', scale=(0.5, 0.5, 0.5), position=position, color=color, collider='box')
        self.speed = 2

    def update(self):
        self.move()

    def move(self):
        pass

class Hider(Agent):
    def move(self):
        direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)) * self.speed * time.dt
        self.position += direction
        if self.intersects().hit:
            self.position -= direction  # Move back if collision detected

class Seeker(Agent):
    def move(self):
        direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)) * self.speed * time.dt
        self.position += direction
        if self.intersects().hit:
            self.position -= direction  # Move back if collision detected

# Initialize Ursina
app = Ursina()

# Create player
player = FirstPersonController()

# Create game environment
group = Entity(model='plane', texture='grass', collider='mesh', scale=(50, 3, 50))

# Create walls
wall1 = Entity(model='cube', scale=(0.1, 1, 10), position=(-5, 0.5, 0), color=color.gray, collider='box')
wall2 = Entity(model='cube', scale=(0.1, 1, 10), position=(5, 0.5, 0), color=color.gray, collider='box')
wall3 = Entity(model='cube', scale=(10, 1, 0.1), position=(0, 0.5, -5), color=color.gray, collider='box')
wall4 = Entity(model='cube', scale=(10, 1, 0.1), position=(0, 0.5, 5), color=color.gray, collider='box')

# Add some movable objects
box1 = Entity(model='cube', scale=(0.5, 0.5, 0.5), position=(0, 0.25, 0), color=color.red, collider='box')
box2 = Entity(model='cube', scale=(0.5, 0.5, 0.5), position=(1, 0.25, 1), color=color.blue, collider='box')

# Create agents
hider = Hider(position=(0, 0.25, -2), color=color.green)
seeker = Seeker(position=(0, 0.25, 2), color=color.yellow)

# Lighting and sky
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, rotation=(45, -45, 45))
Sky()
window.fullscreen = False

# Define update function to move agents
def update():
    hider.update()
    seeker.update()

# Run the game
app.run()