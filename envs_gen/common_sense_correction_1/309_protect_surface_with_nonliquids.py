from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 309_protect_surface_with_nonliquids(Imagine_Task):
    def load_actors(self):
    self.coaster = self.add_actor("coaster", "coaster")
    self.apple = self.add_actor("apple", "apple")
    self.red_block = self.add_actor("red_block", "red_block")
    self.toycar = self.add_actor("toycar", "toycar")
    self.shampoo = self.add_actor("shampoo", "shampoo")
    distractor_list = ["pot-with-plant", "dumbbell", "shoe", "scanner"]
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Define Robot Actions (`play_once`)**

The robot should perform the correct actions: picking and placing the `red_block`, `toycar`, and `apple` onto the `coaster`. The `shampoo` should not be placed on the coaster, so it is left untouched in the environment.

```python

    def play_once(self):
    success = self.pick_and_place(self.red_block, self.coaster)
    print("Place red_block on coaster:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.toycar, self.coaster)
    print("Place toycar on coaster:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.apple, self.coaster)
    print("Place apple on coaster:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **Step 3: Check Task Success (`check_success`)**

The success condition is met if:
- All three solid items (`red_block`, `toycar`, `apple`) are on the coaster.
- The `shampoo` is **not** on the coaster (i.e., it remains in its initial position or is placed elsewhere).

```python

    
