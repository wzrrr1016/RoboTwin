from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 327_dispose_disposables_and_perishables_with_correction(Imagine_Task):
    def load_actors(self):
        self.can = self.add_actor("can", "can")
        self.bottle = self.add_actor("bottle", "bottle")
        self.apple = self.add_actor("apple", "apple")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "shoe", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        success = self.pick_and_place(self.can, self.dustbin)
        print("Pick can:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.dumbbell, self.dustbin)
        print("Pick dumbbell (wrong):", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.dumbbell, self.table)
        print("Recover dumbbell:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Pick bottle:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.dustbin)
        print("Pick apple:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        can_in = self.check_on(self.can, self.dustbin)
        bottle_in = self.check_on(self.bottle, self.dustbin)
        apple_in = self.check_on(self.apple, self.dustbin)
        dumbbell_not_in = not self.check_on(self.dumbbell, self.dustbin)
        return can_in and bottle_in and apple_in and dumbbell_not_in
