# M.A.D

M.A.D is a tool for managing services and customer addresses of three companies in a database and generating offers for customers. As it was developed for a German client, the code and README are in English, but the content displayed is in German.

## Installation

### Windows

1. **Install Python 3.12:**
   - Download the installer from [python.org](https://www.python.org/downloads/release/python-312/)
   - Follow the installation instructions, ensuring to add Python to your PATH.

2. **Install Python Packages:**
   ```bash
   pip install Flask==2.3.3 pywebview==4.3.2 docxtpl==0.16.7
   ```

3. **Download Bootstrap:**
   - Download Bootstrap from [getbootstrap.com](https://getbootstrap.com/docs/5.3/getting-started/download/)
   - Move `bootstrap.css` and `bootstrap.css.map` to `static/css` folder.
   - Move `bootstrap.bundle.js` and `bootstrap.bundle.js.map` to `static/js` folder.

4. **Download Tippy.js:**
   - Download Tippy.js from [unpkg.com/@popperjs/core@2](https://unpkg.com/@popperjs/core@2) and [unpkg.com/tippy.js@6](https://unpkg.com/tippy.js@6)
   - Move the files to `static/js` folder.

### Linux

1. **Install Python 3.12:**
   - Use your package manager to install Python 3.12.
     For example, on Ubuntu:
     ```bash
     sudo apt update
     sudo apt install python3.12
     ```

2. **Install Python Packages:**
   ```bash
   pip install Flask==2.3.3 pywebview==4.3.2 docxtpl==0.16.7
   ```

3. **Download Bootstrap:**
   - Download Bootstrap from [getbootstrap.com](https://getbootstrap.com/docs/5.3/getting-started/download/)
   - Move `bootstrap.css` and `bootstrap.css.map` to `static/css` folder.
   - Move `bootstrap.bundle.js` and `bootstrap.bundle.js.map` to `static/js` folder.

4. **Download Tippy.js:**
   - Download Tippy.js from [unpkg.com/@popperjs/core@2](https://unpkg.com/@popperjs/core@2) and [unpkg.com/tippy.js@6](https://unpkg.com/tippy.js@6)
   - Move the files to `static/js` folder.

## Project Description

### Database
On the database page, services with prices, value-added tax rates, and descriptions can be created, edited, and deleted. There is a table provided for each company, "Fabelzier" and "Geierlamm," while tables for "Simplex Callidus" can be created and named as desired under settings. The "Sontiges" table contains basic prices necessary for creating offers.
Before deleting individual entries or leaving the database page, all changes should be saved, as they will otherwise be lost.

### Offer Creation
Clicking on the buttons of the respective company takes you to the form for creating offers, where customer and project data can be entered, and services from the database can be dragged and dropped into the form. 
Clicking on the offer preview button at the bottom right takes you to the preview of the offer to be created, where project data and prices can be adjusted.  
To save an offer as a (company-specific) template, enter a name in the field next to the save and load buttons and then click on save. 
Clicking on the name field selects and loads existing templates. 
To modify an existing template, select it again in the name field and click on save.

### Offer Preview
The offer preview contains an overview of the project data, as well as the offered services including prices and VAT. Prices and project data can still be edited here. Changing a price automatically recalculates all dependent prices. 
Clicking on the create offer button at the bottom right generates a Word document with the finished offer. Created offers are saved under `/data/<companyname>`.

### Customer Database
In the customer database, names and addresses of customers can be added, edited, and deleted. If an offer is created for a customer who is not yet in the database, they are automatically saved.

### Settings
Here, database tables for "Simplex Callidus" can be created, renamed, and deleted. 
Furthermore, saved offer templates can be renamed and deleted.

### Backup
At each program start, a backup of the database is automatically created and saved in `/data/db_backups`.
