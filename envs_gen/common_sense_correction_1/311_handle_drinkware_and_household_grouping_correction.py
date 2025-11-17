from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 311_handle_drinkware_and_household_grouping_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: plate and coaster
        - Objects: cup_with_handle, mug, tissue-box, sand-clock, knife
        - Distractors: calculator, battery, small-speaker, scanner, mouse
        """
        # Create containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Create objects to be manipulated
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractor objects to the environment
        distractor_list = ['calculator', 'battery', 'small-speaker', 'scanner', 'mouse']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task:
        1. Place drinkware with handles (cup_with_handle, mug) on the coaster
        2. Place non-drinkware household items (tissue-box, sand-clock, knife) on the plate
        """
        # Place drinkware with handles on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug on coaster:", success)
        if not success:
            return self.info
            
        # Place non-drinkware household items on plate
        success = self.pick_and_place(self.tissue_box, self.plate)
        print("Place tissue-box on plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.sand_clock, self.plate)
        print("Place sand-clock on plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife on plate:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in their correct target containers:
        - cup_with_handle and mug should be on the coaster
        - tissue-box, sand-clock, and knife should be on the plate
        """
        return (
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.mug, self.coaster) and
            self.check_on(self.tissue_box, self.plate) and
            self.check_on(self.sand_clock, self.plate) and
            self.check_on(self.knife, self.plate)
        )
