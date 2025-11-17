from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 122_toy_and_utensil_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.plate = self.add_actor("plate", "plate")
        
        # Add relevant objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ["calculator", "pot-with-plant", "book", "alarm-clock", "hammer"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place red block in shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Red block placed:", success)
        if not success:
            return self.info

        # Place fork in shoe_box (wrong action)
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("Fork placed in shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: Move fork to plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Fork moved to plate:", success)
        if not success:
            return self.info

        # Place green block in shoe_box
        success = self.pick_and_place(self.green_block, self.shoe_box)
        print("Green block placed:", success)
        if not success:
            return self.info

        # Place pink block in shoe_box
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Pink block placed:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all blocks are in shoe_box and fork is on plate
        blocks_in_shoe_box = (
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.green_block, self.shoe_box) and
            self.check_on(self.pink_block, self.shoe_box)
        )
        fork_on_plate = self.check_on(self.fork, self.plate)
        return blocks_in_shoe_box and fork_on_plate
