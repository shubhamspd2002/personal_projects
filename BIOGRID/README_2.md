# BIOGRID (Biological General Repository for Interaction Datasets)
## Project by Shubham Prabhudesai

**BIOGRID** is a **public database** that stores **biological interaction data**, including:

- **Protein-protein interactions (PPIs)**
- **Genetic interactions**
- **Chemical interactions**
- **Post-translational modifications**

## Key Features
- Covers multiple organisms (humans, yeast, bacteria, etc.).
- Data sourced from **published literature** and **high-throughput experiments**.
- Provides **APIs and downloadable datasets** for bioinformatics research.

## Use Cases
- Identifying protein-protein interaction networks.
- Analyzing disease-related gene interactions.
- Drug discovery and pathway analysis.

🔗 **Access BIOGRID**: [https://thebiogrid.org/](https://thebiogrid.org/)

## Steps for the user to acces this project:
- Clone the project in your local repository.
- Create a virtual environment
- If on windows, activate it by typing the following:
  -      source (name of your venv)/Scripts/activate
- If on mac/linux, activate it by typing the following:
  -      source (name of your venv)/bin/activate
- Run the following commands in your gitbash shell to install dependencies:
  -     pip install pdm
  -     pdm install
- If any errors occur during the dependency installations, delete the virtual environment and reinstall it with a different python version. and follow the steps again to install the dependencies
- If any other problems, try closing and reopening VS code.
- To run tests, on the LHS panel, click on the test tube icon called testing. 
  - Click Configure Python Tests
  - Click pytest and then click tests
  - In case you select the wrong options, just go to your explorer (ctrl/cmd + shift + e) and then delete .vscode folder and follow the above steps again
  - To run the tests, click 'run tests' which is a small play button in the testing GUI or in the shell type: 
  -     pytest
  - To check the coverage of your project, in the shell type: 
  -     pytest --cov

## Steps used to create this project
- For the project from the main 
- Download the files from gitlab biogrid project using a zip file method. 
- Make a new project by the same name in your personal gitlab account and clone it.
- Extract all the files from the zip file and paste it in the clone in you local repository.
- Make sure you have a GitBash command shell.
- Create a virtual environment and make sure it is active. If not, then you can run the following command: 
  - source (name of your venv)/Scripts/activate
- Then run the following commands:
  -     pdm init
  -     pdm add pandas
  -     pdm add sqlalchemy
  -     pdm add -dG tests pytest
  -     pdm add -dG tests pytest-cov
- Shift the test_software folder into the tests folder
 - In the folder src\biogrid, create a folder named db and inside it, create manager.py, models.py and __ init __.py files.
 - In the manager.py and models.py files check whether the classes and methods can be imported by the test_software.py file.
- Stage the changes:
  -     git add .
- Commit the changes:
  -     git commit -m "commit message"
- Push to the remote repository:
  -     git push
- Create a dev branch
  -     git branch dev
- Also create a branch with the same name remotely. Execute the following command:
  -     git push --set-upstream origin dev
  -  or
  -     git push -u origin dev
  - What It Does:
    - Pushes your local dev branch to the remote repository (origin).
    - Links (sets upstream for) your local dev branch to the remote dev branch.
    - After this, you can just use git push and git pull without specifying origin dev every time.
- In the models.py file create the classes Protein, Organism, Interaction. For the creation of each class, create a separate branch from dev by the same name and merge with dev.
- In the manager.py file create the classes Importer and Query. For the creation of each class, create a separate branch from dev by the same name and merge with dev. 
- During the creation of the classes Importer and Query, look at the test_software.py file and make sure the names of the methods you create in manager.py are identical to the method names under their respective test_ functions in test_software.py.
- Take a closer look at the normalization and renaming of some columns and make changes accordingly.
- When the final class Query is created and the branch is merged into dev, run the tests. To run it, the following steps were followed:
  - On the LHS panel, click on the test tube icon called testing. 
  - Click Configure Python Tests
  - Click pytest and then click tests
  - In case you select the wrong options, just go to your explorer (ctrl/cmd + shift + e) and then delete .vscode folder and follow the above steps again
  - To run the tests, click 'run tests' which is a small play button in the testing GUI or in the shell type: 
  -     pytest
  - To check the coverage of your project, in the shell type: 
  -     pytest --cov
- If any bugs or errors, fix them so that all the tests pass.
- Now create a Jupyter Notebook and use the BIOGRID-CORONAVIRUS-4.4.242.tab3 data to make the classes, dataframes and dabatase. If any errors and bugs, fix them.
- Then create the doc strings for all the classes and the methods and merge dev into main


