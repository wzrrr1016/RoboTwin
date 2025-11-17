from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 374_drinkware_and_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")

        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup = self.add_actor("cup", "cup")
        self.apple = self.add_actor("apple", "apple")
        self.fork = self.add_actor("fork", "fork")

        # Add distractors
        distractor_list = ["calculator", "toycar", "alarm-clock", "dumbbell", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place drinkware on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        # Wrong placement of apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Wrongly place apple on coaster:", success)
        if not success:
            return self.info

        # Recovery: move apple to plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Move apple to plate:", success)
        if not success:
            return self.info

        # Place eating utensil on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Place fork on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if both cups are on the coaster
        cup1_on = self.check_on(self.cup_with_handle, self.coaster)
        cup2_on = self.check_on(self.cup, self.coaster)

        # Check if apple and fork are on the plate
        apple_on = self.check_on(self.apple, self.plate)
        fork_on = self.check_on(self.fork, self.plate)

        return cup1_on and cup2_on and apple_on and fork_on
