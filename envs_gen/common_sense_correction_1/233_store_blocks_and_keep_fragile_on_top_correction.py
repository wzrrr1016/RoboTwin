from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 233_store_blocks_and_keep_fragile_on_top_correction(Imagine_Task):
    def load_actors(self):
	    # Add the shoe_box as a container
	    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
	    
	    # Add the solid toy blocks
	    self.green_block = self.add_actor("green_block", "green_block")
	    self.red_block = self.add_actor("red_block", "red_block")
	    
	    # Add fragile and electronic items
	    self.cup = self.add_actor("cup", "cup")
	    self.mouse = self.add_actor("mouse", "mouse")
	    
	    # Add distractors
	    distractor_list = ["apple", "baguette", "book", "dumbbell", "tissue-box"]
	    self.add_distractors(distractor_list)
	```
	
	---
	
	### ✅ **2. `play_once` Function**
	
	This function defines the sequence of actions the robot should perform:
	
	1. Place the green and red blocks into the shoe_box.
	2. Place the cup into the shoe_box (wrong action).
	3. Recover by placing the cup on top of the shoe_box.
	4. Place the mouse on top of the shoe_box.
	
	```python

    def play_once(self):
	    # Place green block into shoe_box
	    success = self.pick_and_place(self.green_block, self.shoe_box)
	    print("Place green_block:", success)
	    if not success:
	        return self.info
	
	    # Place red block into shoe_box
	    success = self.pick_and_place(self.red_block, self.shoe_box)
	    print("Place red_block:", success)
	    if not success:
	        return self.info
	
	    # Wrong action: place cup into shoe_box
	    success = self.pick_and_place(self.cup, self.shoe_box)
	    print("Wrong place cup:", success)
	    if not success:
	        return self.info
	
	    # Recovery: place cup on top of shoe_box
	    success = self.pick_and_place(self.cup, self.shoe_box)
	    print("Recover cup:", success)
	    if not success:
	        return self.info
	
	    # Place mouse on top of shoe_box
	    success = self.pick_and_place(self.mouse, self.shoe_box)
	    print("Place mouse:", success)
	    if not success:
	        return self.info
	
	    return self.info
	```
	
	---
	
	### ✅ **3. `check_success` Function**
	
	This function verifies that the task was completed correctly:
	
	- Solid blocks are **not on** the shoe_box (assumed to be inside).
	- Fragile (cup) and electronic (mouse) items are **on** the shoe_box.
	
	```python

    
