class SceneNode:
    def __init__(self, name="Node", position=None):
        if position is None:
            position = [0, 0, 0]
        self.name = name
        self.position = position
        self.children = []
        self.parent = None

        self._cached_world_position = None

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        child_node.invalidate_cache()

    def set_position(self, new_position):
        self.position = new_position
        self.invalidate_cache()

    def invalidate_cache(self):
        self._cached_world_position = None
        for child in self.children:
            child.invalidate_cache()

    def get_world_position(self):
        if self._cached_world_position is not None:
            return self._cached_world_position

        if self.parent:
            parent_pos = self.parent.get_world_position()
            result = [
                self.position[0] + parent_pos[0],
                self.position[1] + parent_pos[1],
                self.position[2] + parent_pos[2]
            ]
        else:
            result = self.position[:]

        self._cached_world_position = result
        return result

    def print_tree(self, indent=0):
        print(" " * indent + self.name + " at " + str(self.get_world_position()))
        for child in self.children:
            child.print_tree(indent + 2)