from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 452_store_snacks_and_place_fragile_decor_on_top_correction(Imagine_Task):
    def load_actors(self):
    # Add the wooden box container
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")

    # Add edible perishable snacks
    self.french_fries = self.add_actor("french_fries", "french_fries")
    self.bread = self.add_actor("bread", "bread")

    # Add fragile decorative items
    self.mug = self.add_actor("mug", "mug")
    self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    # Add distractors
    distractor_list = ["calculator", "screwdriver", "dumbbell", "shoe", "book"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes a wrong action (placing the mug into the box), followed by a recovery action (placing the mug on top of the box), and then placing the correct items.

```python

    def play_once(self):
    # Wrong action: place mug into wooden_box
    success = self.pick_and_place(self.mug, self.wooden_box)
    print("Wrong action (place mug into box):", success)
    if not success:
        # Recovery: place mug on wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Recovery action (place mug on box):", success)
        if not success:
            return self.info

    # Place edible perishable snacks into wooden_box
    success = self.pick_and_place(self.french_fries, self.wooden_box)
    print("Place french fries into box:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.bread, self.wooden_box)
    print("Place bread into box:", success)
    if not success:
        return self.info

    # Place fragile decorative item on wooden_box
    success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
    print("Place pot-with-plant on box:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the task was completed successfully by checking the final positions of the objects using the `check_on` API.

```python

    
