class Component(object):
    def __init__(self):
        self.owner = None

    def update(self):
        pass


class TransformComponent(Component):
    def __init__(self, position=None):
        Component.__init__(self)
        self.position = position or [0, 0, 0]

    def set_position(self, pos):
        self.position = pos

    def get_position(self):
        return self.position


class PhysicsComponent(Component):
    def __init__(self, velocity=None):
        Component.__init__(self)
        self.velocity = velocity or [0, 0, 0]

    def update(self):
        transform = self.owner.get_component(TransformComponent)
        if transform:
            for i in range(3):
                transform.position[i] += self.velocity[i]