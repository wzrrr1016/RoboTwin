from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 264_dispose_unsafe_drinkware_and_electronics_correction(Imagine_Task):
    def load_actors(self):
    # Add the dustbin container
    self.dustbin = self.add_actor("dustbin", "dustbin")
    # Add the required objects
    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
    self.mouse = self.add_actor("mouse", "mouse")
    self.mug = self.add_actor("mug", "mug")
    self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
    self.orange_block = self.add_actor("orange_block", "orange_block")
    # Add distractors
    distractor_list = ["book", "shoe", "baguette", "dumbbell", "tissue-box"]
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Play Once (Robot Actions)**

The robot must perform the following sequence of actions:

1. **Wrong Action**: Pick up the `mug` and place it in the `dustbin`.
2. **Recovery Action**: Pick up the `mug` from the `dustbin` and place it on the `orange_block`.
3. **Correct Actions**:
   - Pick up the `cup_without_handle` and place it in the `dustbin`.
   - Pick up the `mouse` and place it in the `dustbin`.

Each action is executed using the `pick_and_place` API, and the function returns early if any step fails.

```python

    def play_once(self):
    # 1. Wrong action: Put mug into dustbin
    success = self.pick_and_place(self.mug, self.dustbin)
    print("Put mug into dustbin (wrong):", success)
    if not success:
        return self.info

    # 2. Recovery: Put mug onto orange_block
    success = self.pick_and_place(self.mug, self.orange_block)
    print("Recover: Put mug onto orange_block:", success)
    if not success:
        return self.info

    # 3. Correct action: Put cup_without_handle into dustbin
    success = self.pick_and_place(self.cup_without_handle, self.dustbin)
    print("Put cup_without_handle into dustbin:", success)
    if not success:
        return self.info

    # 4. Correct action: Put mouse into dustbin
    success = self.pick_and_place(self.mouse, self.dustbin)
    print("Put mouse into dustbin:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **Step 3: Check Success**

The task is considered successful if:

- `cup_without_handle` is in the `dustbin`
- `mouse` is in the `dustbin`
- `mug` is on the `orange_block` (not in the dustbin)

We use the `check_on` API to verify the positions of the objects.

```python

    
