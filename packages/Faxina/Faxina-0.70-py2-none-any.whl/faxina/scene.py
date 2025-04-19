class Object3D:
    def __init__(self, name, pos):
        self.name = name
        self.position = pos

    def update(self):
        pass

    def __str__(self):
        return "%s at %s" % (self.name, str(self.position))