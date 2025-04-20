import os
import time

class ConsoleRenderer:
    def __init__(self, engine):
        self.engine = engine

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def render(self):
        self.clear()

        root = getattr(self.engine, 'root', None)
        if not root or not root.children:
            print("No objects in the scene.")
        else:
            print("Rendering Scene...\n")
            self._render_node(root, 0)

        time.sleep(1)

    def _render_node(self, node, indent):
        if node.name != "Root":
            pos = node.get_world_position()
            print(" " * indent + "%s at position %s" % (node.name, pos))

        for child in node.children:
            self._render_node(child, indent + 2)