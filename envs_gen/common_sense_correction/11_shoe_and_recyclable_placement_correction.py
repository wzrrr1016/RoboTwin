from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 11_shoe_and_recyclable_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.shoe = self.add_actor("shoe", "shoe")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors
        distractor_list = ['pet-collar', 'table-tennis', 'toycar', 'pot-with-plant', 'alarm-clock', 'red_block']
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Step 1: Put shoe into shoe_box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Put shoe into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Put hammer into dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("Put hammer into dustbin:", success)
        if not success:
            return self.info

        # Step 3: Wrong placement of cup_with_handle into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Put cup_with_handle into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery - move cup_with_handle to dustbin
        success = self.pick_and_place(self.cup_with_handle, self.dustbin)
        print("Put cup_with_handle into dustbin (recovery):", success)
        if not success:
            return self.info

        # Step 5: Put bottle into dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Put bottle into dustbin:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.shoe, self.shoe_box) and
            self.check_on(self.hammer, self.dustbin) and
            self.check_on(self.cup_with_handle, self.dustbin) and
            self.check_on(self.bottle, self.dustbin)):
            return True
        return False
