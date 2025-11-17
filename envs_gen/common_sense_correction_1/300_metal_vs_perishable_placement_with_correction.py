from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 300_metal_vs_perishable_placement_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Creates the shoe_box container and all relevant objects.
        Adds distractor objects to the environment.
        """
        # Create the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create the metal objects to be placed inside the shoe_box
        self.can = self.add_actor("can", "can")
        self.hammer = self.add_actor("hammer", "hammer")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Create the perishable items to be placed on top of the shoe_box
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects to the environment
        distractor_list = ['book', 'pot-with-plant', 'markpen', 'red_block', 'table-tennis']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's task sequence:
        1. Place metal objects (can, stapler, hammer) into the shoe_box
        2. Place perishable items (apple, bread) on top of the shoe_box
        """
        # Place metal objects into the shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Pick and place can:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Pick and place stapler:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick and place hammer:", success)
        if not success:
            return self.info
            
        # Place perishable items on top of the shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Pick and place apple:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("Pick and place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - All metal objects are in the shoe_box
        - All perishable items are on the shoe_box
        """
        # Check if all metal objects are in the shoe_box
        metal_objects_in = (
            self.check_on(self.can, self.shoe_box) and
            self.check_on(self.stapler, self.shoe_box) and
            self.check_on(self.hammer, self.shoe_box)
        )
        
        # Check if all perishable items are on the shoe_box
        perishables_on = (
            self.check_on(self.apple, self.shoe_box) and
            self.check_on(self.bread, self.shoe_box)
        )
        
        # Return True only if all conditions are met
        return metal_objects_in and perishables_on
