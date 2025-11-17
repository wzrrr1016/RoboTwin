from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 421_store_toys_keep_liquids_and_weights_outside(Imagine_Task):
    def load_actors(self):
    # Add the shoe box as the main container
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")

    # Add the required objects
    self.green_block = self.add_actor("green_block", "green_block")
    self.blue_block = self.add_actor("blue_block", "blue_block")
    self.pink_block = self.add_actor("pink_block", "pink_block")
    self.shampoo = self.add_actor("shampoo", "shampoo")
    self.dumbbell = self.add_actor("dumbbell", "dumbbell")

    # Add distractors to the environment
    distractor_list = ["calculator", "alarm-clock", "tissue-box", "stapler", "mouse", "microphone"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot should perform. It includes placing the blocks into the shoe box, placing the shampoo and dumbbell on top, and correcting the incorrect placement of the dumbbell.

```python

    def play_once(self):
    # Place green_block into shoe_box
    success = self.pick_and_place(self.green_block, self.shoe_box)
    if not success:
        return self.info

    # Place blue_block into shoe_box
    success = self.pick_and_place(self.blue_block, self.shoe_box)
    if not success:
        return self.info

    # Place shampoo on top of shoe_box
    success = self.pick_and_place(self.shampoo, self.shoe_box)
    if not success:
        return self.info

    # Place dumbbell into shoe_box (wrong action)
    success = self.pick_and_place(self.dumbbell, self.shoe_box)
    if not success:
        return self.info

    # Recovery: pick dumbbell from shoe_box and place it on top
    success = self.pick_and_place(self.dumbbell, self.shoe_box)
    if not success:
        return self.info

    # Place pink_block into shoe_box
    success = self.pick_and_place(self.pink_block, self.shoe_box)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the task was completed successfully. It checks that the shampoo and dumbbell are on top of the shoe box and that the blocks are not on top (implying they are inside the box).

```python

    
