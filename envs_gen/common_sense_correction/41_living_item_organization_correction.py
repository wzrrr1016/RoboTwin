from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 41_living_item_organization_correction(Imagine_Task):
    def load_actors(self):
    self.sand_clock = self.add_actor("sand-clock", "sand-clock")
    self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
    self.dumbbell = self.add_actor("dumbbell", "dumbbell")
    self.toycar = self.add_actor("toycar", "toycar")
    self.hammer = self.add_actor("hammer", "hammer")
```

---

### ✅ **Step 2: Play Once (Action)**

We use the `pick_and_place` API to pick the `pot-with-plant` and place it into the `fluted_block`. If the action fails, we return early to avoid unnecessary steps.

```python

    def play_once(self):
    success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
    print("pick place pot_with_plant:", success)
    if not success:
        return self.info
```

---

### ✅ **Step 3: Check Success**

We verify that the `pot-with-plant` is now on the `fluted_block` using the `check_on` API.

```python

    
