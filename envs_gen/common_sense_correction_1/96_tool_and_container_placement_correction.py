from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 96_tool_and_container_placement_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.coaster = self.add_actor("coaster", "coaster")
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")

    # Add objects
    self.drill = self.add_actor("drill", "drill")
    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
    self.small_speaker = self.add_actor("small-speaker", "small-speaker")
    self.can = self.add_actor("can", "can")

    # Add distractors
    distractor_list = ['baguette', 'apple', 'book', 'pot-with-plant', 'red_block']
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes:

1. **Wrong action**: Place the `drill` on the `coaster` (incorrect).
2. **Recovery action**: Move the `drill` from the `coaster` to the `shoe_box`.
3. Place the `screwdriver` into the `shoe_box`.
4. Place the `small-speaker` onto the `coaster`.
5. Place the `can` onto the `coaster`.

Each action is executed using the `pick_and_place` API, and the function returns early if any step fails.

```python

    def play_once(self):
    # 1. Wrong action: Place drill on coaster
    success = self.pick_and_place(self.drill, self.coaster)
    print("Pick drill and place onto coaster (wrong):", success)
    if not success:
        return self.info

    # 2. Recovery: Move drill to shoe_box
    success = self.pick_and_place(self.drill, self.shoe_box)
    print("Pick drill from coaster and place into shoe_box (recovery):", success)
    if not success:
        return self.info

    # 3. Place screwdriver into shoe_box
    success = self.pick_and_place(self.screwdriver, self.shoe_box)
    print("Pick screwdriver and place into shoe_box:", success)
    if not success:
        return self.info

    # 4. Place small-speaker onto coaster
    success = self.pick_and_place(self.small_speaker, self.coaster)
    print("Pick small-speaker and place onto coaster:", success)
    if not success:
        return self.info

    # 5. Place can onto coaster
    success = self.pick_and_place(self.can, self.coaster)
    print("Pick can and place onto coaster:", success)
    if not success:
        return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the final arrangement of objects meets the task requirements:

- `drill` and `screwdriver` are in the `shoe_box` (repair tools).
- `small-speaker` and `can` are on the `coaster` (small electronics and drink container).

It uses the `check_on` API to verify the placement of each object.

```python

    
