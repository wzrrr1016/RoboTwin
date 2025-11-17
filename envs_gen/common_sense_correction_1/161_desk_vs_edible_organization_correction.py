from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 161_desk_vs_edible_organization_correction(Imagine_Task):
    def load_actors(self):
    self.coaster = self.add_actor("coaster", "coaster")
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")
    self.bottle = self.add_actor("bottle", "bottle")
    self.apple = self.add_actor("apple", "apple")
    self.markpen = self.add_actor("markpen", "markpen")
    self.book = self.add_actor("book", "book")
    distractor_list = ["shoe", "dumbbell", "toycar", "pot-with-plant", "alarm-clock"]
    self.add_distractors(distractor_list)
```

---

### ✅ **Step 2: Play Once (Robot Actions)**

The robot must perform the following sequence of actions:

1. **Wrong Action**: Place the book on the coaster.
2. **Recovery Action**: Pick the book from the coaster and place it on the fluted_block.
3. **Correct Actions**:
   - Place the bottle on the coaster.
   - Place the apple on the coaster.
   - Place the markpen on the fluted_block.

Each action is followed by a success check. If any step fails, the function returns early.

```python

    def play_once(self):
    # Wrong action: book on coaster
    success = self.pick_and_place(self.book, self.coaster)
    print("Wrong action: book on coaster:", success)
    if not success:
        return self.info

    # Recovery action: book on fluted_block
    success = self.pick_and_place(self.book, self.fluted_block)
    print("Recovery action: book on fluted_block:", success)
    if not success:
        return self.info

    # Correct actions
    success = self.pick_and_place(self.bottle, self.coaster)
    print("Bottle on coaster:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.apple, self.coaster)
    print("Apple on coaster:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.markpen, self.fluted_block)
    print("Markpen on fluted_block:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ **Step 3: Check Success**

The success condition is met if:

- `bottle` and `apple` are on the `coaster`
- `markpen` and `book` are on the `fluted_block`

```python

    
