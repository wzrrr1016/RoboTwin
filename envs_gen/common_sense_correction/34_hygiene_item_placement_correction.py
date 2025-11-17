from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 34_hygiene_item_placement_correction(Imagine_Task):
    def load_actors(self):
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")
    self.shampoo = self.add_actor("shampoo", "shampoo")
    self.tissue_box = self.add_actor("tissue-box", "tissue-box")
    self.bottle = self.add_actor("bottle", "bottle")
    self.mouse = self.add_actor("mouse", "mouse")
    distractor_list = ["calculator", "pet-collar", "table-tennis", "hammer", "shoe"]
    self.add_distractors(distractor_list)
    self.check_scene()
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of actions the robot arm should perform. The correct actions are to pick and place the `shampoo` and `tissue-box` into the `fluted_block`. The `bottle` is mistakenly placed into the `fluted_block` (wrong action), and then it is recovered by placing it back on the table.

Each action is followed by a success check. If any action fails, the task is terminated early.

```python

    def play_once(self):
    # Correct action: Place shampoo into fluted_block
    success = self.pick_and_place(self.shampoo, self.fluted_block)
    print("Pick shampoo:", success)
    if not success:
        return self.info

    # Correct action: Place tissue-box into fluted_block
    success = self.pick_and_place(self.tissue_box, self.fluted_block)
    print("Pick tissue-box:", success)
    if not success:
        return self.info

    # Wrong action: Place bottle into fluted_block
    success = self.pick_and_place(self.bottle, self.fluted_block)
    print("Pick bottle (wrong):", success)
    if not success:
        return self.info

    # Recovery action: Place bottle back on the table
    success = self.pick_and_place(self.bottle, self.table)
    print("Recover bottle:", success)
    if not success:
        return self.info

    self.add_end()
    return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the task was completed successfully. The success condition is that the `shampoo` and `tissue-box` are in the `fluted_block`, and the `bottle` is back on the table (i.e., not in the container).

We use the `check_on` method to verify the placement of each object.

```python

    
