from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 38_ready_to_eat_on_plate_with_correction(Imagine_Task):
    def load_actors(self):
        self.plate = self.add_actor("plate", "plate")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.knife = self.add_actor("knife", "knife")
        self.fork = self.add_actor("fork", "fork")
        distractor_list = ["calculator", "pot-with-plant", "shoe", "book", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        success = self.pick_and_place(self.apple, self.plate)
        print("pick place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bread, self.plate)
        print("pick place bread:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.fork, self.table)
        print("pick place fork:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.knife, self.table)
        print("pick place knife:", success)
        if not success:
            return self.info

    def check_success(self):
        if (
            self.check_on(self.apple, self.plate) and
            self.check_on(self.bread, self.plate) and
            not self.check_on(self.knife, self.plate) and
            not self.check_on(self.fork, self.plate)
        ):
            return True
        return False
