from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 11_primary_color_and_tool_placement_correction(Imagine_Task):
    def load_actors(self):
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
    self.blue_block = self.add_actor("blue_block", "blue_block")
    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
    self.knife = self.add_actor("knife", "knife")
```

---

### ✅ **2. Define the Robot Actions**

We use the `pick_and_place` API to perform the required actions in the correct order:

- **Pick** the `blue_block` and **place** it into the `wooden_box`.
- **Pick** the `screwdriver` and **place** it into the `shoe_box`.
- **Pick** the `knife` and **place** it into the `shoe_box`.

Each step is checked for success, and if any step fails, the robot returns early.

```python

    def play_once(self):
    success = self.pick_and_place(self.blue_block, self.wooden_box)
    print("pick place blue_block:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.screwdriver, self.shoe_box)
    print("pick place screwdriver:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.knife, self.shoe_box)
    print("pick place knife:", success)
    if not success:
        return self.info
```

---

### ✅ **3. Check for Success**

The success condition is verified by checking whether:

- The `blue_block` is **on** the `wooden_box`.
- The `screwdriver` is **on** the `shoe_box`.
- The `knife` is **on** the `shoe_box`.

```python

    
