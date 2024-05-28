To set up and activate the .venv environment:
./setup_env.sh

Deactivate the Conda base environment:
conda deactivate

Prevent Conda base from auto-activating:
conda config --set auto_activate_base false





1. Create the Virtual Environment:
python3 -m venv .venv

2. Activate the Virtual Environment:
source .venv/bin/activate
Activating the virtual environment modifies your shell's environment variables so that it uses the Python interpreter and packages installed within the .venv directory. You'll see the name of your virtual environment appear in parentheses at the beginning of your command prompt.

3. Install Dependencies:
pip install -r requirements.txt
If your project has dependencies listed in the requirements.txt file, use this command to install them within the virtual environment.

4. Load Environment Variables (Optional):
There are several ways to load environment variables from your .env file into the virtual environment:

python-dotenv:
pip install python-dotenv

Add the following to the top of your Python script:
Python
from dotenv import load_dotenv
load_dotenv()

or:
autoenv (Zsh plugin):

Bash
git clone https://github.com/hyperupcall/autoenv.git $ZSH_CUSTOM/plugins/autoenv
Add autoenv to your .zshrc plugins list and create a .env file in your project directory.

Manual Sourcing:
source .env



Example (using python-dotenv):
Python:
from dotenv import load_dotenv
load_dotenv()

import os

api_key = os.getenv("API_KEY")
database_url = os.getenv("DATABASE_URL")

# ... Rest of your Python script using the variables from the .env file

Important Considerations:

.env Files and Version Control: Never commit your .env file to version control systems like Git. This file often contains sensitive information like API keys, passwords, etc. Use a .gitignore file to exclude it.
Zsh Integration: If you prefer a more seamless way to activate your virtual environment whenever you enter your project directory, consider using the Zsh plugin "autoenv" or similar tools.
Multiple Environments: If you need different sets of dependencies or environment variables, you can create multiple virtual environments (e.g., .venv-dev, .venv-prod).