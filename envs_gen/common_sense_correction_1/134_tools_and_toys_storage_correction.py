from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 134_tools_and_toys_storage_correction(Imagine_Task):
    def load_actors(self):
    # Add the wooden box as a container
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
    
    # Add the required objects
    self.knife = self.add_actor("knife", "knife")
    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
    self.toycar = self.add_actor("toycar", "toycar")
    self.purple_block = self.add_actor("purple_block", "purple_block")
    
    # Add distractors
    distractor_list = ["pot-with-plant", "alarm-clock", "book", "shoe", "tissue-box"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It uses the `pick_and_place` API to move objects from their initial positions to the correct ones. The toycar is first placed incorrectly inside the box and then corrected by placing it on top.

```python

    def play_once(self):
    # Step 1: Pick knife and place into wooden_box
    success = self.pick_and_place(self.knife, self.wooden_box)
    print("Pick and place knife:", success)
    if not success:
        return self.info

    # Step 2: Pick toycar and place into wooden_box (wrong)
    success = self.pick_and_place(self.toycar, self.wooden_box)
    print("Pick and place toycar (wrong):", success)
    if not success:
        return self.info

    # Step 3: Pick toycar from wooden_box and place on wooden_box (recovery)
    success = self.pick_and_place(self.toycar, self.wooden_box)
    print("Pick and place toycar (recovery):", success)
    if not success:
        return self.info

    # Step 4: Pick purple_block and place on wooden_box
    success = self.pick_and_place(self.purple_block, self.wooden_box)
    print("Pick and place purple_block:", success)
    if not success:
        return self.info

    # Step 5: Pick screwdriver and place into wooden_box
    success = self.pick_and_place(self.screwdriver, self.wooden_box)
    print("Pick and place screwdriver:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the task was completed successfully. Since the API only provides `check_on`, we assume that if an object is **not** on the container, it is **inside** the container. This is a reasonable assumption for the given task and API constraints.

```python

    
