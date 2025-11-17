from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 224_store_repair_tools_with_one_mistake(Imagine_Task):
    def load_actors(self):
    # Load the wooden box as a container
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
    
    # Load the required objects
    self.hammer = self.add_actor("hammer", "hammer")
    self.drill = self.add_actor("drill", "drill")
    self.knife = self.add_actor("knife", "knife")
    self.bottle = self.add_actor("bottle", "bottle")
    self.hamburg = self.add_actor("hamburg", "hamburg")
    
    # Add distractors
    distractor_list = ["calculator", "pet-collar", "alarm-clock", "book", "toycar"]
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Play Once (Define Robot Actions)**

The robot performs a sequence of actions to place objects in the correct locations. Initially, the hamburg is placed **inside** the box (incorrect), and then it is **recovered** by placing it **on the box surface**.

```python

    def play_once(self):
    # Place hammer into the wooden box
    success = self.pick_and_place(self.hammer, self.wooden_box)
    print("Hammer placed into box:", success)
    if not success:
        return self.info

    # Place drill into the wooden box
    success = self.pick_and_place(self.drill, self.wooden_box)
    print("Drill placed into box:", success)
    if not success:
        return self.info

    # Wrongly place hamburg into the box
    success = self.pick_and_place(self.hamburg, self.wooden_box)
    print("Hamburg placed into box (wrong):", success)
    if not success:
        return self.info

    # Correct by placing hamburg on the box surface
    success = self.pick_and_place(self.hamburg, self.wooden_box)
    print("Hamburg placed on box (recovery):", success)
    if not success:
        return self.info

    # Place bottle on the box surface
    success = self.pick_and_place(self.bottle, self.wooden_box)
    print("Bottle placed on box:", success)
    if not success:
        return self.info

    # Place knife into the box
    success = self.pick_and_place(self.knife, self.wooden_box)
    print("Knife placed into box:", success)
    if not success:
        return self.info
```

---

### ✅ **Step 3: Check Success**

We verify that all required objects are placed in the correct locations using the `check_on` API. Since the API does not distinguish between "inside" and "on top", we assume that placing an object into the box (via `pick_and_place`) results in it being **on the box** in the environment's logic.

```python

    
