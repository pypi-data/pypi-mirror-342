import sys

class KeyboardController:
    def __init__(self, target_object):
        self.target = target_object

    def handle_input(self):
        print("[W/A/S/D] to move, [Q] to quit")
        key = raw_input("Key: ").lower()

        if key == 'w':
            self.target.position[1] += 1
        elif key == 's':
            self.target.position[1] -= 1
        elif key == 'a':
            self.target.position[0] -= 1
        elif key == 'd':
            self.target.position[0] += 1
        elif key == 'q':
            print("Quitting...")
            sys.exit()
        else:
            print("Invalid key.")