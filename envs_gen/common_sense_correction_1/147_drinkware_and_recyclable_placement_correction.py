from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 147_drinkware_and_recyclable_placement_correction(Imagine_Task):
    def load_actors(self):
    # Add the tray (container)
    self.tray = self.add_actor("tray", "tray")
    
    # Add objects used for drinking and recyclable metal
    self.cup = self.add_actor("cup", "cup")
    self.can = self.add_actor("can", "can")
    self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
    self.tissue_box = self.add_actor("tissue-box", "tissue-box")
    
    # Add distractors
    distractor_list = ["calculator", "toycar", "shoe", "book", "hammer"]
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Define Robot Actions in `play_once`**

The robot will:

1. **Incorrectly** place the tissue-box into the tray.
2. **Recover** by placing the tissue-box back on the table.
3. **Correctly** place the cup, can, and cup_without_handle into the tray.

Each action is followed by a success check. If any step fails, the function returns early.

```python

    def play_once(self):
    # Wrong action: place tissue-box into tray
    success = self.pick_and_place(self.tissue_box, self.tray)
    print("Wrong placement of tissue-box:", success)
    if not success:
        return self.info

    # Recovery: place tissue-box back on the table
    success = self.pick_and_place(self.tissue_box, self.table)
    print("Recovery of tissue-box:", success)
    if not success:
        return self.info

    # Correct actions
    success = self.pick_and_place(self.cup, self.tray)
    print("Place cup:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.can, self.tray)
    print("Place can:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.cup_without_handle, self.tray)
    print("Place cup_without_handle:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **Step 3: Check Task Success in `check_success`**

We verify that:

- The **cup**, **can**, and **cup_without_handle** are on the tray.
- The **tissue-box** is **not** on the tray (i.e., it was successfully recovered).

```python

    
