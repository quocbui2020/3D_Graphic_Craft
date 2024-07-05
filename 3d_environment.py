# https://chatgpt.com/c/3b8b1524-f109-46f4-a8ff-96227603963e
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Custom player controller for third-person view
# class ThirdPersonController(Entity):
#     def __init__(self, **kwargs):
#         super().__init__()
#         self.model = 'cube'
#         self.color = color.orange
#         self.scale_y = 2
#         self.speed = 5
#         self.camera_distance = 5
#         self.min_camera_distance = 2
#         self.max_camera_distance = 10

#         for key, value in kwargs.items():
#             setattr(self, key, value)

#         self.camera_pivot = Entity(parent=self, y=2)
#         camera.parent = self.camera_pivot
#         camera.position = (0, 0, -self.camera_distance)
#         camera.rotation_x = 15
#         camera.look_at(self.camera_pivot, 'forward')

#         # Register scroll input handling
#         window.input = self.handle_zoom

#     def update(self):
#         self.rotation_y += held_keys['d'] * 100 * time.dt
#         self.rotation_y -= held_keys['a'] * 100 * time.dt

#         forward = self.forward * held_keys['w']
#         backward = self.back * held_keys['s']
#         right = self.right * held_keys['d']
#         left = self.left * held_keys['a']

#         move_direction = (forward + backward + right + left).normalized()
#         self.position += move_direction * self.speed * time.dt

#     def handle_zoom(self, key):
#         if key == 'scroll_up':
#             self.camera_distance -= 0.2
#         elif key == 'scroll_down':
#             self.camera_distance += 0.2

#         self.camera_distance = max(self.min_camera_distance, min(self.camera_distance, self.max_camera_distance))
#         camera.position = (0, 0, -self.camera_distance)
#         camera.look_at(self.camera_pivot, 'forward')

# Create Agents (Hiders and Seekers)
class Agent(Entity):
    def __init__(self, position, color, label):
        super().__init__(model='cube', scale=(0.5, 0.5, 0.5), position=position, color=color, collider='box')
        self.speed = 2
        self.label = Text(text=label, scale=2, position=(self.position.x, self.position.y + 1, self.position.z))

    def update(self):
        self.move()
        self.label.position = Vec3(self.position.x, self.position.y + 1, self.position.z)

class Hider(Agent):
    def move(self):
        # direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)) * self.speed * time.dt
        # self.position += direction
        # if self.intersects().hit:
            # self.position -= direction  # Move back if collision detected

        move_interval = 0.0  # Initial delay between movements
        move_speed = 1.0     # Adjust this value to control movement speed (larger values = slower movement)

        if move_interval <= 0:
            move_interval = move_speed  # Reset move_interval for the next movement

            # Randomly generate new position
            new_x = random.uniform(-5, 5)  # Adjust bounds as per your world size
            new_z = random.uniform(-5, 5)
            new_y = 0.5  # Keep the agent at a certain height (adjust as needed)

            # Move the agent to the new position
            self.position = (new_x, new_y, new_z)

seeker_speed = 1
class Seeker(Agent):
    def move(self):
        global seeker_speed
        new_x = self.position.x + time.dt * seeker_speed # Adjust bounds as per your world size
        if abs(self.position.x) > 4.75:
            seeker_speed = seeker_speed * -1

        self.position = (new_x, self.position.y, self.position.z)

# Initialize Ursina
app = Ursina()

# Create player
player = FirstPersonController()
# player = ThirdPersonController()

# Create game environment
group = Entity(model='plane', texture='grass', collider='mesh', scale=(50, 3, 50))

# Create walls
wall1 = Entity(model='cube', scale=(0.1, 1, 10), position=(-5, 0.5, 0), color=color.gray, collider='box')
wall2 = Entity(model='cube', scale=(0.1, 1, 10), position=(5, 0.5, 0), color=color.gray, collider='box')
wall3 = Entity(model='cube', scale=(10, 1, 0.1), position=(0, 0.5, -5), color=color.gray, collider='box')
wall4 = Entity(model='cube', scale=(10, 1, 0.1), position=(0, 0.5, 5), color=color.gray, collider='box')

# Add some movable objects
# box1 = Entity(model='cube', scale=(0.5, 0.5, 0.5), position=(0, 0.25, 0), color=color.red, collider='box')
# box2 = Entity(model='cube', scale=(0.5, 0.5, 0.5), position=(1, 0.25, 1), color=color.blue, collider='box')

# Create agents
hider = Hider(position=(0, 0.25, -2), color=color.green, label='Hider')
seeker = Seeker(position=(0, 0.25, 2), color=color.yellow, label='Seeker')

# Create text entities for coordinates
hider_text = Text(position=(-0.7, 0.45), scale=1.5)
seeker_text = Text(position=(-0.7, 0.40), scale=1.5)



# Create coordinate axes
axis_length = 5

x_axis = Entity(model='cube', scale=(axis_length, 0.05, 0.05), position=(axis_length/2, 0.05, 0), color=color.red)
y_axis = Entity(model='cube', scale=(0.05, axis_length, 0.05), position=(0, axis_length/2, 0), color=color.green)
z_axis = Entity(model='cube', scale=(0.05, 0.05, axis_length), position=(0, 0.05, axis_length/2), color=color.blue)

# Create labels for the axes
x_label = Text(text='X', scale=2, parent=x_axis, position=(0.5, 0.5, 0), origin=(0, 0))
y_label = Text(text='Y', scale=2, parent=y_axis, position=(0.5, 0.5, 0), origin=(0, 0))
z_label = Text(text='Z', scale=2, parent=z_axis, position=(0.5, 0.5, 0), origin=(0, 0))

# Create the camera controller
# camera_controller = Entity()
# camera.parent = camera_controller

# Lighting and sky
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, rotation=(45, -45, 45))
Sky()
window.fullscreen = False

# Define update function to move agents
def update():
    hider.update()
    seeker.update()

    # Update the coordinate text
    hider_text.text = f'Hider: {hider.position}'
    seeker_text.text = f'Seeker: {seeker.position}'

# Run the game
app.run()