# TO INSTALL 

## Steps:
1. Install python
   1. Can be done however you wish, commands below do this threw brew
        - The first command installs brew, not needed if you already have it installed
   2. Install pip (the package manager)  (if not already installed)
2. Create virtual environment
   - This is just a place for all the required stuff to go, so doesn't affect the rest of your computer
3. Activate the virtual environment 
4. Install all required components
5. Build the app

## Commands
Can mostly just be copy-pasted into the terminal  
with an optional prayer to the almighty omnisiah 
```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
    python -m ensurepip --upgrade
    python -m venv .venv  
    source .venv/bin/activate  
    pip install -r requirements.txt  
    pyinstaller main.spec
```