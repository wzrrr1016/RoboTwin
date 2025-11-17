from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 408_place_drink_containers_on_coaster_with_correction(Imagine_Task):
    def load_actors(self):
        # Create required containers and objects
        self.coaster = self.add_actor("coaster", "coaster")
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects to the environment
        distractors = ["calculator", "screwdriver", "shoe", "book", "dumbbell"]
        self.add_distractors(distractors)

    def play_once(self):
        # Initial incorrect placement (to be recovered)
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Place toycar on coaster (wrong):", success)
        if not success:
            return self.info

        # Recovery action - move toycar back to table
        success = self.pick_and_place(self.toycar, self.table)
        print("Move toycar to table (recovery):", success)
        if not success:
            return self.info

        # Place beverage containers on coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Place bottle on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        # Place non-beverage item on table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Place shampoo on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify final state meets task requirements
        if (self.check_on(self.bottle, self.coaster) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.shampoo, self.table) and
            self.check_on(self.toycar, self.table)):
            return True
        return False
