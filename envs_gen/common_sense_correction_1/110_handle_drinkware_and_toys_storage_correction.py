from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 110_handle_drinkware_and_toys_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Add the required objects
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.mug = self.add_actor("mug", "mug")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.apple = self.add_actor("apple", "apple")
        # Add distractors
        distractor_list = ['calculator', 'alarm-clock', 'small-speaker', 'book', 'pet-collar']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place orange_block into wooden_box
        success = self.pick_and_place(self.orange_block, self.wooden_box)
        print("Place orange_block:", success)
        if not success:
            return self.info

        # Place pink_block into wooden_box
        success = self.pick_and_place(self.pink_block, self.wooden_box)
        print("Place pink_block:", success)
        if not success:
            return self.info

        # Wrongly place mug into wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Wrong place mug:", success)
        if not success:
            return self.info

        # Recovery: pick mug from wooden_box and place on wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Recover mug:", success)
        if not success:
            return self.info

        # Place screwdriver into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        # Place apple on wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check that mug and apple are on top of wooden_box
        mug_on = self.check_on(self.mug, self.wooden_box)
        apple_on = self.check_on(self.apple, self.wooden_box)

        # Check that orange_block, pink_block, and screwdriver are inside (not on top)
        orange_inside = not self.check_on(self.orange_block, self.wooden_box)
        pink_inside = not self.check_on(self.pink_block, self.wooden_box)
        screwdriver_inside = not self.check_on(self.screwdriver, self.wooden_box)

        return mug_on and apple_on and orange_inside and pink_inside and screwdriver_inside
