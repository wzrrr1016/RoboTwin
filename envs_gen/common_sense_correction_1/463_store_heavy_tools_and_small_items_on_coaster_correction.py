from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 463_store_heavy_tools_and_small_items_on_coaster_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
    self.coaster = self.add_actor("coaster", "coaster")

    # Add objects
    self.hammer = self.add_actor("hammer", "hammer")
    self.drill = self.add_actor("drill", "drill")
    self.bottle = self.add_actor("bottle", "bottle")
    self.mouse = self.add_actor("mouse", "mouse")

    # Add distractors
    distractor_list = ["apple", "baguette", "book", "pot-with-plant", "tissue-box"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes a **wrong action** (placing the hammer on the coaster), followed by a **recovery action** (moving the hammer to the shoe_box), and then placing the remaining objects in the correct locations.

```python

    def play_once(self):
    # Wrong action: Place hammer on coaster
    success = self.pick_and_place(self.hammer, self.coaster)
    print("Hammer to coaster (wrong):", success)
    if not success:
        return self.info

    # Recovery: Move hammer to shoe_box
    success = self.pick_and_place(self.hammer, self.shoe_box)
    print("Hammer to shoe_box (recovery):", success)
    if not success:
        return self.info

    # Place drill in shoe_box
    success = self.pick_and_place(self.drill, self.shoe_box)
    print("Drill to shoe_box:", success)
    if not success:
        return self.info

    # Place bottle on coaster
    success = self.pick_and_place(self.bottle, self.coaster)
    print("Bottle to coaster:", success)
    if not success:
        return self.info

    # Place mouse on coaster
    success = self.pick_and_place(self.mouse, self.coaster)
    print("Mouse to coaster:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies that all objects are placed in the correct containers as per the task description.

- **Heavy repair tools** (`hammer`, `drill`) should be in the `shoe_box`.
- **Small electronics or drinkware** (`bottle`, `mouse`) should be on the `coaster`.

```python

    
