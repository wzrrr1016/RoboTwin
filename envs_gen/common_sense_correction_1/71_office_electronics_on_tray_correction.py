from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 71_office_electronics_on_tray_correction(Imagine_Task):
    def load_actors(self):
    self.tray = self.add_actor("tray", "tray")
    self.stapler = self.add_actor("stapler", "stapler")
    self.small_speaker = self.add_actor("small-speaker", "small-speaker")
    self.bottle = self.add_actor("bottle", "bottle")
    self.scanner = self.add_actor("scanner", "scanner")
    distractor_list = ["shoe", "dumbbell", "pot-with-plant", "apple", "red_block"]
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Play Once**

The robot must perform the following actions in sequence:

1. Pick and place the **stapler** on the **tray**.
2. Pick and place the **small-speaker** on the **tray**.
3. **Wrongly** pick and place the **bottle** on the **tray**.
4. **Recover** by picking the **bottle** from the **tray** and placing it on the **table**.
5. Pick and place the **scanner** on the **tray**.

We use the `pick_and_place` API for each action. If any step fails, the function returns early to avoid unnecessary actions.

```python

    def play_once(self):
    # Step 1: Place stapler on tray
    success = self.pick_and_place(self.stapler, self.tray)
    print("pick place stapler:", success)
    if not success:
        return self.info

    # Step 2: Place small-speaker on tray
    success = self.pick_and_place(self.small_speaker, self.tray)
    print("pick place small-speaker:", success)
    if not success:
        return self.info

    # Step 3: Wrongly place bottle on tray
    success = self.pick_and_place(self.bottle, self.tray)
    print("pick place bottle (wrong):", success)

    # Step 4: Recover by placing bottle on table
    success = self.pick_and_place(self.bottle, self.table)
    print("pick place bottle (recovery):", success)
    if not success:
        return self.info

    # Step 5: Place scanner on tray
    success = self.pick_and_place(self.scanner, self.tray)
    print("pick place scanner:", success)
    if not success:
        return self.info
```

---

### ✅ **Step 3: Check Success**

The success condition is that the **stapler**, **small-speaker**, and **scanner** are on the **tray**, and the **bottle** is **not** on the **tray**. We use the `check_on` API to verify the positions of the objects.

```python

    
