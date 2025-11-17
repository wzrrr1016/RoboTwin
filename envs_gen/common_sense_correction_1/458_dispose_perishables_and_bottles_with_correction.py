from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 458_dispose_perishables_and_bottles_with_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required objects and distractors in the environment"""
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add perishable foods and personal-care items
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add tool that should be kept out
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractor objects
        distractor_list = ["calculator", "pot-with-plant", "toycar", "book", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's disposal task sequence"""
        # 1. Wrongly place screwdriver in dustbin (needs recovery)
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Wrong placement of screwdriver:", success)
        if not success:
            return self.info

        # 2. Recover screwdriver back to table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Recovering screwdriver to table:", success)
        if not success:
            return self.info

        # 3. Dispose perishable foods
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Disposing french fries:", success)
        if not success:
            return self.info

        # 4. Dispose hamburg
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Disposing hamburg:", success)
        if not success:
            return self.info

        # 5. Dispose shampoo (personal-care item)
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Disposing shampoo:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all task requirements are met"""
        # Check if all required items are in the dustbin
        perishables_in_bin = (
            self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.hamburg, self.dustbin) and
            self.check_on(self.shampoo, self.dustbin)
        )
        
        # Check if tool is properly kept out (on table, not in dustbin)
        tool_properly_placed = (
            not self.check_on(self.screwdriver, self.dustbin) and
            self.check_on(self.screwdriver, self.table)
        )
        
        return perishables_in_bin and tool_properly_placed
