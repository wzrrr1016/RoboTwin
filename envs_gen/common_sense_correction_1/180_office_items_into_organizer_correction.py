from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 180_office_items_into_organizer_correction(Imagine_Task):
    def load_actors(self):
    # Add the container
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")
    
    # Add the relevant objects
    self.stapler = self.add_actor("stapler", "stapler")
    self.mouse = self.add_actor("mouse", "mouse")
    self.toycar = self.add_actor("toycar", "toycar")
    self.apple = self.add_actor("apple", "apple")
    
    # Add distractors
    distractor_list = ["pot-with-plant", "shoe", "dumbbell", "hammer"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of robot actions. It includes:

- A **wrong action**: placing the apple in the `fluted_block`.
- A **recovery action**: placing the apple back on the table.
- **Correct actions**: placing the stapler and mouse in the `fluted_block`, and the toycar on the table.

```python

    def play_once(self):
    # Wrong action: place apple into fluted_block
    success = self.pick_and_place(self.apple, self.fluted_block)
    print("Wrong action: pick place apple:", success)
    if not success:
        return self.info

    # Recovery: place apple back on the table
    success = self.pick_and_place(self.apple, self.table)
    print("Recovery: pick place apple on table:", success)
    if not success:
        return self.info

    # Correct actions
    success = self.pick_and_place(self.stapler, self.fluted_block)
    print("pick place stapler:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.mouse, self.fluted_block)
    print("pick place mouse:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.toycar, self.table)
    print("pick place toycar on table:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies that the final state of the environment matches the task requirements:

- `stapler` and `mouse` are in the `fluted_block`.
- `toycar` and `apple` are on the table.

```python

    
