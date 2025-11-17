from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 37_organize_play_and_storage_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.tray = self.add_actor("tray", "tray")
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")

    # Add objects
    self.toycar = self.add_actor("toycar", "toycar")
    self.green_block = self.add_actor("green_block", "green_block")
    self.yellow_block = self.add_actor("yellow_block", "yellow_block")
    self.fork = self.add_actor("fork", "fork")
    self.shampoo = self.add_actor("shampoo", "shampoo")

    # Add distractors
    distractor_list = ["calculator", "screwdriver", "pot-with-plant", "alarm-clock", "book"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes a **wrong action** (placing the fork on the tray) and a **recovery action** (moving the fork to the shoe_box). Each action is executed using the `pick_and_place` API, and the function returns early if any step fails.

```python

    def play_once(self):
    # Step 1: Place toycar on tray
    success = self.pick_and_place(self.toycar, self.tray)
    print("Place toycar on tray:", success)
    if not success:
        return self.info

    # Step 2: Place green_block on tray
    success = self.pick_and_place(self.green_block, self.tray)
    print("Place green_block on tray:", success)
    if not success:
        return self.info

    # Step 3: Wrong action - Place fork on tray
    success = self.pick_and_place(self.fork, self.tray)
    print("Place fork on tray (wrong):", success)
    if not success:
        return self.info

    # Step 4: Recovery - Move fork to shoe_box
    success = self.pick_and_place(self.fork, self.shoe_box)
    print("Move fork to shoe_box:", success)
    if not success:
        return self.info

    # Step 5: Place yellow_block on tray
    success = self.pick_and_place(self.yellow_block, self.tray)
    print("Place yellow_block on tray:", success)
    if not success:
        return self.info

    # Step 6: Place shampoo in shoe_box
    success = self.pick_and_place(self.shampoo, self.shoe_box)
    print("Place shampoo in shoe_box:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies that the final configuration matches the task requirements. It checks that all **play items** (toys and blocks) are on the `tray`, and that **personal-care items** and **eating utensils** are in the `shoe_box`.

```python

    
