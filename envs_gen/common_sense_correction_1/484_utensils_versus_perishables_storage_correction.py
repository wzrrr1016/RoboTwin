from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 484_utensils_versus_perishables_storage_correction(Imagine_Task):
    def load_actors(self):
	    # Load the container
	    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
	
	    # Load the main objects
	    self.cup = self.add_actor("cup", "cup")
	    self.fork = self.add_actor("fork", "fork")
	    self.french_fries = self.add_actor("french_fries", "french_fries")
	    self.tissue_box = self.add_actor("tissue-box", "tissue-box")
	    self.purple_block = self.add_actor("purple_block", "purple_block")
	
	    # Load distractors
	    distractor_list = ["calculator", "screwdriver", "hammer", "book", "alarm-clock"]
	    self.add_distractors(distractor_list)
	```
	
	---
	
	#### 2. `play_once`
	
	This function defines the sequence of actions the robot should perform:
	
	1. Place the **cup** into the `shoe_box`.
	2. Place the **fork** onto the `shoe_box` (wrong action).
	3. Pick the **fork** from the top of the `shoe_box` and place it into the `shoe_box` (recovery).
	4. Place **french_fries**, **tissue-box**, and **purple_block** on top of the `shoe_box`.
	
	```python

    def play_once(self):
	    # Step 1: Place cup into shoe_box
	    success = self.pick_and_place(self.cup, self.shoe_box)
	    if not success:
	        return self.info
	
	    # Step 2: Place fork onto shoe_box (wrong)
	    success = self.pick_and_place(self.fork, self.shoe_box)
	    if not success:
	        return self.info
	
	    # Step 3: Pick fork from top of shoe_box and place into shoe_box (recovery)
	    success = self.pick_and_place(self.fork, self.shoe_box)
	    if not success:
	        return self.info
	
	    # Step 4: Place french_fries on top of shoe_box
	    success = self.pick_and_place(self.french_fries, self.table)
	    if not success:
	        return self.info
	
	    # Step 5: Place tissue-box on top of shoe_box
	    success = self.pick_and_place(self.tissue_box, self.table)
	    if not success:
	        return self.info
	
	    # Step 6: Place purple_block on top of shoe_box
	    success = self.pick_and_place(self.purple_block, self.table)
	    if not success:
	        return self.info
	```
	
	> **Note:** We use `self.table` as the container to place objects **on top** of the `shoe_box`, assuming the `shoe_box` is a surface and not a container that can hold objects inside.
	
	---
	
	#### 3. `check_success`
	
	This function verifies that:
	
	- `cup` and `fork` are **inside** the `shoe_box` (i.e., not on top).
	- `french_fries`, `tissue-box`, and `purple_block` are **on top** of the `shoe_box`.
	
	```python

    
