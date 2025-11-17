from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 163_store_liquids_and_accessible_items_correction(Imagine_Task):
    def load_actors(self):
	    # Add containers
	    self.tray = self.add_actor("tray", "tray")
	    self.wooden_box = self.add_actor("wooden_box", "wooden_box")
	
	    # Add objects
	    self.shampoo = self.add_actor("shampoo", "shampoo")
	    self.bottle = self.add_actor("bottle", "bottle")
	    self.toycar = self.add_actor("toycar", "toycar")
	    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
	
	    # Add distractors
	    distractor_list = ['calculator', 'alarm-clock', 'shoe', 'book', 'small-speaker']
	    self.add_distractors(distractor_list)
	```
	
	---
	
	### ✅ **2. `play_once` Function**
	
	This function defines the sequence of actions the robot should perform. It includes a "wrong" action followed by a "recovery" action, as described in the task. The robot first places the `screwdriver` into the `wooden_box` (incorrect), then recovers by placing it onto the `tray`. It then places the `toycar` on the `tray`, and both the `shampoo` and `bottle` into the `wooden_box`.
	
	```python

    def play_once(self):
	    # Step 1: Pick screwdriver and place into wooden_box (wrong)
	    success = self.pick_and_place(self.screwdriver, self.wooden_box)
	    print("pick place screwdriver into wooden_box:", success)
	    if not success:
	        return self.info
	
	    # Step 2: Pick screwdriver from wooden_box and place onto tray (recovery)
	    success = self.pick_and_place(self.screwdriver, self.tray)
	    print("pick place screwdriver into tray:", success)
	    if not success:
	        return self.info
	
	    # Step 3: Pick toycar and place onto tray
	    success = self.pick_and_place(self.toycar, self.tray)
	    print("pick place toycar:", success)
	    if not success:
	        return self.info
	
	    # Step 4: Pick shampoo and place into wooden_box
	    success = self.pick_and_place(self.shampoo, self.wooden_box)
	    print("pick place shampoo:", success)
	    if not success:
	        return self.info
	
	    # Step 5: Pick bottle and place into wooden_box
	    success = self.pick_and_place(self.bottle, self.wooden_box)
	    print("pick place bottle:", success)
	    if not success:
	        return self.info
	
	    return self.info
	```
	
	---
	
	### ✅ **3. `check_success` Function**
	
	This function verifies that the final state of the environment matches the task requirements. It checks that the `shampoo` and `bottle` are in the `wooden_box`, and the `toycar` and `screwdriver` are on the `tray`.
	
	```python

    
