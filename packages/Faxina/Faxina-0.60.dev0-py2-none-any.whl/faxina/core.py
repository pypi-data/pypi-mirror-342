from render import ConsoleRenderer

class FaxinaEngine:
    def __init__(self):
        self.objects = []
        self.renderer = ConsoleRenderer(self)

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self):
        for obj in self.objects:
            obj.update()

    def render(self):
        self.renderer.render()