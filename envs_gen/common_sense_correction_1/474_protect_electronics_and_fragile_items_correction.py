from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 474_protect_electronics_and_fragile_items_correction(Imagine_Task):
    def load_actors(self):
        # Add the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        # Add the target objects
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.sand_clock = self.add_actor("sand-clock", "sand_clock")
        self.mouse = self.add_actor("mouse", "mouse")
        self.bread = self.add_actor("bread", "bread")
        # Add distractors
        distractor_list = ['dumbbell', 'book', 'hammer', 'markpen', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: put bread into shoe_box
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("Wrong action (bread into shoe_box):", success)
        if not success:
            return self.info

        # Recovery: put bread back on the table
        success = self.pick_and_place(self.bread, self.table)
        print("Recovery action (bread to table):", success)
        if not success:
            return self.info

        # Correct actions: place small electronics and fragile items into shoe_box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Put small-speaker:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.shoe_box)
        print("Put sand-clock:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Put mouse:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        if (
            self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.sand_clock, self.shoe_box) and
            self.check_on(self.mouse, self.shoe_box) and
            self.check_on(self.bread, self.table)
        ):
            return True
        return False
