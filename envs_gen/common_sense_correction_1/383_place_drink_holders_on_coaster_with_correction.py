from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 383_place_drink_holders_on_coaster_with_correction(Imagine_Task):
    def load_actors(self):
    # Add the coaster
    self.coaster = self.add_actor("coaster", "coaster")
    # Add objects
    self.mug = self.add_actor("mug", "mug")
    self.bottle = self.add_actor("bottle", "bottle")
    self.bread = self.add_actor("bread", "bread")
    self.stapler = self.add_actor("stapler", "stapler")
    # Add distractors
    distractors = ["calculator", "pet-collar", "toycar", "book", "shoe"]
    self.add_distractors(distractors)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of robot actions. The robot:

1. Places the **mug** on the coaster.
2. Places the **bread** on the coaster (this is a mistake).
3. Corrects the mistake by placing the **bread** back on the table.
4. Places the **bottle** on the coaster.
5. Places the **stapler** on the table.

Each action is followed by a success check. If any step fails, the function returns early.

```python

    def play_once(self):
    # Place mug on coaster
    success = self.pick_and_place(self.mug, self.coaster)
    print("Pick and place mug:", success)
    if not success:
        return self.info

    # Place bread on coaster (wrong)
    success = self.pick_and_place(self.bread, self.coaster)
    print("Pick and place bread (wrong):", success)
    if not success:
        return self.info

    # Move bread back to table
    success = self.pick_and_place(self.bread, self.table)
    print("Move bread to table:", success)
    if not success:
        return self.info

    # Place bottle on coaster
    success = self.pick_and_place(self.bottle, self.coaster)
    print("Pick and place bottle:", success)
    if not success:
        return self.info

    # Place stapler on table
    success = self.pick_and_place(self.stapler, self.table)
    print("Pick and place stapler:", success)
    if not success:
        return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies the final state of the environment. It checks:

- The **mug** and **bottle** are on the coaster (they hold liquids).
- The **bread** and **stapler** are **not** on the coaster (bread is perishable, stapler is a tool).

```python

    
