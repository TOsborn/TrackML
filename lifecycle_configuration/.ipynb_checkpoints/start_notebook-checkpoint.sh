#!/bin/bash

set -e

##################################

# Git user info
USERNAME=""
NAME=""
EMAIL=""

# environment in which notebooks will run
CONDA_ENVIRONMENT="tensorflow_p36"

###################################

# 'here document' to run commands as ec2-user
su - ec2-user << END

# set git configuration
git config --global user.username $USERNAME
git config --global user.name $NAME
git config --global user.email $EMAIL

# activate tensorflow_p36
source activate $CONDA_ENVIRONMENT

# install helper library for the conda environment
pip install SageMaker/trackml-library/

END
