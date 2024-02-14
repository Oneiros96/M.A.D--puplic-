from docxtpl import DocxTemplate
from os import path
from datetime import datetime

#offer_data={
#   "customer": {
#       "name": "Grundschule Nebra", 
#       "street": "Schulstra\u00dfe", 
#       "street_nr": "1", 
#       "postal_code": "12345", 
#       "city": "Nebra"
#   }, 
#    "project_data": {
#        "project_name": "fabelzier demo", 
#        "days": "2", 
#        "times": [
#            {
#                "start": "10:00", 
#                "end": "18:00", 
#                "date": "2024-01-01"
#                }, 
#            {
#                "start": "10:00", 
#                "end": "16:00", 
#                "date": "2024-01-02"
#                }
#        ], 
#        "validity_period": "14"
#        }, 
#    "base_costs": {
#        "rides": "4", 
#        "distance": "35", 
#        "price_km": "0.45", 
#        "staff": "1", 
#        "price_day": "170", 
#        "assembly_fee": "360"
#        }, 
#    "offers": [
#        {
#            "id": "232", 
#            "name": "Feuerspucken"
#            }, 
#        {
#            "id": "233", 
#            "name": "M\u00e4rchenerz\u00e4hlerei"
#            }
#        ], 
#    "offer_bundle": [
#        {
#            "id": "233", 
#            "name": "M\u00e4rchenerz\u00e4hlerei"
#            }, 
#        {
#            "id": "232", 
#           "name": "Feuerspucken"}
#           ]
#}
def fabelzier_create_quotation(quotation_data):
    customer, base_costs, offers, offer_bundle = quotation_data["customer"], quotation_data["base_costs"], quotation_data["offers"], quotation_data["offer_bundle"] 
    project_data = date_formates(quotation_data["project_data"],)

    #needed for if statement in template
    offer_bundle["discount"] = int(offer_bundle["discount"])

    today = datetime.now()
    ymd = today.strftime("%Y.%m.%d")
    dmy = today.strftime("%d.%m.%Y")

    doc = DocxTemplate(path.join(path.dirname(__file__), f"../templates/fabelzier_template.docx"))
    context = {
         "customer": customer,
         "date": dmy,
         "project_data": project_data,
         "base_costs": base_costs,
         "offers": offers,
         "offer_bundle": offer_bundle
         }
    
    doc.render(context)
    doc.save(path.join(path.dirname(__file__), f"../data/fabelzier/{ymd}_{customer['name']}.docx"))
    
def date_formates(project_data):
    for time in project_data["times"]:
        if time["date"]:
            date_object = datetime.strptime(time["date"], "%Y-%m-%d")
            time["date"] = date_object.strftime('%d.%m.%Y')
    return project_data

def create_fabelzier_quotation_preview(quotation_data, db):
    customer = quotation_data["customer"]
    project_data = quotation_data["project_data"]
    base_costs = calculate_base_costs(project_data, quotation_data["base_costs"])
    offers = get_offers(quotation_data["offers"], base_costs["total_brutto"], db)
    offer_bundle = ""
    if quotation_data["offer_bundle"]:
        offer_bundle = get_offer_bundle(quotation_data["offer_bundle"], base_costs["total_brutto"], db)
    return customer, project_data, base_costs, offers, offer_bundle
    
def calculate_base_costs(project_data, base_costs):
    # calculation of nessesary values
    base_costs["travel_costs"] = round((float(base_costs["rides"]) * float(base_costs["distance"]) * float(base_costs["price_km"])), 2)
    base_costs["staff_costs"] = round((float(base_costs["staff"]) * float(base_costs["price_day"]) * float(project_data["days"])) , 2)
    base_costs["total_brutto"] = round((base_costs["travel_costs"] + base_costs["staff_costs"] + float(base_costs["assembly_fee"])), 2)
    
    
    # ensure all prices have have two decimal digits
    base_costs["travel_costs"] = "{:.2f}".format(base_costs["travel_costs"])
    base_costs["staff_costs"] = "{:.2f}".format(base_costs["staff_costs"])
    base_costs["assembly_fee"] = "{:.2f}".format(float(base_costs["assembly_fee"]))
    base_costs["total_brutto"] = "{:.2f}".format(base_costs["total_brutto"])
   
    return base_costs

def get_offers(offers, total_base_costs, db):
    offer_list = []
    
    for offer in offers:
        offer_data = db.execute("SELECT name, price_brutto, description FROM offers WHERE offer_id = ?", (offer["id"],))[0]
        offer_data["price_total"] = round((float(offer_data["price_brutto"]) + float(total_base_costs)), 2)
        offer_data["price_total"] = "{:.2f}".format(offer_data["price_total"])
        offer_data["price_brutto"] = "{:.2f}".format(offer_data["price_brutto"])
        offer_list.append(offer_data)
    
    return offer_list

def get_offer_bundle(offer_bundle, total_base_costs, db):
    bundle = {
        "name": "",
        "price": 0,
        "price_total": 0}
    
    for offer in offer_bundle:
        offer_data = db.execute("SELECT name, price_brutto FROM offers WHERE offer_id = ?", (offer["id"],))[0]
        if bundle["name"] == "":
            bundle["name"] = offer_data["name"]
        else:
            bundle["name"] += " + " + offer_data["name"]
        bundle["price"] += offer_data["price_brutto"]
    bundle["price_total"] = bundle["price"] + float(total_base_costs)
    bundle["price"] = "{:.2f}".format(bundle["price"])
    
    return bundle