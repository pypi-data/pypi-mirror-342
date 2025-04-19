# render.py
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

        if len(self.engine.objects) == 0:
            print("No objects in the scene.")
        else:
            print("Rendering Scene...")
            for obj in self.engine.objects:
                print("%s at position %s" % (obj.name, obj.position))

        time.sleep(1)