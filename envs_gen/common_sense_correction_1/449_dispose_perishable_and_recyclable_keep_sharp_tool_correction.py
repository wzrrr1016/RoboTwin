from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 449_dispose_perishable_and_recyclable_keep_sharp_tool_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.knife = self.add_actor("knife", "knife")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")
        self.book = self.add_actor("book", "book")
        
        # Add distractor objects
        distractors = ["calculator", "pet-collar", "toycar", "pot-with-plant", "alarm-clock"]
        self.add_distractors(distractors)

    def play_once(self):
        # Place perishable food (french fries) in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french fries:", success)
        if not success:
            return self.info

        # Place empty metal container (can) in dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Place can:", success)
        if not success:
            return self.info

        # Wrong action: Place sharp tool (knife) in dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Wrongly place knife:", success)
        if not success:
            return self.info

        # Recovery: Remove sharp tool from dustbin and place on book
        success = self.pick_and_place(self.knife, self.book)
        print("Recover knife:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify correct items are in dustbin and sharp tool is removed
        if (self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.knife, self.book)):
            return True
        return False
