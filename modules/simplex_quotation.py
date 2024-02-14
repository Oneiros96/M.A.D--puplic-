from docxtpl import DocxTemplate
from os import path
from datetime import datetime





#'quotation_data = {
#   'customer': {
#        'name': 'Grundschule Springfield', 
#        'street': 'Schulstraße', 
#        'street_nr': '4', 
#        'postal_code': '12345', 
#        'city': 'Springfield'
#       }, 
#    
#   'project_data': {
#        'days': '3', 
#        'participants': '40',
#        'project_name': 'Testangebot',
#        'customer_staff': '2-4',
#        'project_theme': 'Mittelalter'
#        'validity_period: '14'
#       },
#    
#   'base_costs': {
#        'rides': '4', 
#        'distance': '23', 
#        'price_km': '0.45', 
#        'staff': '3', 
#        'price_day': '170', 
#        'assembly_fee': '360'
#       }, 
#   
#   'projects': {
#       "test": [
#           {"id":"8","name":"Stadt Modell + Handelsspiel"},
#           {"id":"10","name":"Korb flechten***"}
#       ],
#       "daten":[
#           {"id":"13","name":"Kartenspiel basteln**"},
#           {"id":"13","name":"Kartenspiel basteln**"}]
#   }'

def create_simplex_quotation(quotation_data):
    customer = quotation_data["customer"]
    project_data = quotation_data["project_data"]
    base_costs = quotation_data["base_costs"]
    project_days = quotation_data["project_days"]
    total_cost = quotation_data["total_cost"]
    total_cost_pp = quotation_data["total_cost"]
    
    today = datetime.now()
    ymd = today.strftime("%Y.%m.%d")
    dmy = today.strftime("%d.%m.%Y")
    
    doc = DocxTemplate(path.join(path.dirname(__file__), f"../templates/simplex_template.docx"))
    context = {
        "customer": customer,
        "date": dmy,
        "project_data": project_data,
        "base_costs": base_costs,
        "project_days": project_days,
        "total_cost": total_cost,
        "total_cost_pp": total_cost_pp
        }
    
    doc.render(context)
    doc.save(path.join(path.dirname(__file__), f"../data/simplex/{ymd}_{customer['name']}.docx"))

def create_simplex_quotation_preview(quotation_data, db):
    customer = quotation_data["customer"]
    project_data = quotation_data["project_data"]
    base_costs = calculate_base_costs(project_data, quotation_data["base_costs"])
    project_days = get_project_days(quotation_data["projects"], project_data["participants"], db)
    total_cost = "{:.2f}".format(float(project_days["total_cost"]) + float(base_costs["total_brutto"]))
    total_cost_pp = "{:.2f}".format(float(project_days["total_cost_pp"]) + float(base_costs["per_participant"]))
    return customer, project_data, base_costs, project_days, total_cost, total_cost_pp
    

def calculate_base_costs(project_data, base_costs):
    # calculation of nessesary values
    base_costs["travel_costs"] = round((float(base_costs["rides"]) * float(base_costs["distance"]) * float(base_costs["price_km"])), 2)
    base_costs["staff_costs"] = round((float(base_costs["staff"]) * float(base_costs["price_day"]) * float(project_data["days"])) , 2)
    base_costs["total_brutto"] = round((base_costs["travel_costs"] + base_costs["staff_costs"] + float(base_costs["assembly_fee"])), 2)
    base_costs["total_netto"] = round(((base_costs["total_brutto"] * 100) / 107), 2)
    base_costs["vat"] = round((base_costs["total_netto"] * 0.07), 2)
    base_costs["per_participant"] = round((base_costs["total_brutto"] / int(project_data["participants"])), 2)
    # ensure all prices have have two decimal digits
    base_costs["travel_costs"] = "{:.2f}".format(base_costs["travel_costs"])
    base_costs["staff_costs"] = "{:.2f}".format(base_costs["staff_costs"])
    base_costs["assembly_fee"] = "{:.2f}".format(float(base_costs["assembly_fee"]))
    base_costs["total_brutto"] = "{:.2f}".format(base_costs["total_brutto"])
    base_costs["total_netto"] = "{:.2f}".format(base_costs["total_netto"])
    base_costs["vat"] = "{:.2f}".format(base_costs["vat"])
    base_costs["per_participant"] = "{:.2f}".format(base_costs["per_participant"])

    return base_costs

def get_project_days(projects, participants, db):
    project_days = {
        "project_days": [],
        "total_cost": 0,
        "total_cost_pp": 0
    }
    for project_name, offer_list in projects.items():
        project_day = {
            "name": project_name,
            "offers": [],
            "cost": "",
            "cost_pp": ""
        }
        offers = []
        cost_pp = 0
        for item in offer_list:
            offer = db.execute("SELECT name, price_brutto, description FROM offers WHERE offer_id = ?", (item["id"],))[0]
            cost_pp += offer["price_brutto"]
            offer["price_total"] = "{:.2f}".format(round((offer["price_brutto"] * int(participants)), 2))
            offer["price_brutto"] = "{:.2f}".format((offer["price_brutto"]))
            offers.append(offer)
        
        cost = cost_pp * int(participants)
        project_day["cost"] = "{:.2f}".format(cost)
        project_day["cost_pp"] = "{:.2f}".format(cost_pp)
        project_day["offers"] = offers
        project_days["project_days"].append(project_day)

        project_days["total_cost"] += cost
        project_days["total_cost_pp"] += cost_pp
    project_days["total_cost"] = "{:.2f}".format(project_days["total_cost"])
    project_days["total_cost_pp"] = "{:.2f}".format(project_days["total_cost_pp"])
    return project_days
