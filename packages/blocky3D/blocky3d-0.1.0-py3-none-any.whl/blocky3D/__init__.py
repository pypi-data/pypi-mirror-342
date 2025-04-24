from .engine import World

# 초보자용 함수
def create_world(size=10):
    global world
    world = World(size)

def place_block(x, y, z, color='white'):
    world.add_block(x, y, z, color)

def start_viewer():
    world.show()
