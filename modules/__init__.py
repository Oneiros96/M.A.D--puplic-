from .database import SQLite, init_database
from .update_db import update_db
from .simplex_quotation import create_simplex_quotation, create_simplex_quotation_preview
from .customers import save_customer, update_customers
from .fabelzier_quotation import fabelzier_create_quotation, create_fabelzier_quotation_preview
from .geierlamm_quoation import create_geierlamm_quotation_preview, geierlamm_create_quotation
from .db_backup import db_backup

from os import path, makedirs

def init_data_folder():
    ############################################
    # Checks if the nessesary folder structure #
    # to store user generated Data exists.     #
    # data/                                    #
    #   simplex/                               #
    ############################################
    data_folder_path = path.join(path.dirname(__file__), f"../data")
    simplex_folder_path = path.join(path.dirname(__file__), f"../data/simplex")
    fabel_folder_path = path.join(path.dirname(__file__), f"../data/fabelzier")
    geier_folder_path = path.join(path.dirname(__file__), f"../data/geierlamm")
    db_backups_path = path.join(path.dirname(__file__), f"../data/db_backups")
    
    paths = [data_folder_path, simplex_folder_path, fabel_folder_path, geier_folder_path, db_backups_path]
    for folder_path in paths:
        if not path.exists(folder_path):
            makedirs(folder_path)
    

init_data_folder()
