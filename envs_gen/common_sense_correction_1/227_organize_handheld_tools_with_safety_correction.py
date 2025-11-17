from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 227_organize_handheld_tools_with_safety_correction(Imagine_Task):
    def load_actors(self):
    # Add the organizer container
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")

    # Add the required objects
    self.stapler = self.add_actor("stapler", "stapler")
    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
    self.hammer = self.add_actor("hammer", "hammer")
    self.knife = self.add_actor("knife", "knife")
    self.purple_block = self.add_actor("purple_block", "purple_block")

    # Add distractors
    distractor_list = ['apple', 'book', 'tissue-box', 'toycar', 'pot-with-plant']
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Play Once (Define Robot Actions)**

The robot performs a sequence of actions to complete the task. It places the stapler, screwdriver, and hammer into the `fluted_block`, mistakenly places the knife into the container, and then recovers by placing the knife on the table. Finally, it places the `purple_block` into the container.

```python

    def play_once(self):
    # Place stapler into fluted_block
    success = self.pick_and_place(self.stapler, self.fluted_block)
    print("Pick and place stapler:", success)
    if not success:
        return self.info

    # Place screwdriver into fluted_block
    success = self.pick_and_place(self.screwdriver, self.fluted_block)
    print("Pick and place screwdriver:", success)
    if not success:
        return self.info

    # Wrongly place knife into fluted_block
    success = self.pick_and_place(self.knife, self.fluted_block)
    print("Pick and place knife (wrong):", success)
    if not success:
        return self.info

    # Recovery: place knife on table
    success = self.pick_and_place(self.knife, self.table)
    print("Pick and place knife on table:", success)
    if not success:
        return self.info

    # Place hammer into fluted_block
    success = self.pick_and_place(self.hammer, self.fluted_block)
    print("Pick and place hammer:", success)
    if not success:
        return self.info

    # Place purple_block into fluted_block
    success = self.pick_and_place(self.purple_block, self.fluted_block)
    print("Pick and place purple block:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **Step 3: Check Success**

The success condition is verified by checking if the correct objects are in the correct locations:

- `stapler`, `screwdriver`, `hammer`, and `purple_block` are in the `fluted_block`
- `knife` is on the `table`

```python

    
