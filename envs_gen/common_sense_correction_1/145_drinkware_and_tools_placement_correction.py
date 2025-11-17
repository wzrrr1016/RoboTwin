from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 145_drinkware_and_tools_placement_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add objects to be manipulated
        self.cup = self.add_actor("cup", "cup")
        self.can = self.add_actor("can", "can")
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractor objects
        distractor_list = ["calculator", "toycar", "book", "shoe", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions"""
        # Initial incorrect placement (drill on coaster) and recovery
        success = self.pick_and_place(self.drill, self.coaster)
        print("Place drill on coaster (wrong):", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Move drill to wooden_box (recovery):", success)
        if not success:
            return self.info

        # Place drinkware on coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        # Place tools and heavy items in wooden box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver in wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Place dumbbell in wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if all objects are in their correct final positions"""
        return (self.check_on(self.cup, self.coaster) and
                self.check_on(self.can, self.coaster) and
                self.check_on(self.drill, self.wooden_box) and
                self.check_on(self.screwdriver, self.wooden_box) and
                self.check_on(self.dumbbell, self.wooden_box))
