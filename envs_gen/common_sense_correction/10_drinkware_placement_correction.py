from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 10_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.scanner = self.add_actor("scanner", "scanner")
        self.toycar = self.add_actor("toycar", "toycar")
        self.hammer = self.add_actor("hammer", "hammer")

        # Add distractors
        distractor_list = ['shoe', 'book', 'pot-with-plant', 'sand-clock', 'tissue-box', 'shampoo']
        self.add_distractors(distractor_list)

        self.check_scene()

    def play_once(self):
        # Place mug on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug on coaster:", success)
        if not success:
            return self.info

        # Wrong action: place scanner on coaster
        success = self.pick_and_place(self.scanner, self.coaster)
        print("Wrong: Place scanner on coaster:", success)
        if not success:
            return self.info

        # Recovery: move scanner to fluted_block
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("Recover: Place scanner into fluted_block:", success)
        if not success:
            return self.info

        # Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        # Place hammer into fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Place hammer:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        if (self.check_on(self.mug, self.coaster) and
            self.check_on(self.scanner, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.hammer, self.fluted_block)):
            return True
        return False
