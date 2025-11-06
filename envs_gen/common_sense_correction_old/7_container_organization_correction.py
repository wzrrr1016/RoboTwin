from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 7_container_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.table = self.add_actor("table", "table")

        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.toycar = self.add_actor("toycar", "toycar")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Step 1: Pick mug (with handle) and place into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Step 2: Pick toycar (no handle) and place onto table (wrong)
        success = self.pick_and_place(self.toycar, self.table)
        print("pick place toycar (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick toycar from fluted_block and place onto table (correct)
        success = self.pick_and_place(self.toycar, self.table)
        print("pick place toycar (correct):", success)
        if not success:
            return self.info

        # Step 4: Pick french_fries (no handle) and place onto table (correct)
        success = self.pick_and_place(self.french_fries, self.table)
        print("pick place french_fries:", success)
        if not success:
            return self.info

        # Step 5: Pick bread (no handle) and place onto table (correct)
        success = self.pick_and_place(self.bread, self.table)
        print("pick place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check that mug (with handle) is in fluted_block
        if not self.check_on(self.mug, self.fluted_block):
            return False

        # Check that toycar (no handle) is on the table
        if not self.check_on(self.toycar, self.table):
            return False

        # Check that french_fries (no handle) is on the table
        if not self.check_on(self.french_fries, self.table):
            return False

        # Check that bread (no handle) is on the table
        if not self.check_on(self.bread, self.table):
            return False

        return True
