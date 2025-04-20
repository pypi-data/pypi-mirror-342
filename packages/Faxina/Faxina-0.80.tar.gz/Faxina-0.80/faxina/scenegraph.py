class SceneNode:
    def __init__(self, name, position=None):
        self.name = name
        self.position = position or [0, 0, 0]
        self.parent = None
        self.children = []
        self._world_position_cache = None
        self._cache_valid = False

        self.tag = None
        self.components = {}

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        child.invalidate_cache()

    def set_position(self, pos):
        self.position = pos
        self.invalidate_cache()

    def get_world_position(self):
        if self._cache_valid:
            return self._world_position_cache

        if self.parent:
            parent_pos = self.parent.get_world_position()
            self._world_position_cache = [self.position[i] + parent_pos[i] for i in range(3)]
        else:
            self._world_position_cache = list(self.position)

        self._cache_valid = True
        return self._world_position_cache

    def invalidate_cache(self):
        self._cache_valid = False
        for child in self.children:
            child.invalidate_cache()
    def set_component(self, key, value):
        self.components[key] = value

    def get_component(self, key, default=None):
        return self.components.get(key, default)