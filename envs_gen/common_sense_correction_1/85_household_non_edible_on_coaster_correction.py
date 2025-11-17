from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 85_household_non_edible_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        self.coaster = self.add_actor("coaster", "coaster")
        self.bell = self.add_actor("bell", "bell")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.teanet = self.add_actor("teanet", "teanet")
        distractor_list = ["apple", "baguette", "french_fries", "hamburg", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick bell and place it onto coaster
        success = self.pick_and_place(self.bell, self.coaster)
        print("Pick bell and place on coaster:", success)
        if not success:
            return self.info

        # Step 2: Pick shampoo and place it onto bell (wrong action)
        success = self.pick_and_place(self.shampoo, self.bell)
        print("Pick shampoo and place on bell (wrong):", success)

        # Step 3: If the wrong placement failed, recover by placing shampoo on coaster
        if not success:
            success = self.pick_and_place(self.shampoo, self.coaster)
            print("Recovery: Pick shampoo and place on coaster:", success)
            if not success:
                return self.info

        # Step 4: Pick teanet and place it onto coaster
        success = self.pick_and_place(self.teanet, self.coaster)
        print("Pick teanet and place on coaster:", success)
        if not success:
            return self.info

    def check_success(self):
        return (
            self.check_on(self.bell, self.coaster) and
            self.check_on(self.shampoo, self.coaster) and
            self.check_on(self.teanet, self.coaster)
        )
