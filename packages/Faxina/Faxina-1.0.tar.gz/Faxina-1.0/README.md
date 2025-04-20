# Faxina - Engine 3D for Python 2.4

Faxina is console-based engine 3D for Python 2.4.

---

## What's New?

🧱 **Scene Graph (SceneNode)**
Objects can be parented to each other in a hierarchy. Moving a parent moves all its children.

🗃 **Object Grouping**
Group objects using `add_child()`. Transformations are applied recursively to children.

⚡ **Transform Caching**
World positions are calculated once and cached. Recalculated only when local position changes.

🖥 **Console Renderer**
Renders scene as plain text in the terminal. Supports screen clearing and basic object output.

🔄 **Update System**
Allow each object to define its own `update()` logic (e.g., animation, movement).
Engine already supports `engine.update()`.

🏷 **Tags / Properties**
Attach metadata to objects like `tag = "enemy"` or `set("health", 100)`.

🧠 **Simple Component-Based Architecture**
Components like `TransformComponent`, `PhysicsComponent` separate logic and data cleanly.

📦 Scene Loading from JSON / TXT
Save and load entire scenes from JSON or simple TXT files.
Useful for storing scene configurations and sharing projects.

🎮 Keyboard Input (Console)
Basic controls like WASD for moving objects in the terminal.

The ConsoleRenderer now displays the scene as an ASCII table, showing the object names and their positions.

## Example Code

```python
from faxina.objects import FaxinaObject
from faxina.components import TransformComponent, PhysicsComponent
from faxina.core import FaxinaEngine

# Create engine
engine = FaxinaEngine()

# Create an object
obj = FaxinaObject("Mover")
obj.add_component(TransformComponent([0, 0, 0]))
obj.add_component(PhysicsComponent([1, 0, 0]))

# Add object to engine
engine.add_object(obj)

# Run update loop
for i in range(5):
    engine.update()
    engine.render()