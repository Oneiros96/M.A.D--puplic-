from flask import Flask, redirect, render_template, request, jsonify
import webview, json
from modules import SQLite, init_database, update_db,  save_customer, update_customers, db_backup 
from modules import create_simplex_quotation, create_simplex_quotation_preview, fabelzier_create_quotation, create_fabelzier_quotation_preview, create_geierlamm_quotation_preview, geierlamm_create_quotation

app = Flask(__name__)
window = webview.create_window("", app)
db_backup()
db = SQLite("./data/offers.db")
init_database(db)

@app.route("/", methods = ["GET"])
def index():
   data = db.execute("SELECT * FROM offers")
   tables = db.execute("SELECT * FROM tables")
   # move "Sontiges" table (id 3 = list index 2) to the end of the list
   tables.append(tables.pop(2))
   return render_template("index.html", tables = tables, data = data)

############
# Database #
############
@app.route("/delete_offer", methods = ["POST"])
def delete_offer():
   db.execute("DELETE FROM offers WHERE offer_id =?", (request.form["offer_id"],))
   return redirect("/")

@app.route("/update_all", methods = ["POST"])
def update_all():
   updates = json.loads(request.form["updates"])
   update_db(updates, db)
   return redirect("/")

#########
#Simplex#
#########
@app.get("/simplex")
def simplex():
   data, tables, prices, save_names, customers = simplex_render_data()
   quotation_data = None
   return render_template("simplex.html", quotation_data = quotation_data, data = data, 
                          tables = tables, prices = prices, save_names = save_names, customers = customers)

@app.post("/simplex/quotation_preview")
def simplex_quotation_preview():
   quotation_data = json.loads(request.form["data"])
   customer, project_data, base_costs, project_days, total_cost, total_cost_pp = create_simplex_quotation_preview(quotation_data, db)
   return render_template("simplex_quotation_preview.html", customer = customer, project_data = project_data, 
                          base_costs = base_costs, project_days = project_days, total_cost = total_cost, 
                          total_cost_pp = total_cost_pp)

@app.post("/simplex/render_quotation")
def simplex_render_quotation():
   quotation_data = json.loads(request.form["data"])
   save_customer(quotation_data["customer"], db)
   create_simplex_quotation(quotation_data)
   return redirect("/simplex")


@app.post("/simplex/save_quotation")
def save_simplex_qoutation():
   save_data = request.json
   data_json = json.dumps(save_data["data"])
   if save_data["quotation_id"]:
      db.execute("UPDATE simplex_quotations SET name = ?, data = ? WHERE id = ?",(save_data["quotation_name"], data_json, save_data["quotation_id"]) )
   else:
      db.execute("INSERT INTO simplex_quotations (name, data) VALUES (?, ?)", (save_data["quotation_name"], data_json))
   return jsonify({'message': 'success'}),200

@app.get("/simplex/load_quotation/")
def load_simplex_quotation():
   quotation_id =  request.args.get("quotation_id")
   if not quotation_id:
      return redirect("/simplex")
   quotation_data = json.loads(db.execute("SELECT data FROM simplex_quotations WHERE id = ?", (quotation_id,))[0]["data"])
   data, tables, prices, save_names, customers = simplex_render_data()
   return render_template("simplex.html", quotation_data = quotation_data, data = data, tables = tables, prices = prices, save_names = save_names, customers = customers)

def simplex_render_data():
   data = db.execute("SELECT offer_id, name, table_id FROM offers")
   tables = db.execute("SELECT * FROM tables WHERE table_id  >= 4") # starting by table 4 to exclude fabelzier/geierlamm/default tables
   prices = db.execute("SELECT price_brutto FROM offers WHERE offer_id <= 3")
   customers = db.execute("SELECT name FROM customers ORDER BY name")
   save_names = db.execute("SELECT id, name FROM simplex_quotations ORDER BY name")

      
   return data, tables, prices, save_names, customers

###########
#Fabelzier#
###########
@app.get("/fabelzier")
def fabelzier():
   fabelzier_offers, customers, prices, save_names = fabelzier_render_data()
   return render_template("fabelzier.html", fabelzier_offers = fabelzier_offers, customers = customers, prices = prices, save_names = save_names)

@app.post("/fabelzier/save_quotation")
def save_fabelzier_qoutation():
   save_data = request.json
   data_json = json.dumps(save_data["data"])
   if save_data["quotation_id"]:
      db.execute("UPDATE fabelzier_quotations SET name = ?, data = ? WHERE id = ?",(save_data["quotation_name"], data_json, save_data["quotation_id"]) )
   else:
      db.execute("INSERT INTO fabelzier_quotations (name, data) VALUES (?, ?)", (save_data["quotation_name"], data_json))
   return jsonify({'message': 'success'}),200

@app.get("/fabelzier/load_quotation")
def fabelzier_load_quoataion():
   quotation_id =  request.args.get("quotation_id")
   if not quotation_id:
      return redirect("/fabelzier")
   quotation_data = json.loads(db.execute("SELECT data FROM fabelzier_quotations WHERE id = ?", (quotation_id,))[0]["data"])
   fabelzier_offers, customers, prices, save_names = fabelzier_render_data()
   return render_template("fabelzier.html", quotation_data = quotation_data, fabelzier_offers = fabelzier_offers, customers = customers, prices = prices, save_names = save_names)

@app.post("/fabelzier/quotation_preview/")
def fabelzier_quotation_preview():
   quotation_data = json.loads(request.form["data"])
   customer, project_data, base_costs, offers, offer_bundle = create_fabelzier_quotation_preview(quotation_data, db)
   return render_template("/fabelzier_quotation_preview.html", customer = customer, project_data = project_data, base_costs = base_costs, offers = offers, offer_bundle = offer_bundle)

@app.post("/fabelzier/render_quotation")
def fabelzier_render_quotation():
   quotation_data = json.loads(request.form["data"])
   save_customer(quotation_data["customer"], db)
   fabelzier_create_quotation(quotation_data)
   return redirect("/fabelzier")

def fabelzier_render_data():
   fabelzier_offers = db.execute("SELECT name, offer_id FROM offers WHERE table_id = 1")
   customers = db.execute("SELECT name FROM customers ORDER BY name")
   prices = db.execute("SELECT price_brutto FROM offers WHERE offer_id <= 3")
   save_names = db.execute("SELECT id, name FROM fabelzier_quotations ORDER BY name")
   return fabelzier_offers, customers, prices, save_names

###########
#Geierlamm#
###########
@app.get("/geierlamm")
def geierlamm():
   offers, customers, prices, save_names = geierlamm_render_data()
   return render_template("geierlamm.html", offers = offers, customers = customers, prices = prices, save_names = save_names)

@app.post("/geierlamm/save_quotation")
def save_geierlamm_qoutation():
   save_data = request.json
   data_json = json.dumps(save_data["data"])
   if save_data["quotation_id"]:
      db.execute("UPDATE geierlamm_quotations SET name = ?, data = ? WHERE id = ?",(save_data["quotation_name"], data_json, save_data["quotation_id"]) )
   else:
      db.execute("INSERT INTO geierlamm_quotations (name, data) VALUES (?, ?)", (save_data["quotation_name"], data_json))
   return jsonify({'message': 'success'}),200

@app.get("/geierlamm/load_quotation")
def geierlamm_load_quotation():
   quotation_id =  request.args.get("quotation_id")
   if not quotation_id:
      return redirect("/geierlamm")
   quotation_data = json.loads(db.execute("SELECT data FROM geierlamm_quotations WHERE id = ?", (quotation_id,))[0]["data"])
   offers, customers, prices, save_names = geierlamm_render_data()
   return render_template("geierlamm.html", quotation_data = quotation_data, offers = offers, customers = customers, prices = prices, save_names = save_names)

@app.post("/geierlamm/quotation_preview/")
def geierlamm_quotation_preview():
   quotation_data = json.loads(request.form["data"])
   customer, project_data, base_costs, offers, offer_bundle = create_geierlamm_quotation_preview(quotation_data, db)
   return render_template("/geierlamm_quotation_preview.html", customer = customer, project_data = project_data, base_costs = base_costs, offers = offers, offer_bundle = offer_bundle)

@app.post("/geierlamm/render_quotation")
def geierlamm_render_quotation():
   quotation_data = json.loads(request.form["data"])
   save_customer(quotation_data["customer"], db)
   geierlamm_create_quotation(quotation_data)
   return redirect("/geierlamm")

def geierlamm_render_data():
   offers = db.execute("SELECT name, offer_id FROM offers WHERE table_id = 2")
   customers = db.execute("SELECT name FROM customers ORDER BY name")
   prices = db.execute("SELECT price_brutto FROM offers WHERE offer_id <= 3")
   save_names = db.execute("SELECT id, name FROM geierlamm_quotations ORDER BY name")
   return offers, customers, prices, save_names


###########
#Customers#
###########
@app.route("/customers", methods = ["GET", "POST"])
def customers():
   if request.method == "POST":
      updates = json.loads(request.form["updates"])
      update_customers(updates, db)
   customers = db.execute("SELECT * FROM customers ORDER BY name")
   return render_template("customers.html", customers = customers)

@app.get("/customer_data")
def return_customer_data():
   customer_name = request.args.get("customer_name_input")
   customer_data = db.execute("SELECT * FROM customers WHERE name = ?", (customer_name,))
   if customer_data:
      return jsonify(customer_data[0])
   else:
      return jsonify({
          "street": "",
          "street_nr": "",
          "postal_code": "",
          "city:": ""
              })

@app.post("/delete_customer")
def delete_customer():
   db.execute("DELETE FROM customers WHERE customer_id =?", (request.form["customer_id"],))
   return redirect("/customers")

#################
# Settings Menu #
#################

@app.route("/settings", methods = ["GET"])
def settings():
   tables = db.execute("SELECT * FROM tables")
   simplex_quotations = db.execute("SELECT id, name FROM simplex_quotations ORDER BY name")
   fabelzier_quotations = db.execute("SELECT id, name FROM fabelzier_quotations ORDER BY name")
   geierlamm_quotations = db.execute("SELECT id, name FROM geierlamm_quotations ORDER BY name")
   return render_template("settings.html", tables = tables, simplex_quotations = simplex_quotations, fabelzier_quotations = fabelzier_quotations, geierlamm_quotations = geierlamm_quotations)

@app.route("/new_table", methods=["POST"])
def tables():
   db.execute("INSERT INTO tables (name) VALUES(?)", (request.form["new_table_name"],))
   return redirect("/settings")                                                                

@app.route("/delete_table", methods = ["POST"])
def delete_table():   
   db.execute("DELETE FROM tables WHERE table_id=?", (request.form["table_id"],))
   db.execute("DELETE FROM offers WHERE table_id =?", (request.form["table_id"],))
   return redirect("/settings")

@app.route("/update_table_name", methods = ["POST"])
def update_table_name():
   db.execute("UPDATE tables SET name = ? WHERE table_id = ?",(request.form["table_name"], request.form["table_id"]))
   return redirect("/settings")

@app.post("/update_simplex_quotation")
def update_simplex_quotation():
   db.execute("UPDATE simplex_quotations SET name = ? WHERE id = ?", (request.form["name"], request.form["id"]))
   return redirect("/settings")

@app.post("/delete_simplex_quotation")
def delete_simplex_quotation():
   db.execute("DELETE FROM simplex_quotations WHERE id = ?", (request.form["id"],))
   return redirect("/settings")

@app.post("/update_fabelzier_quotation")
def update_fabelzier_quotation():
   db.execute("UPDATE fabelzier_quotations SET name = ? WHERE id = ?", (request.form["name"], request.form["id"]))
   return redirect("/settings")

@app.post("/delete_fabelzier_quotation")
def delete_fabelzier_quotation():
   db.execute("DELETE FROM fabelzier_quotations WHERE id = ?", (request.form["id"],))
   return redirect("/settings")

@app.post("/update_geierlamm_quotation")
def update_geierlamm_quotation():
   db.execute("UPDATE geierlamm_quotations SET name = ? WHERE id = ?", (request.form["name"], request.form["id"]))
   return redirect("/settings")

@app.post("/delete_geierlamm_quotation")
def delete_geierlamm_quotation():
   db.execute("DELETE FROM geierlamm_quotations WHERE id = ?", (request.form["id"],))
   return redirect("/settings")

if __name__ == "__main__":
   #app.run(debug=True)
   webview.start()