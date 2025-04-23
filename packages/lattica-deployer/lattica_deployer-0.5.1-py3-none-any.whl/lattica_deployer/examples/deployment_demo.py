import torch

from lattica_deployer import common
from lattica_deploy.homomorphic_operations.operators import (
    SequentialHomOp, HomLinear, HomSquare, HomMatMul
)
from lattica import interface_deploy as toolkit_interface

from lattica_deployer_src.lattica_deployer.internal_demos.lattica_deploy_local import LocalLatticaDeploy


# Initialize LocalLatticaDeploy with your token
deployer = LocalLatticaDeploy("<YOUR-TOKEN-HERE>")

model_id = "<MODEL_ID>"

# Read parameters from config file
homomorphic_params = common.read_params_config('params.yaml')
is_ckks = True
homomorphic_params['is_ckks'] = is_ckks

# Get a worker
worker_session_id = deployer.start_worker(model_id)

# Init context on server
deployer.init_model_context(homomorphic_params, is_ckks=is_ckks, model=model_id)

# Create your pipeline
hom_pipeline = SequentialHomOp(
    (HomLinear((128, 10)), True),
    (SequentialHomOp(
        (HomSquare(), False),
        (HomMatMul((3, 128)), True)
    ), True)
)

# Set weights
hom_pipeline.set_data(toolkit_interface.T_ENG, is_ckks, (0,), torch.randn((128, 10)), torch.randn(128))
hom_pipeline.set_data(toolkit_interface.T_ENG, is_ckks, (1,1), torch.randn((3, 128)))

# Deploy the pipeline
common.deploy_pipeline(hom_pipeline, model_id)
