from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 43_metal_object_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the plate
        self.plate = self.add_actor("plate", "plate")
        # Add the metal objects
        self.can = self.add_actor("can", "can")
        self.bell = self.add_actor("bell", "bell")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        # Add the tissue-box (non-metal, used in wrong action)
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        # Add distractors
        distractors = ['calculator', 'baguette', 'shoe', 'book', 'alarm-clock', 'fluted_block']
        self.add_distractors(distractors)
        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        # Step 1: Pick can and place into plate
        success = self.pick_and_place(self.can, self.plate)
        print("Pick can:", success)
        if not success:
            return self.info

        # Step 2: Pick bell and place into plate
        success = self.pick_and_place(self.bell, self.plate)
        print("Pick bell:", success)
        if not success:
            return self.info

        # Step 3: Pick tissue-box and place into plate (wrong action)
        success = self.pick_and_place(self.tissue_box, self.plate)
        print("Pick tissue-box (wrong):", success)
        if not success:
            return self.info

        # Step 4: Pick tissue-box from plate and place back on table (recovery)
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Recover tissue-box:", success)
        if not success:
            return self.info

        # Step 5: Pick screwdriver and place into plate
        success = self.pick_and_place(self.screwdriver, self.plate)
        print("Pick screwdriver:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        # Check if all metal objects are on the plate
        can_on_plate = self.check_on(self.can, self.plate)
        bell_on_plate = self.check_on(self.bell, self.plate)
        screwdriver_on_plate = self.check_on(self.screwdriver, self.plate)

        # Check if tissue-box is NOT on the plate (i.e., it was recovered)
        tissue_not_on_plate = not self.check_on(self.tissue_box, self.plate)

        # Return True only if all conditions are met
        return can_on_plate and bell_on_plate and screwdriver_on_plate and tissue_not_on_plate
