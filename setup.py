from setuptools import find_packages,setup
from typing import List


HYPHEN_E_DOT="-e ."
def get_requirements(file_path:str)->List[str]:
    """
    this function will return lists of requirements
    """
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","")for req in requirements]   # while reading from the .txt it will also add the \n for next line which must be removed.
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
    name='ML Project1',
    version='0.0.1',
    author='Jaskaran Singh',
    author_email='jaskaransaggu1699@gmail.com',
    packages=find_packages(),   # finds all packages in the project
    install_requires=get_requirements('requirements.txt')
)