from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 107_tools_and_toys_placement_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")

    # Add objects
    self.green_block = self.add_actor("green_block", "green_block")
    self.yellow_block = self.add_actor("yellow_block", "yellow_block")
    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
    self.stapler = self.add_actor("stapler", "stapler")

    # Add distractors
    distractor_list = ["pot-with-plant", "alarm-clock", "book", "baguette", "apple"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. The robot must:

1. **Incorrectly** place the `screwdriver` into the `shoe_box`.
2. **Correct** the mistake by picking the `screwdriver` from the `shoe_box` and placing it onto the `fluted_block`.
3. Place the `stapler` onto the `fluted_block`.
4. Place the `green_block` and `yellow_block` into the `shoe_box`.

Each action is executed using the `pick_and_place` API. If any step fails, the function returns early to prevent unnecessary actions.

```python

    def play_once(self):
    # Step 1: Place screwdriver into shoe_box (wrong)
    success = self.pick_and_place(self.screwdriver, self.shoe_box)
    print("Place screwdriver into shoe_box:", success)
    if not success:
        return self.info

    # Step 2: Recovery - place screwdriver onto fluted_block
    success = self.pick_and_place(self.screwdriver, self.fluted_block)
    print("Recover screwdriver to fluted_block:", success)
    if not success:
        return self.info

    # Step 3: Place stapler onto fluted_block
    success = self.pick_and_place(self.stapler, self.fluted_block)
    print("Place stapler:", success)
    if not success:
        return self.info

    # Step 4: Place green_block into shoe_box
    success = self.pick_and_place(self.green_block, self.shoe_box)
    print("Place green_block:", success)
    if not success:
        return self.info

    # Step 5: Place yellow_block into shoe_box
    success = self.pick_and_place(self.yellow_block, self.shoe_box)
    print("Place yellow_block:", success)
    if not success:
        return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the task was completed successfully. It checks if:

- The `green_block` and `yellow_block` are on the `shoe_box`.
- The `screwdriver` and `stapler` are on the `fluted_block`.

```python

    
