class FaxinaObject(object):
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        component.owner = self
        self.components.append(component)

    def get_component(self, comp_type):
        for comp in self.components:
            if isinstance(comp, comp_type):
                return comp
        return None

    def update(self):
        for comp in self.components:
            comp.update()