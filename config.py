import os

####################################
# Load .env file
####################################

try:
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv("./.env"))
except ImportError:
    print("dotenv not installed, skipping...")

MODEL_NAME = os.getenv("MODEL_NAME", "jbochi/madlad400-3b-mt")
