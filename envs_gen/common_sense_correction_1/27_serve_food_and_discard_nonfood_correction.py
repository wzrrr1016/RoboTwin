from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 27_serve_food_and_discard_nonfood_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers (plate, dustbin), objects (bread, hamburg, can, teanet, knife),
        and distractors.
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.can = self.add_actor("can", "can")
        self.teanet = self.add_actor("teanet", "teanet")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors
        distractor_list = ["red_block", "pot-with-plant", "small-speaker", "sand-clock", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot places edible items on the plate and non-edible/hazardous items in the dustbin.
        """
        # Place edible items on the plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick and place bread:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hamburg, self.plate)
        print("Pick and place hamburg:", success)
        if not success:
            return self.info

        # Wrongly place knife on the plate (recovery step will follow)
        success = self.pick_and_place(self.knife, self.plate)
        print("Pick and place knife (wrong):", success)
        if not success:
            return self.info

        # Recover knife and place it in the dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Recover knife to dustbin:", success)
        if not success:
            return self.info

        # Place non-edible items in the dustbin
        success = self.pick_and_place(self.teanet, self.dustbin)
        print("Pick and place teanet:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.dustbin)
        print("Pick and place can:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        All edible items must be on the plate, and all non-edible/hazardous items must be in the dustbin.
        """
        # Check if edible items are on the plate
        edible_on_plate = (
            self.check_on(self.bread, self.plate) and
            self.check_on(self.hamburg, self.plate)
        )

        # Check if non-edible/hazardous items are in the dustbin
        non_edible_in_dustbin = (
            self.check_on(self.knife, self.dustbin) and
            self.check_on(self.teanet, self.dustbin) and
            self.check_on(self.can, self.dustbin)
        )

        return edible_on_plate and non_edible_in_dustbin
