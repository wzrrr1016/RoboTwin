from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 166_coaster_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the four drinkware objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup = self.add_actor("cup", "cup")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        
        # Add distractors from the task description
        distractor_list = ['calculator', 'pet-collar', 'toycar', 'book', 'battery']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: place bottle on coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Wrong placement of bottle:", success)
        
        # Recovery: place bottle on table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recovery of bottle:", success)
        if not success:
            return self.info

        # Correct action: place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Correct action: place cup on coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup:", success)
        if not success:
            return self.info

        # Correct action: place cup_without_handle on table
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("Place cup_without_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the correct items are on the coaster and others are on the table
        if (self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.cup_without_handle, self.table) and
            self.check_on(self.bottle, self.table)):
            return True
        return False
