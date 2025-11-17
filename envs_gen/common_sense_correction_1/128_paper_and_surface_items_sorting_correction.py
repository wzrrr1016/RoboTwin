from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 128_paper_and_surface_items_sorting_correction(Imagine_Task):
    def load_actors(self):
    # Add containers
    self.dustbin = self.add_actor("dustbin", "dustbin")
    self.coaster = self.add_actor("coaster", "coaster")

    # Add objects
    self.book = self.add_actor("book", "book")
    self.tissue_box = self.add_actor("tissue-box", "tissue-box")
    self.bottle = self.add_actor("bottle", "bottle")
    self.small_speaker = self.add_actor("small-speaker", "small-speaker")

    # Add distractors
    distractor_list = ["shoe", "dumbbell", "hammer", "baguette", "toycar"]
    self.add_distractors(distractor_list)
```

---

### ✅ `play_once`

This function defines the sequence of actions the robot should perform. It includes:

1. **Wrong action**: Place the `book` on the `coaster`.
2. **Recovery action**: Pick the `book` from the `coaster` and place it into the `dustbin`.
3. **Correct actions**:
   - Place the `tissue-box` into the `dustbin`.
   - Place the `bottle` and `small-speaker` onto the `coaster`.

Each action is followed by a success check. If any step fails, the function returns early.

```python

    def play_once(self):
    # Wrong action: place book on coaster
    success = self.pick_and_place(self.book, self.coaster)
    print("Place book on coaster (wrong):", success)
    if not success:
        return self.info

    # Recovery: pick book from coaster and place into dustbin
    success = self.pick_and_place(self.book, self.dustbin)
    print("Recover book to dustbin:", success)
    if not success:
        return self.info

    # Correct actions
    success = self.pick_and_place(self.tissue_box, self.dustbin)
    print("Place tissue-box into dustbin:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.bottle, self.coaster)
    print("Place bottle onto coaster:", success)
    if not success:
        return self.info

    success = self.pick_and_place(self.small_speaker, self.coaster)
    print("Place small-speaker onto coaster:", success)
    if not success:
        return self.info

    return self.info
```

---

### ✅ `check_success`

This function verifies whether all the objects are in the correct final positions. It uses the `check_on` method to confirm that:

- `book` and `tissue-box` are in the `dustbin`
- `bottle` and `small-speaker` are on the `coaster`

```python

    
