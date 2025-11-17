from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 67_store_tools_and_drinkware_with_disposal_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
    self.dustbin = self.add_actor("dustbin", "dustbin")

    # Add required objects
    self.drill = self.add_actor("drill", "drill")
    self.hammer = self.add_actor("hammer", "hammer")
    self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
    self.apple = self.add_actor("apple", "apple")

    # Add distractors
    distractor_list = ["calculator", "toycar", "alarm-clock", "book", "shoe"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes the correct placement of objects, a wrong placement (apple into `wooden_box`), and a recovery step (apple into `dustbin`). Each action is verified for success, and the function returns early if any step fails.

```python

    def play_once(self):
    # Step 1: Place cup_with_handle into wooden_box
    success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
    print("Place cup_with_handle:", success)
    if not success:
        return self.info

    # Step 2: Place drill into wooden_box
    success = self.pick_and_place(self.drill, self.wooden_box)
    print("Place drill:", success)
    if not success:
        return self.info

    # Step 3: Wrongly place apple into wooden_box
    success = self.pick_and_place(self.apple, self.wooden_box)
    print("Wrongly place apple:", success)
    if not success:
        return self.info

    # Step 4: Recovery - place apple into dustbin
    success = self.pick_and_place(self.apple, self.dustbin)
    print("Recover apple:", success)
    if not success:
        return self.info

    # Step 5: Place hammer into wooden_box
    success = self.pick_and_place(self.hammer, self.wooden_box)
    print("Place hammer:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies that the final state of the environment matches the task requirements. It checks that the repair tools (`drill`, `hammer`) and reusable drinkware (`cup_with_handle`) are in the `wooden_box`, and that the perishable food (`apple`) is in the `dustbin`.

```python

    
