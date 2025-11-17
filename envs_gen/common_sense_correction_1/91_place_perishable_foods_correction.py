from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 91_place_perishable_foods_correction(Imagine_Task):
    def load_actors(self):
        self.plate = self.add_actor("plate", "plate")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.toycar = self.add_actor("toycar", "toycar")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        distractor_list = ["calculator", "hammer", "stapler", "alarm-clock", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: place toycar on plate
        success = self.pick_and_place(self.toycar, self.plate)
        print("Pick toycar to plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: place toycar on table
        success = self.pick_and_place(self.toycar, self.table)
        print("Pick toycar to table (recovery):", success)
        if not success:
            return self.info

        # Place apple on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Pick apple to plate:", success)
        if not success:
            return self.info

        # Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick bread to plate:", success)
        if not success:
            return self.info

        # Place shampoo on table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Pick shampoo to table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        apple_on_plate = self.check_on(self.apple, self.plate)
        bread_on_plate = self.check_on(self.bread, self.plate)
        toycar_not_on_plate = not self.check_on(self.toycar, self.plate)
        shampoo_not_on_plate = not self.check_on(self.shampoo, self.plate)
        return apple_on_plate and bread_on_plate and toycar_not_on_plate and shampoo_not_on_plate
