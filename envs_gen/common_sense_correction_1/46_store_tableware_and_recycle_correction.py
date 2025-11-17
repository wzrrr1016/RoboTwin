from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 46_store_tableware_and_recycle_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
    self.dustbin = self.add_actor("dustbin", "dustbin")

    # Add objects
    self.fork = self.add_actor("fork", "fork")
    self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
    self.can = self.add_actor("can", "can")
    self.knife = self.add_actor("knife", "knife")

    # Add distractors
    distractor_list = ["calculator", "shoe", "book", "toycar", "markpen"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes:

- Picking and placing the **fork**, **cup_with_handle**, and **knife** into the `wooden_box`.
- A **wrong** action of placing the **can** into the `wooden_box`.
- A **recovery** action of picking the **can** from the `wooden_box` and placing it into the `dustbin`.

Each action is followed by a success check. If any step fails, the function returns early.

```python

    def play_once(self):
    # Step 1: Place fork into wooden_box
    success = self.pick_and_place(self.fork, self.wooden_box)
    print("Pick and place fork:", success)
    if not success:
        return self.info

    # Step 2: Wrongly place can into wooden_box
    success = self.pick_and_place(self.can, self.wooden_box)
    print("Wrongly place can:", success)
    if not success:
        return self.info

    # Step 3: Recovery - move can to dustbin
    success = self.pick_and_place(self.can, self.dustbin)
    print("Recover can:", success)
    if not success:
        return self.info

    # Step 4: Place cup_with_handle into wooden_box
    success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
    print("Place cup_with_handle:", success)
    if not success:
        return self.info

    # Step 5: Place knife into wooden_box
    success = self.pick_and_place(self.knife, self.wooden_box)
    print("Place knife:", success)
    if not success:
        return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the final state of the environment matches the task requirements. It checks:

- All **eating/drinking items** (`fork`, `cup_with_handle`, `knife`) are in the `wooden_box`.
- The **can** is in the `dustbin`.

```python

    
