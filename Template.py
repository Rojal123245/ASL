import os
from pathlib import Path
import logging


#logger to check this this folders are created without error
logging.basicConfig(level=logging.INFO,format = '[%(asctime)s]: %(message)s:')

package_name = "ASLD_step2"

list_of_files = [
    ".github/workflows/.gitkeep", #for empty folder just create .gitkeep file so that it will stored in gitub
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/components/__init__.py",
    f"src/{package_name}/utils/__init__.py",
    f"src/{package_name}/config/__init__.py",
    f"src/{package_name}/pipeline/__init__.py",
    f"src/{package_name}/entity/__init__.py",
    f"src/{package_name}/constants/__init__.py",
    "tests/__init__.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",
    "configs/config.yaml",  #configuration
    "dvc.yaml",             #for dvc pipeline
    "params.yaml",          #training parameter yaml
    "init_setup.sh",        #shell script for creation of environment
    "requiremets.txt",      #
    "requirements_dev.txt", #for creation of development steps
    "setup.py",             #
    "setup.cfg",            #setup config
    "pyproject.toml",       #for python packages only
    "tox.ini",              #testing of project locally
    "research/trials.ipynb", #our jupyter trails test
]

#create these files
for filepath in list_of_files:
    filepath = Path(filepath)
    #since some files are created with no folder but some has folder
    filedir,filename = os.path.split(filepath)
    if filedir !="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating the directory: {filedir} for file :{filename}")

    #if file already present and have size then don't create it again
    if(not os.path.exists(filepath)) or (os.path.getsize(filepath) ==0):
        with open(filepath,"w")as f:
            pass #creating an empty files
            logging.info(f"creating empty file:{filepath}")
    else:
        logging.info(f"filename already exist:{filename}")
