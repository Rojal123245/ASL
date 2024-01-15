echo [$(date)]: "START"
echo [$(date)]: "Creating the environment with python version 3.8"
conda create --prefix ./env python=3.8 -y
echo [$(date)]: "activating the environemnt"
source  activate ./env
echo [$(date)]: "installing the dev requiremets.txt"
pip install -r requirements.txt
echo [$(date)]: "END"