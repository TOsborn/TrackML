#!/bin/bash

set -e

##################################

GIT_USERNAME=""
GIT_NAME=""
GIT_EMAIL=""

KAGGLE_USERNAME=""
KAGGLE_KEY=""
KAGGLE_COMPETITION="trackml-particle-identification"

CONDA_ENVIRONMENT="tensorflow_p36"

###################################

# save kaggle api token
su ec2-user -c "mkdir /home/ec2-user/.kaggle"
su ec2-user -c "echo \"{\\\"username\\\": \\\"$KAGGLE_USERNAME\\\", \\\"key\\\": \\\"$KAGGLE_KEY\\\"}\" > /home/ec2-user/.kaggle/kaggle.json"

# ensure kaggle api key is not viewable by other users (and suppress warnings)
su ec2-user -c "chmod 600 /home/ec2-user/.kaggle/kaggle.json"

# 'here document' to run commands as ec2-user
su - ec2-user << END

set -e

# set git configuration
git config --global user.username $GIT_USERNAME
git config --global user.name $GIT_NAME
git config --global user.email $GIT_EMAIL

# install and configure Kaggle CLI
pip install kaggle
kaggle config set -n competition -v trackml-particle-identification

# activate tensorflow_p36
source activate $CONDA_ENVIRONMENT

# install helper library in the conda environment
pip install SageMaker/trackml-library/

END
