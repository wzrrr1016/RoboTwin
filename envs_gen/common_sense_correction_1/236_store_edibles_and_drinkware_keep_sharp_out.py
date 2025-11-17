from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 236_store_edibles_and_drinkware_keep_sharp_out(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        # Add the objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.mug = self.add_actor("mug", "mug")
        self.knife = self.add_actor("knife", "knife")
        # Add distractors
        distractors = ["calculator", "pet-collar", "alarm-clock", "toycar", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        # Step 1: Pick apple and place into shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Pick apple:", success)
        if not success:
            return self.info

        # Step 2: Pick knife and place into shoe_box (wrong action)
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Pick knife (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick knife from shoe_box and place on the table (recovery)
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife:", success)
        if not success:
            return self.info

        # Step 4: Pick mug and place into shoe_box
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Pick mug:", success)
        if not success:
            return self.info

        # Step 5: Pick hamburg and place into shoe_box
        success = self.pick_and_place(self.hamburg, self.shoe_box)
        print("Pick hamburg:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all edible and drinkware items are in the shoe_box
        apple_on = self.check_on(self.apple, self.shoe_box)
        hamburg_on = self.check_on(self.hamburg, self.shoe_box)
        mug_on = self.check_on(self.mug, self.shoe_box)
        # Check if knife is NOT in the shoe_box
        knife_not_in = not self.check_on(self.knife, self.shoe_box)
        return apple_on and hamburg_on and mug_on and knife_not_in
