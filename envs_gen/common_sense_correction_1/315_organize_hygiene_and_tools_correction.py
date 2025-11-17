from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 315_organize_hygiene_and_tools_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the simulation environment"""
        # Create the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.markpen = self.add_actor("markpen", "markpen")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractor objects
        self.add_distractors(["toycar", "shoe", "book", "alarm-clock", "pot-with-plant", "dumbbell"])

    def play_once(self):
        """Execute the sequence of robotic actions for the task"""
        # Place personal-care item (shampoo) into organizer
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Place shampoo:", success)
        if not success:
            return self.info
            
        # Place disposable cleaning item (tissue box) into organizer
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue box:", success)
        if not success:
            return self.info
            
        # Initial wrong placement of writing instrument (markpen) into organizer
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Wrong placement of markpen:", success)
        if not success:
            return self.info
            
        # Recovery: Move markpen to organizer's surface
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Recovery placement of markpen:", success)
        if not success:
            return self.info
            
        # Place tool (screwdriver) on organizer's surface
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if all task requirements are successfully completed"""
        # Check if personal-care and cleaning items are in the organizer
        # and if tools and writing instruments are on the organizer's surface
        return (
            self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.tissue_box, self.fluted_block) and
            self.check_on(self.markpen, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block)
        )
