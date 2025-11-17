from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 7_repair_tool_and_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.coaster = self.add_actor("coaster", "coaster")
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")

    # Add objects
    self.can = self.add_actor("can", "can")
    self.drill = self.add_actor("drill", "drill")
    self.hammer = self.add_actor("hammer", "hammer")

    # Add distractors
    distractor_list = ["calculator", "pet-collar", "table-tennis", "baguette", "scanner"]
    self.add_distractors(distractor_list)

    # Finalize scene setup
    self.check_scene()
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes:

1. **Incorrect action**: Place the `can` into the `fluted_block` (wrong).
2. **Recovery action**: Move the `can` from the `fluted_block` to the `coaster`.
3. **Correct actions**: Place the `drill` and `hammer` into the `fluted_block`.

Each action is executed using the `pick_and_place` API, and the function returns early if any step fails.

```python

    def play_once(self):
    # Step 1: Place can into fluted_block (wrong action)
    success = self.pick_and_place(self.can, self.fluted_block)
    print("Pick can into fluted_block (wrong):", success)
    if not success:
        return self.info

    # Step 2: Recover can to coaster
    success = self.pick_and_place(self.can, self.coaster)
    print("Recover can to coaster:", success)
    if not success:
        return self.info

    # Step 3: Place drill into fluted_block
    success = self.pick_and_place(self.drill, self.fluted_block)
    print("Place drill:", success)
    if not success:
        return self.info

    # Step 4: Place hammer into fluted_block
    success = self.pick_and_place(self.hammer, self.fluted_block)
    print("Place hammer:", success)
    if not success:
        return self.info

    # Mark the end of the task
    self.add_end()
    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the final state of the environment matches the task requirements:

- The `can` (drinkware) is on the `coaster`.
- The `drill` and `hammer` (repair tools) are on the `fluted_block`.

It uses the `check_on` API to validate the placement of each object.

```python

    
