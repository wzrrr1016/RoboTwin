
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class cup_sorting_spill_recover(Imagine_Task):
    def load_actors(self):
        # Containers
        self.fluted_block = self.add_actor("fluted-block", "fluted-block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Cups
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.cup_with_liquid = self.add_actor("cup-with-liquid", "cup-with-liquid")

    def play_once(self):
        # Mistake: move cup-with-liquid to wooden_box first, then recover to fluted-block
        success = self.pick_and_place(self.cup_with_liquid, self.wooden_box)
        print("mistake cup-with-liquid->wooden_box:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.cup_with_liquid, self.fluted_block)
        print("recover cup-with-liquid->fluted-block:", success)
        if not success:
            return self.info

        # Correct: place cup_with_handle and cup_without_handle into wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("place cup_with_handle->wooden_box:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.cup_without_handle, self.wooden_box)
        print("place cup_without_handle->wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Dry cups in wooden_box; liquid cup on fluted-block
        return (
            self.check_on(self.cup_with_handle, self.wooden_box)
            and self.check_on(self.cup_without_handle, self.wooden_box)
            and self.check_on(self.cup_with_liquid, self.fluted_block)
        )
