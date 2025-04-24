from ursina import *

class World:
    def __init__(self, size):
        self.size = size
        self.blocks = []

    def add_block(self, x, y, z, color):
        self.blocks.append({'x': x, 'y': y, 'z': z, 'color': color})
        print(f"Block placed at ({x}, {y}, {z}) with color {color}")

    def show(self):
        app = Ursina()

        for block in self.blocks:
            Entity(
                model='cube',
                color=color_dict.get(block['color'], color.white),
                position=(block['x'], block['y'], block['z']),
                scale=1
            )

        camera.position = (self.size/2, self.size/2, -self.size*2)
        camera.look_at((self.size/2, 0, self.size/2))
        app.run()

# 색상 매핑 딕셔너리
color_dict = {
    'green': color.green,
    'brown': color.brown,
    'red': color.red,
    'blue': color.azure,
    'white': color.white
}
