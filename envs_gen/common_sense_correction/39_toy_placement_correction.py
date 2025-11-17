from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 39_toy_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Add the toy items
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.toycar = self.add_actor("toycar", "toycar")
        # Add other objects
        self.book = self.add_actor("book", "book")
        self.mug = self.add_actor("mug", "mug")
        # Add distractors
        distractor_list = ['dumbbell', 'shoe', 'microphone', 'alarm-clock', 'pot-with-plant', 'screwdriver']
        self.add_distractors(distractor_list)
        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        # Place toy items into the wooden box
        success = self.pick_and_place(self.orange_block, self.wooden_box)
        print("Pick orange_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("Pick red_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Pick toycar:", success)
        if not success:
            return self.info

        # Wrong action: place mug into the wooden box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Wrong: Pick mug into box:", success)
        if not success:
            return self.info

        # Recovery: place mug back on the table
        success = self.pick_and_place(self.mug, self.table)
        print("Recovery: Pick mug back to table:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Verify all toy items are in the wooden box and mug is not
        if (
            self.check_on(self.orange_block, self.wooden_box) and
            self.check_on(self.red_block, self.wooden_box) and
            self.check_on(self.toycar, self.wooden_box) and
            not self.check_on(self.mug, self.wooden_box)
        ):
            return True
        return False
