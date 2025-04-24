class World:
    def __init__(self, size):
        self.size = size
        self.blocks = []

    def add_block(self, x, y, z, color):
        self.blocks.append({'x': x, 'y': y, 'z': z, 'color': color})
        print(f"블록 추가됨: 위치({x}, {y}, {z}), 색상: {color}")

    def show(self):
        print(f"{self.size}x{self.size} 맵에 {len(self.blocks)}개의 블록이 있습니다!")
        print("간단한 뷰어 (진짜 3D 뷰어는 이후 개발!)")
