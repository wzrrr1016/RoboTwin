from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 386_store_decorative_and_paper_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the main objects
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.book = self.add_actor("book", "book")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors
        distractor_list = ["apple", "chips-tub", "jam-jar", "calculator", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place book and sand-clock into the wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("pick place book:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.wooden_box)
        print("pick place sand-clock:", success)
        if not success:
            return self.info

        # Place knife on the wooden_box (outside)
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("pick place knife:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if book and sand-clock are inside the wooden_box
        book_inside = self.check_on(self.book, self.wooden_box)
        sand_clock_inside = self.check_on(self.sand_clock, self.wooden_box)

        # Check if pot-with-plant is NOT inside the wooden_box
        pot_outside = not self.check_on(self.pot_with_plant, self.wooden_box)

        # Check if knife is on the wooden_box (outside)
        knife_on_box = self.check_on(self.knife, self.wooden_box)

        return book_inside and sand_clock_inside and pot_outside and knife_on_box
