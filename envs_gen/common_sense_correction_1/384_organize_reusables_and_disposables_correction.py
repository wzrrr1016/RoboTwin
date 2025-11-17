from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 384_organize_reusables_and_disposables_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add task-specific objects to the environment
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.hammer = self.add_actor("hammer", "hammer")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractor objects to the environment
        distractor_list = ['chips-tub', 'milk-box', 'jam-jar', 'olive-oil']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions to complete the waste sorting task.
        This includes both correct actions and recovery from an initial mistake.
        """
        # Step 1: Wrong placement of book into dustbin (initial mistake)
        success = self.pick_and_place(self.book, self.dustbin)
        print("Pick book and place into dustbin (wrong):", success)
        if not success:
            return self.info
        
        # Step 2: Recovery action - move book from dustbin to fluted_block
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Pick book from dustbin and place into fluted_block (recovery):", success)
        if not success:
            return self.info
        
        # Step 3: Place tissue-box (disposable item) into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Pick tissue-box and place into dustbin:", success)
        if not success:
            return self.info
        
        # Step 4: Place hammer (reusable item) into fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Pick hammer and place into fluted_block:", success)
        if not success:
            return self.info
        
        # Step 5: Place pink_block (valuable item) into fluted_block
        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Pick pink_block and place into fluted_block:", success)
        if not success:
            return self.info
        
        # Step 6: Place small-speaker (reusable item) into fluted_block
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Pick small-speaker and place into fluted_block:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        """
        Verify if all objects are in their correct containers according to the task requirements.
        """
        # Check if all objects are in their correct containers
        if (self.check_on(self.book, self.fluted_block) and
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.pink_block, self.fluted_block) and
            self.check_on(self.small_speaker, self.fluted_block)):
            return True
        return False
