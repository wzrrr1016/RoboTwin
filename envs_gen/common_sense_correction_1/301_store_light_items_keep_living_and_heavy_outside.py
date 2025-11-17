from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 301_store_light_items_keep_living_and_heavy_outside(Imagine_Task):
    def load_actors(self):
    # Create the shoe_box container
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
    
    # Add the relevant objects
    self.pot = self.add_actor("pot-with-plant", "pot-with-plant")
    self.shampoo = self.add_actor("shampoo", "shampoo")
    self.cup = self.add_actor("cup_without_handle", "cup_without_handle")
    self.drill = self.add_actor("drill", "drill")
    
    # Add distractors
    distractor_list = ['calculator', 'toycar', 'book', 'alarm-clock', 'red_block']
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Play Once (Define Robot Actions)**

The robot must perform the following sequence of actions:

1. **Incorrectly** place the `pot-with-plant` into the shoe_box (this is a mistake).
2. **Correct** the mistake by placing the `pot-with-plant` **on top** of the shoe_box.
3. Place `shampoo` and `cup_without_handle` **inside** the shoe_box.
4. Place `drill` **on top** of the shoe_box.

```python

    def play_once(self):
    # Step 1: Wrong action - place pot into shoe_box
    success = self.pick_and_place(self.pot, self.shoe_box)
    print("Wrong placement of pot:", success)
    if not success:
        return self.info

    # Step 2: Recovery - place pot on top of shoe_box
    success = self.pick_and_place(self.pot, self.shoe_box)
    print("Recovery placement of pot:", success)
    if not success:
        return self.info

    # Step 3: Place shampoo into shoe_box
    success = self.pick_and_place(self.shampoo, self.shoe_box)
    print("Shampoo placement:", success)
    if not success:
        return self.info

    # Step 4: Place cup into shoe_box
    success = self.pick_and_place(self.cup, self.shoe_box)
    print("Cup placement:", success)
    if not success:
        return self.info

    # Step 5: Place drill on top of shoe_box
    success = self.pick_and_place(self.drill, self.shoe_box)
    print("Drill placement:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **Step 3: Check Success**

We use the `check_on` API to verify that:

- `shampoo` and `cup_without_handle` are **inside** the shoe_box.
- `pot-with-plant` and `drill` are **on top** of the shoe_box.

Given the ambiguity in the API (whether `check_on` checks for being *on top* or *inside*), we assume that the API correctly differentiates between the two based on the object's properties and placement logic.

```python

    
