from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class food_container_organization_correction_38(Imagine_Task):
    def load_actors(self):
    # Load containers
    self.fluted_block = self.add_actor("fluted_block", "fluted_block")
    self.coaster = self.add_actor("coaster", "coaster")
    
    # Load objects
    self.bread = self.add_actor("bread", "bread")
    self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
    self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
    self.hamburg = self.add_actor("hamburg", "hamburg")
    self.fork = self.add_actor("fork", "fork")
```

---

### ✅ **Step 2: Play Once (Action Sequence)**

The robot must perform the following steps:

1. **Pick bread** and place it into the **coaster** (wrong action).
2. **Pick bread** from the **coaster** and place it into the **fluted_block** (correct action).
3. **Pick cup_without_handle** and place it into the **coaster**.
4. **Pick cup_with_handle** and place it into the **coaster**.
5. **Pick hamburg** and place it into the **fluted_block**.
6. **Pick fork** and place it into the **coaster**.

Each step is executed using the `pick_and_place` API, and the robot will return early if any step fails.

```python

    def play_once(self):
    # Step 1: Place bread into coaster (wrong)
    success = self.pick_and_place(self.bread, self.coaster)
    print("pick place bread into coaster:", success)
    if not success:
        return self.info

    # Step 2: Pick bread from coaster and place into fluted_block
    success = self.pick_and_place(self.bread, self.fluted_block)
    print("pick place bread into fluted_block:", success)
    if not success:
        return self.info

    # Step 3: Place cup_without_handle into coaster
    success = self.pick_and_place(self.cup_without_handle, self.coaster)
    print("pick place cup_without_handle into coaster:", success)
    if not success:
        return self.info

    # Step 4: Place cup_with_handle into coaster
    success = self.pick_and_place(self.cup_with_handle, self.coaster)
    print("pick place cup_with_handle into coaster:", success)
    if not success:
        return self.info

    # Step 5: Place hamburg into fluted_block
    success = self.pick_and_place(self.hamburg, self.fluted_block)
    print("pick place hamburg into fluted_block:", success)
    if not success:
        return self.info

    # Step 6: Place fork into coaster
    success = self.pick_and_place(self.fork, self.coaster)
    print("pick place fork into coaster:", success)
    if not success:
        return self.info
```

---

### ✅ **Step 3: Check Success**

Finally, we verify that all objects are in the correct containers using the `check_on` API.

```python

    
