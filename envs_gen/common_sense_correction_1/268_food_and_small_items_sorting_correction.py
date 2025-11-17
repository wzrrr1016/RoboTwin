from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 268_food_and_small_items_sorting_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.coaster = self.add_actor("coaster", "coaster")
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")

    # Add relevant objects
    self.apple = self.add_actor("apple", "apple")
    self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
    self.markpen = self.add_actor("markpen", "markpen")
    self.blue_block = self.add_actor("blue_block", "blue_block")

    # Add distractors
    distractor_list = ["hammer", "shoe", "pot-with-plant", "alarm-clock", "dumbbell"]
    self.add_distractors(distractor_list)
```

---

### ✅ `play_once`

This function defines the sequence of actions the robot should perform. It includes:

1. **Wrong action**: Place the apple in the wooden_box.
2. **Recovery action**: Move the apple to the coaster.
3. **Correct actions**:
   - Place the cup_without_handle on the coaster.
   - Place the markpen and blue_block in the wooden_box.

Each action is followed by a success check. If any step fails, the function returns early.

```python

    def play_once(self):
    # Wrong action: Place apple in wooden_box
    success = self.pick_and_place(self.apple, self.wooden_box)
    print("Wrong apple placement:", success)
    if not success:
        return self.info

    # Recovery: Move apple to coaster
    success = self.pick_and_place(self.apple, self.coaster)
    print("Recovery apple:", success)
    if not success:
        return self.info

    # Place cup_without_handle on coaster
    success = self.pick_and_place(self.cup_without_handle, self.coaster)
    print("Cup placement:", success)
    if not success:
        return self.info

    # Place markpen in wooden_box
    success = self.pick_and_place(self.markpen, self.wooden_box)
    print("Markpen placement:", success)
    if not success:
        return self.info

    # Place blue_block in wooden_box
    success = self.pick_and_place(self.blue_block, self.wooden_box)
    print("Blue block placement:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ `check_success`

This function verifies that all relevant objects are in their correct final positions:

- `apple` and `cup_without_handle` on the **coaster**
- `markpen` and `blue_block` in the **wooden_box**

```python

    
