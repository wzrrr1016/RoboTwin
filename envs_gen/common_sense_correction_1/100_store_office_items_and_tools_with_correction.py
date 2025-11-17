from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 100_store_office_items_and_tools_with_correction(Imagine_Task):
    def load_actors(self):
    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
    self.book = self.add_actor("book", "book")
    self.stapler = self.add_actor("stapler", "stapler")
    self.bottle = self.add_actor("bottle", "bottle")
    self.hammer = self.add_actor("hammer", "hammer")
    distractor_list = ['apple', 'baguette', 'battery', 'pet-collar', 'table-tennis']
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Play Once**

The `play_once` function defines the sequence of actions the robot should perform. It includes:

1. **Place the book and stapler into the shoe_box**.
2. **Incorrectly place the bottle into the shoe_box**.
3. **Recover by picking the bottle from the shoe_box and placing it on top**.
4. **Place the hammer on top of the shoe_box**.

Each action is executed using the `pick_and_place` API, and the function returns early if any step fails.

```python

    def play_once(self):
    # Place book into shoe_box
    success = self.pick_and_place(self.book, self.shoe_box)
    print("Place book:", success)
    if not success:
        return self.info

    # Place stapler into shoe_box
    success = self.pick_and_place(self.stapler, self.shoe_box)
    print("Place stapler:", success)
    if not success:
        return self.info

    # Wrongly place bottle into shoe_box
    success = self.pick_and_place(self.bottle, self.shoe_box)
    print("Place bottle (wrong):", success)
    if not success:
        return self.info

    # Recovery: pick bottle from shoe_box and place on top of it
    success = self.pick_and_place(self.bottle, self.shoe_box)
    print("Recover bottle:", success)
    if not success:
        return self.info

    # Place hammer on top of shoe_box
    success = self.pick_and_place(self.hammer, self.shoe_box)
    print("Place hammer:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **Step 3: Check Success**

The `check_success` function verifies that all required objects are in the correct positions. Since the API only provides `check_on`, we assume that placing an object into the shoe_box (via `pick_and_place`) results in it being "on" the container. This includes both **inside** and **on top** of the container.

We check that:

- `book` and `stapler` are in the shoe_box (inside or on top).
- `bottle` and `hammer` are on top of the shoe_box.

```python

    
