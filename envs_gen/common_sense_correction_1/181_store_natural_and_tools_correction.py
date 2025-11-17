from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 181_store_natural_and_tools_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")

    # Add objects
    self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
    self.apple = self.add_actor("apple", "apple")
    self.hammer = self.add_actor("hammer", "hammer")
    self.small_speaker = self.add_actor("small-speaker", "small-speaker")

    # Add distractors
    distractor_list = ["book", "shoe", "red_block", "blue_block", "toycar"]
    self.add_distractors(distractor_list)
```

---

### ✅ **2. `play_once` Function**

This function defines the sequence of robotic actions. It includes:

- A **wrong action** (placing `pot-with-plant` on `fluted_block`)
- A **recovery action** (moving `pot-with-plant` to `wooden_box`)
- Correct placements of `apple`, `hammer`, and `small-speaker` into their respective containers.

```python

    def play_once(self):
    # Wrong action: place pot-with-plant on fluted_block
    success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
    print("Wrong placement of pot-with-plant:", success)
    if not success:
        return self.info

    # Recovery: move pot-with-plant to wooden_box
    success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
    print("Recovery of pot-with-plant:", success)
    if not success:
        return self.info

    # Place apple into wooden_box
    success = self.pick_and_place(self.apple, self.wooden_box)
    print("Place apple:", success)
    if not success:
        return self.info

    # Place hammer on fluted_block
    success = self.pick_and_place(self.hammer, self.fluted_block)
    print("Place hammer:", success)
    if not success:
        return self.info

    # Place small-speaker on fluted_block
    success = self.pick_and_place(self.small_speaker, self.fluted_block)
    print("Place small-speaker:", success)
    if not success:
        return self.info
```

---

### ✅ **3. `check_success` Function**

This function verifies whether the final arrangement meets the task requirements:

- `pot-with-plant` and `apple` are in `wooden_box` (perishable/living items)
- `hammer` and `small-speaker` are in `fluted_block` (tools and electronics)

```python

    
