from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 362_office_stationery_placement_correction(Imagine_Task):
    def load_actors(self):
    # Add the wooden_box as a container
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
    
    # Add the main objects
    self.markpen = self.add_actor("markpen", "markpen")
    self.stapler = self.add_actor("stapler", "stapler")
    self.mouse = self.add_actor("mouse", "mouse")
    self.drill = self.add_actor("drill", "drill")
    self.tissue_box = self.add_actor("tissue-box", "tissue-box")
    
    # Add distractors
    distractor_list = ["pot-with-plant", "sand-clock", "shoe", "red_block"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of robot actions. It places the reusable stationery (`markpen`, `stapler`) into the `wooden_box`, and the electronic or disposable items (`mouse`, `drill`, `tissue-box`) on the `table` (which is assumed to be the surface where the wooden box is placed). The `drill` is first mistakenly placed into the box and then corrected by placing it on the table.

```python

    def play_once(self):
    # Place markpen into wooden_box
    success = self.pick_and_place(self.markpen, self.wooden_box)
    if not success:
        return self.info

    # Place stapler into wooden_box
    success = self.pick_and_place(self.stapler, self.wooden_box)
    if not success:
        return self.info

    # Place mouse on table (on top of wooden_box)
    success = self.pick_and_place(self.mouse, self.table)
    if not success:
        return self.info

    # Wrong action: place drill into wooden_box
    success = self.pick_and_place(self.drill, self.wooden_box)
    if not success:
        return self.info

    # Recovery: pick drill from wooden_box and place on table
    success = self.pick_and_place(self.drill, self.table)
    if not success:
        return self.info

    # Place tissue-box on table
    success = self.pick_and_place(self.tissue_box, self.table)
    if not success:
        return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies that the correct objects are in the correct locations. It checks that the reusable stationery is inside the `wooden_box` and the other items are on the `table` (i.e., on top of the wooden box).

```python

    
