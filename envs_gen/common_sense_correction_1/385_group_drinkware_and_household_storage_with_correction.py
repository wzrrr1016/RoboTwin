from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 385_group_drinkware_and_household_storage_with_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.coaster = self.add_actor("coaster", "coaster")
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")

    # Add objects
    self.bottle = self.add_actor("bottle", "bottle")
    self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
    self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
    self.small_speaker = self.add_actor("small-speaker", "small-speaker")

    # Add distractors
    distractor_list = ["red_block", "green_block", "blue_block", "yellow_block"]
    self.add_distractors(distractor_list)
```

---

#### 2. **`play_once` Function**

This function defines the sequence of actions the robot should perform. It includes a **wrong action** (placing the bottle in the wooden box), followed by a **recovery action** (moving the bottle to the coaster), and then placing the remaining objects in their correct locations.

```python

    def play_once(self):
    # Wrong action: place bottle into wooden_box
    success = self.pick_and_place(self.bottle, self.wooden_box)
    print("Wrong placement (bottle into wooden_box):", success)
    if not success:
        return self.info

    # Recovery: place bottle onto coaster
    success = self.pick_and_place(self.bottle, self.coaster)
    print("Recovery (bottle onto coaster):", success)
    if not success:
        return self.info

    # Place cups onto coaster
    success = self.pick_and_place(self.cup_with_handle, self.coaster)
    print("Cup with handle onto coaster:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.cup_without_handle, self.coaster)
    print("Cup without handle onto coaster:", success)
    if not success:
        return self.info

    # Place small-speaker into wooden_box
    success = self.pick_and_place(self.small_speaker, self.wooden_box)
    print("Small speaker into wooden_box:", success)
    if not success:
        return self.info

    return self.info
```

---

#### 3. **`check_success` Function**

This function verifies whether all the drinkware items are on the coaster and the small-speaker is in the wooden box.

```python

    
