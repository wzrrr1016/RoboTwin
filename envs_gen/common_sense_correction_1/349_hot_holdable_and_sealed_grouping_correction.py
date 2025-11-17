from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 349_hot_holdable_and_sealed_grouping_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")

    # Add objects
    self.mug = self.add_actor("mug", "mug")
    self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
    self.can = self.add_actor("can", "can")
    self.bottle = self.add_actor("bottle", "bottle")

    # Add distractors
    distractor_list = ['calculator', 'toycar', 'book', 'alarm-clock', 'small-speaker']
    self.add_distractors(distractor_list)
```

---

### 🤖 Step 2: Play Once (Define Robot Actions)

The robot performs a sequence of actions to place objects in the correct containers. The sequence includes a **wrong action** (placing the can on the fluted_block) followed by a **recovery action** (moving the can to the shoe_box), as specified in the task.

```python

    def play_once(self):
    # 1. Pick mug and place on fluted_block
    success = self.pick_and_place(self.mug, self.fluted_block)
    print("Pick mug:", success)
    if not success:
        return self.info

    # 2. Pick can and place on fluted_block (wrong)
    success = self.pick_and_place(self.can, self.fluted_block)
    print("Pick can (wrong):", success)
    if not success:
        return self.info

    # 3. Pick can from fluted_block and place into shoe_box (recovery)
    success = self.pick_and_place(self.can, self.shoe_box)
    print("Recover can:", success)
    if not success:
        return self.info

    # 4. Pick cup_with_handle and place on fluted_block
    success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
    print("Pick cup_with_handle:", success)
    if not success:
        return self.info

    # 5. Pick bottle and place into shoe_box
    success = self.pick_and_place(self.bottle, self.shoe_box)
    print("Pick bottle:", success)
    if not success:
        return self.info
```

---

### ✅ Step 3: Check Success

We verify that all objects are in their correct final positions using the `check_on` method.

```python

    
