from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 257_drinkware_and_perishables_tray_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers and objects
        self.tray = self.add_actor("tray", "tray")
        self.mug = self.add_actor("mug", "mug")
        self.bottle = self.add_actor("bottle", "bottle")
        self.apple = self.add_actor("apple", "apple")
        self.book = self.add_actor("book", "book")
        
        # Add distractor objects from the scene description
        distractor_list = ['calculator', 'screwdriver', 'hammer', 'shoe', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Execute the sequence of actions defined in the task
        success = self.pick_and_place(self.mug, self.tray)
        print("Pick mug:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.book, self.tray)
        print("Pick book (wrong):", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.book, self.table)
        print("Recover book:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick bottle:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify that all required items are on the tray
        return (self.check_on(self.mug, self.tray) and 
                self.check_on(self.bottle, self.tray) and 
                self.check_on(self.apple, self.tray))
```
