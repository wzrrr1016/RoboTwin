from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_organization_17(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Load objects
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.drill = self.add_actor("drill", "drill")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Step 1: Pick shampoo and place into fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("pick place shampoo:", success)
        if not success:
            return self.info

        # Step 2: Pick drill and place into fluted_block (wrong)
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("pick place drill (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick drill from fluted_block and place into plate
        success = self.pick_and_place(self.drill, self.plate)
        print("pick place drill to plate:", success)
        if not success:
            return self.info

        # Step 4: Pick pot-with-plant and place into fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("pick place pot_with_plant:", success)
        if not success:
            return self.info

        # Step 5: Pick bread and place into plate
        success = self.pick_and_place(self.bread, self.plate)
        print("pick place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if shampoo and pot_with_plant are in fluted_block
        # Check if drill and bread are in plate
        if (self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.drill, self.plate) and
            self.check_on(self.bread, self.plate)):
            return True
        return False
