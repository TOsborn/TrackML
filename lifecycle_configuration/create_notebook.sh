#!/bin/bash

set -e

#########################################

CONDA_ENVIRONMENT="tensorflow_p36"

#########################################

# 'here document' to run commands as ec2-user
su - ec2-user << END

set -e

# activate and then deactivate conda environment so that tensorflow version optimized for cpu is installed
# (for some unknown reason, waiting until the environment is activated in the start_notebook file causes the instance to fail)
source activate tensorflow_p36
source deactivate

cd SageMaker
git clone https://github.com/LAL/trackml-library

END
