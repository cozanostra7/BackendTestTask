# 1. Clone the repo
git clone https://github.com/cozanostra7/BackendTestTask.git

cd BackendTestTask


# 2. Create and activate virtual environment
python -m venv venv


venv\Scripts\activate       # Windows


source venv/bin/activate    # Mac/Linux


# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file in the root
Populate the .env file with data provided in https://rnacentral.org/help/public-database


# 5. Run the server
python src/main.py
