from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 466_edible_items_on_plate_correction(Imagine_Task):
    def load_actors(self):
    self.plate = self.add_actor("plate", "plate")
    self.apple = self.add_actor("apple", "apple")
    self.hamburg = self.add_actor("hamburg", "hamburg")
    self.french_fries = self.add_actor("french_fries", "french_fries")
    self.mug = self.add_actor("mug", "mug")
    distractor_list = ["calculator", "screwdriver", "toycar", "alarm-clock", "tissue-box"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It uses the `pick_and_place` API to move the edible items (`apple`, `hamburg`, `french_fries`) onto the `plate`. If any of these actions fail, the function returns early to avoid unnecessary operations.

```python

    def play_once(self):
    success = self.pick_and_place(self.apple, self.plate)
    print("pick place apple:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.hamburg, self.plate)
    print("pick place hamburg:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.french_fries, self.plate)
    print("pick place french_fries:", success)
    if not success:
        return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the task was completed successfully. It checks that all three edible items are on the plate and that the non-edible `mug` is **not** on the plate. This ensures that the robot did not mistakenly place the mug on the plate, which would be considered an error.

```python

    
