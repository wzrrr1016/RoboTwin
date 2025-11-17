from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 426_place_edibles_utensils_and_sharp_tool_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create objects to be manipulated
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "shoe", "pot-with-plant", "book", "alarm-clock", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place edible foods and utensils into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french fries:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Place fork:", success)
        if not success:
            return self.info
            
        # Wrongly place knife into fluted_block (initial incorrect action)
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Place knife (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: move knife to purple_block
        success = self.pick_and_place(self.knife, self.purple_block)
        print("Place knife on purple block:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all objects are in their correct locations
        return (
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block) and
            self.check_on(self.knife, self.purple_block)
        )
