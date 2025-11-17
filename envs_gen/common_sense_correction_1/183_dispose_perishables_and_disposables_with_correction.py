from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 183_dispose_perishables_and_disposables_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add the objects
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.bread = self.add_actor("bread", "bread")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.bottle = self.add_actor("bottle", "bottle")
        # Add distractors
        distractor_list = ['pot-with-plant', 'pet-collar', 'sand-clock', 'shoe', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Pick bread and place into dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Pick bread to dustbin:", success)
        if not success:
            return self.info

        # Pick bottle and place into dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Pick bottle to dustbin:", success)
        if not success:
            return self.info

        # Wrong action: place screwdriver into dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Pick screwdriver to dustbin (wrong):", success)
        if not success:
            return self.info

        # Recovery: place screwdriver back to table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Pick screwdriver from dustbin to table:", success)
        if not success:
            return self.info

        # Place small speaker on table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Pick small speaker to table:", success)
        if not success:
            return self.info

        # Place orange block on table
        success = self.pick_and_place(self.orange_block, self.table)
        print("Pick orange block to table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are in the correct locations
        if (self.check_on(self.bread, self.dustbin) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.screwdriver, self.table) and
            self.check_on(self.small_speaker, self.table) and
            self.check_on(self.orange_block, self.table)):
            return True
        return False
