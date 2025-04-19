from faxina.scenegraph import SceneNode
from faxina.render import ConsoleRenderer

class FaxinaEngine:
    def __init__(self):
        self.root = SceneNode("Root")
        self.renderer = ConsoleRenderer(self)

    def add_object(self, obj, parent=None):
        if parent is None:
            self.root.add_child(obj)
        else:
            parent.add_child(obj)

    def update(self):
        self._recursive_update(self.root)

    def _recursive_update(self, node):
        if hasattr(node, 'update'):
            node.update()
        for child in node.children:
            self._recursive_update(child)

    def render(self):
        self.renderer.render()