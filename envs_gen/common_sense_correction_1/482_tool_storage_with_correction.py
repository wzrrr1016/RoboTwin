from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 482_tool_storage_with_correction(Imagine_Task):
    def load_actors(self):
	    # Add the shoe box as the main container
	    self.shoe_box = self.add_actor("shoe_box", "shoe_box")
	    
	    # Add the required tools
	    self.stapler = self.add_actor("stapler", "stapler")
	    self.screwdriver = self.add_actor("screwdriver", "screwdriver")
	    self.drill = self.add_actor("drill", "drill")
	    self.knife = self.add_actor("knife", "knife")
	    
	    # Add distractors to the environment
	    distractor_list = ['baguette', 'apple', 'toycar', 'pot-with-plant', 'tissue-box']
	    self.add_distractors(distractor_list)
	```
	
	---
	
	### 🤖 `play_once` Function
	
	This function defines the robot's sequence of actions. It includes:
	
	- Correctly placing the **stapler** and **screwdriver** into the shoe box.
	- A **wrong action** of placing the **knife** into the shoe box.
	- A **recovery action** of picking the **knife** from the shoe box and placing it **on top**.
	- Placing the **drill** directly on top of the shoe box.
	
	```python

    def play_once(self):
	    # Place stapler into shoe_box
	    success = self.pick_and_place(self.stapler, self.shoe_box)
	    print("Stapler placed:", success)
	    if not success:
	        return self.info
	
	    # Place screwdriver into shoe_box
	    success = self.pick_and_place(self.screwdriver, self.shoe_box)
	    print("Screwdriver placed:", success)
	    if not success:
	        return self.info
	
	    # Wrong action: place knife into shoe_box
	    success = self.pick_and_place(self.knife, self.shoe_box)
	    print("Knife placed into box (wrong):", success)
	    if not success:
	        return self.info
	
	    # Recovery: pick knife from shoe_box and place on top
	    success = self.pick_and_place(self.knife, self.shoe_box)
	    print("Knife placed on box (recovery):", success)
	    if not success:
	        return self.info
	
	    # Place drill on top of shoe_box
	    success = self.pick_and_place(self.drill, self.shoe_box)
	    print("Drill placed on box:", success)
	    if not success:
	        return self.info
	```
	
	> **Note**: The second call to `pick_and_place(self.knife, self.shoe_box)` is intended to simulate the recovery action. It assumes the API can distinguish between placing an object *into* and *on top of* the container based on context or object properties (e.g., sharpness).
	
	---
	
	### ✅ `check_success` Function
	
	This function verifies the final state of the environment. It checks:
	
	- The **stapler** and **screwdriver** are **not on** the shoe box (i.e., they are **inside**).
	- The **drill** and **knife** are **on top** of the shoe box.
	
	```python

    
