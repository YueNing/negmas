from negmas import (SAOMechanism, 
                    AspirationNegotiator, 
                    MappingUtilityFunction, 
                    CheckpointRunner
                )
import uuid
from negmas.helpers import unique_name
from pathlib import Path, PosixPath

negmas_version = "0.37" 

class Instance:
    """
    Instance of negmas

    1. negmas.mechanisms. return a mechanism Instance can be used for gym_negmas
    2. negmas.world. return a world Instance can be used for gym_negmas
    
    """
    def __init__(self, 
            checkpoint_folder=None, 
            checkpoint_filename=None, 
            seed=None
    ):
        self.checkpoint_folder = checkpoint_folder
        self.checkpoint_filename = checkpoint_filename
        self.seed = seed
        self.sessions = None

    def launch_session(self, agent):
        self.create_mechanism_session()

        self.runner = CheckpointRunner(folder=self.new_folder)
        self.runner.reset()
    
    def step(self):
        """
        step run the runner
        """
        self.runner.step()
        # self._object is the seesion, generate the observation space here
        self._object = self.runner.__object

    def create_mechanism_session(self):
        import shutil
        tmp_path = "./tmp"
        fork_after_reset = True
        # create a new folder
        self.new_folder: Path = tmp_path / unique_name("empty", sep="")
        # used for copy mode 
        self.second_folder: Path = tmp_path / unique_name("second", sep="")
        self.new_folder.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(self.new_folder)
        self.new_folder.mkdir(parents=True, exist_ok=True)
        filename = "mechanism"
        self.second_folder.mkdir(parents=True, exist_ok=True)
        n_outcomes, n_negotiators = 5, 3
        n_steps = 50
        self.mechanism = SAOMechanism(
            outcomes=n_outcomes,
            n_steps=n_steps,
            offering_is_accepting=True,
            avoid_ultimatum=False,
            checkpoint_every=2,
            checkpoint_folder=self.new_folder,
            checkpoint_filename=filename,
            extra_checkpoint_info=None,
            exist_ok=True,
            single_checkpoint=True,
        )
        ufuns = MappingUtilityFunction.generate_random(n_negotiators, outcomes=n_outcomes)
        for i in range(n_negotiators):
            self.mechanism.add(AspirationNegotiator(name=f"agent{i}"), ufun=ufuns[i])

        self.mechanism.run()

    
    def kill(self):
        """
        force close a session
        """
        pass

    def close(self):
        """
        close a session
        """
        pass


        



