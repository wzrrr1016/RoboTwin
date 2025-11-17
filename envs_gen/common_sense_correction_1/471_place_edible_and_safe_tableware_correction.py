from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 471_place_edible_and_safe_tableware_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        self.plate = self.add_actor("plate", "plate")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.cup = self.add_actor("cup", "cup")
        
        # Add distractor objects to the environment
        distractor_list = ['calculator', 'pet-collar', 'toycar', 'pot-with-plant', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Place edible item (hamburg) on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Pick hamburg:", success)
        if not success:
            return self.info

        # Place safe utensil (fork) on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick fork:", success)
        if not success:
            return self.info

        # Wrong action: place unsafe utensil (knife) on plate
        success = self.pick_and_place(self.knife, self.plate)
        print("Pick knife (wrong):", success)
        if not success:
            return self.info

        # Recovery: move knife back to table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife:", success)
        if not success:
            return self.info

        # Place additional edible item (cup) on plate
        success = self.pick_and_place(self.cup, self.plate)
        print("Pick cup:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all required items are on the plate
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)
        fork_on_plate = self.check_on(self.fork, self.plate)
        cup_on_plate = self.check_on(self.cup, self.plate)
        
        # Check if the unsafe item (knife) is NOT on the plate
        knife_not_on_plate = not self.check_on(self.knife, self.plate)
        
        # Return True only if all conditions are met
        return hamburg_on_plate and fork_on_plate and cup_on_plate and knife_not_on_plate
