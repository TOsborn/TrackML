#!/bin/bash

set -e

# 'here document' to run commands as ec2-user
su - ec2-user << END

cd SageMaker
git clone https://github.com/LAL/trackml-library

END
