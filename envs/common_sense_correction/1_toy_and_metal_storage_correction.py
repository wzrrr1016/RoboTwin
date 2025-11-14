from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class toy_and_metal_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.green_block = self.add_actor("green_block", "green_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.can = self.add_actor("can", "can")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractors
        distractor_list = ["pet-collar", "sand-clock", "markpen"]
        self.add_distractors(distractor_list)

        self.check_scene()

    def play_once(self):
        # Place small lightweight toys (blocks) on plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("Place green_block on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.pink_block, self.plate)
        print("Place pink_block on plate:", success)
        if not success:
            return self.info

        # Wrong placement of can on plate (needs recovery)
        success = self.pick_and_place(self.can, self.plate)
        print("Place can on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: Move can to shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Move can to shoe_box:", success)
        if not success:
            return self.info

        # Place heavy item (dumbbell) in shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Place dumbbell in shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all placement conditions
        return (
            self.check_on(self.green_block, self.plate) and
            self.check_on(self.pink_block, self.plate) and
            self.check_on(self.can, self.shoe_box) and
            self.check_on(self.dumbbell, self.shoe_box)
        )
