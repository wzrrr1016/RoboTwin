from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 2_serveable_items_and_personal_care_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers and objects to the environment
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.mug = self.add_actor("mug", "mug")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractor objects
        distractor_list = ["calculator", "toycar", "shoe", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong action: place shampoo on tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Place shampoo on tray (wrong):", success)
        if not success:
            return self.info

        # Recovery action: move shampoo to dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Place shampoo into dustbin (recovery):", success)
        if not success:
            return self.info

        # Place utensils and drinkware on tray
        success = self.pick_and_place(self.mug, self.tray)
        print("Place mug on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.fork, self.tray)
        print("Place fork on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.knife, self.tray)
        print("Place knife on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all objects are in their correct locations
        if (self.check_on(self.mug, self.tray) and
            self.check_on(self.fork, self.tray) and
            self.check_on(self.knife, self.tray) and
            self.check_on(self.shampoo, self.dustbin)):
            return True
        return False
```
