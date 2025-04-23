class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.press = False

class Keyboard:
    def __init__(self):
        self.keys = {}

    def update_key(self, vk_code, pressed):
        self.keys[vk_code] = pressed

    def __getitem__(self, key):
        return self.keys.get(key, False)
