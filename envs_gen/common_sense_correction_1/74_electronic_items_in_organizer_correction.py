from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 74_electronic_items_in_organizer_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.microphone = self.add_actor("microphone", "microphone")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.mouse = self.add_actor("mouse", "mouse")
        
        # Add distractors
        distractor_list = ['shoe', 'book', 'hammer', 'tissue-box', 'markpen']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick microphone and place into fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("Place microphone:", success)
        if not success:
            return self.info

        # Step 2: Pick pot-with-plant and place into fluted_block (wrong action)
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Wrongly place pot:", success)
        if not success:
            return self.info

        # Step 3: Recover by placing pot_with_plant back on the table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Recover pot to table:", success)
        if not success:
            return self.info

        # Step 4: Pick mouse and place into fluted_block
        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("Place mouse:", success)
        if not success:
            return self.info

        # Step 5: Pick french_fries and place on the table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Place french fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify that electronic accessories (microphone, mouse) are in fluted_block
        # and perishable foods (french_fries) and living decor (pot_with_plant) are on the table
        if (self.check_on(self.microphone, self.fluted_block) and
            self.check_on(self.mouse, self.fluted_block) and
            self.check_on(self.pot_with_plant, self.table) and
            self.check_on(self.french_fries, self.table)):
            return True
        return False
