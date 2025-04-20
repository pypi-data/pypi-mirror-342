import simplejson as json
from faxina.objects import FaxinaObject
from faxina.components import TransformComponent, PhysicsComponent

class SceneLoader:
    def __init__(self, engine):
        self.engine = engine

    def load_from_json(self, path):
        f = open(path, 'r')
        data = json.load(f)
        f.close()

        for obj_data in data['objects']:
            name = obj_data.get('name', 'Unnamed')
            obj = FaxinaObject(name)

            if 'TransformComponent' in obj_data:
                obj.add_component(TransformComponent(obj_data['TransformComponent']))

            if 'PhysicsComponent' in obj_data:
                obj.add_component(PhysicsComponent(obj_data['PhysicsComponent']))

            self.engine.add_object(obj)

        print("Scene loaded from", path)