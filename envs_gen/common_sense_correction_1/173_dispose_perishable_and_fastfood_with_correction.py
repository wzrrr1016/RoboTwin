from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 173_dispose_perishable_and_fastfood_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add the main objects to the environment
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.toycar = self.add_actor("toycar", "toycar")
        self.cup = self.add_actor("cup", "cup")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects to the environment
        distractors = ["calculator", "hammer", "screwdriver", "book", "dumbbell"]
        self.add_distractors(distractors)

    def play_once(self):
        # Wrong action: Place toycar in dustbin
        success = self.pick_and_place(self.toycar, self.dustbin)
        print("Wrong toycar placement:", success)
        if not success:
            return self.info

        # Recovery action: Place toycar back on table
        success = self.pick_and_place(self.toycar, self.table)
        print("Recovery toycar:", success)
        if not success:
            return self.info

        # Correct actions for food items
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Hamburg placement:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("French fries placement:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bread, self.dustbin)
        print("Bread placement:", success)
        if not success:
            return self.info

        # Place cup on table (non-food item)
        success = self.pick_and_place(self.cup, self.table)
        print("Cup placement:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all required objects are in their correct locations
        if (
            self.check_on(self.hamburg, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.toycar, self.table) and
            self.check_on(self.cup, self.table)
        ):
            return True
        return False
