from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 1_electronic_item_placement_correction(Imagine_Task):
    def load_actors(self):
        self.plate = self.add_actor("plate", "plate")
        self.mouse = self.add_actor("mouse", "mouse")
        self.bell = self.add_actor("bell", "bell")
        self.can = self.add_actor("can", "can")
        distractor_list = ['pet-collar', 'table-tennis', 'sand-clock', 'shoe', 'book', 'dumbbell']
        self.add_distractors(distractor_list)
        self.check_scene()

    def play_once(self):
        # Step 1: Pick bell and place into plate (wrong)
        success = self.pick_and_place(self.bell, self.plate)
        print("Pick bell into plate:", success)
        if not success:
            return self.info

        # Step 2: Pick bell from plate and place back on table (recovery)
        success = self.pick_and_place(self.bell, self.table)
        print("Pick bell into table:", success)
        if not success:
            return self.info

        # Step 3: Pick mouse and place into plate (correct)
        success = self.pick_and_place(self.mouse, self.plate)
        print("Pick mouse into plate:", success)
        if not success:
            return self.info

        # Step 4: Pick can and place back on table (ensuring it is not in the plate)
        success = self.pick_and_place(self.can, self.table)
        print("Pick can into table:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        mouse_on_plate = self.check_on(self.mouse, self.plate)
        bell_not_on_plate = not self.check_on(self.bell, self.plate)
        can_not_on_plate = not self.check_on(self.can, self.plate)
        return mouse_on_plate and bell_not_on_plate and can_not_on_plate
