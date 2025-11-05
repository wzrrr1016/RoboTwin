from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_organization_correction_1(Imagine_Task):
    def load_actors(self):
        # Load all required objects into the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.fork = self.add_actor("fork", "fork")
        self.book = self.add_actor("book", "book")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")

    def play_once(self):
        # Place healthy items on fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.book, self.fluted_block)
        print("Pick and place book:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Pick and place sand-clock:", success)
        if not success:
            return self.info

        # Place unhealthy items into dustbin
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Pick and place hamburg:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.fork, self.dustbin)
        print("Pick and place fork:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if healthy items are on fluted_block
        if (self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.book, self.fluted_block) and
            self.check_on(self.sand_clock, self.fluted_block)):
            # Check if unhealthy items are in dustbin
            if (self.check_on(self.hamburg, self.dustbin) and
                self.check_on(self.fork, self.dustbin)):
                return True
        return False
