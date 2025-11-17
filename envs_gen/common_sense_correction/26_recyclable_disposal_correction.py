from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 26_recyclable_disposal_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add the objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box_0")
        self.can = self.add_actor("can", "can_0")
        self.shampoo = self.add_actor("shampoo", "shampoo_0")
        self.hammer = self.add_actor("hammer", "hammer_0")
        # Add distractors
        distractor_list = ['fluted_block', 'red_block', 'green_block', 'blue_block', 'purple_block']
        self.add_distractors(distractor_list)
        # Check scene setup
        self.check_scene()

    def play_once(self):
        # Place recyclables into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Tissue-box placed:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.dustbin)
        print("Can placed:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Shampoo placed:", success)
        if not success:
            return self.info

        # Wrongly place hammer into dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("Hammer (wrong) placed:", success)
        if not success:
            return self.info

        # Recovery: place hammer on table
        success = self.pick_and_place(self.hammer, self.table)
        print("Hammer (recovery) placed:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        return (
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.shampoo, self.dustbin) and
            self.check_on(self.hammer, self.table)
        )
