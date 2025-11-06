from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 44_edible_items_placement_correction(Imagine_Task):
    def load_actors(self):
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")
    self.bread = self.add_actor("bread", "bread")
    self.fork = self.add_actor("fork", "fork")
    self.red_block = self.add_actor("red_block", "red_block")
    self.scanner = self.add_actor("scanner", "scanner")
    self.bottle = self.add_actor("bottle", "bottle")
```

---

#### 2. **Play Once (Action)**
We use the `pick_and_place` API to:
- **Pick the bread**.
- **Place it into the fluted_block**.

```python

    def play_once(self):
    success = self.pick_and_place(self.bread, self.fluted_block)
    print("pick place bread:", success)
    if not success:
        return self.info
```

---

#### 3. **Check Success**
We verify that the **bread** is now **on the fluted_block** using the `check_on` API.

```python

    
