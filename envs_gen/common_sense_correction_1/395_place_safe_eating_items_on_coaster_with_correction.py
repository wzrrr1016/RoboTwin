from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 395_place_safe_eating_items_on_coaster_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster
        self.coaster = self.add_actor("coaster", "coaster")
        # Add the objects
        self.can = self.add_actor("can", "can")
        self.fork = self.add_actor("fork", "fork")
        self.mouse = self.add_actor("mouse", "mouse")
        self.knife = self.add_actor("knife", "knife")
        # Add the distractors
        distractors = ["screwdriver", "toycar", "pot-with-plant", "alarm-clock", "dumbbell", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        # 1. Pick can and place on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Pick can:", success)
        if not success:
            return self.info

        # 2. Pick mouse and place on coaster (wrong action)
        success = self.pick_and_place(self.mouse, self.coaster)
        print("Pick mouse (wrong):", success)
        if not success:
            return self.info

        # 3. Recovery: pick mouse from coaster and place on table
        success = self.pick_and_place(self.mouse, self.table)
        print("Recover mouse:", success)
        if not success:
            return self.info

        # 4. Pick fork and place on coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Pick fork:", success)
        if not success:
            return self.info

        # 5. Pick knife and place on table
        success = self.pick_and_place(self.knife, self.table)
        print("Pick knife:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        can_on_coaster = self.check_on(self.can, self.coaster)
        fork_on_coaster = self.check_on(self.fork, self.coaster)
        mouse_not_on_coaster = not self.check_on(self.mouse, self.coaster)
        knife_not_on_coaster = not self.check_on(self.knife, self.coaster)

        return can_on_coaster and fork_on_coaster and mouse_not_on_coaster and knife_not_on_coaster
