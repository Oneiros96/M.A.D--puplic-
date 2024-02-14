from docxtpl import DocxTemplate
from os import path
from datetime import datetime

# offer_data = {
#     "customer": 
#     {
#         "name": "Bart Simpson", 
#         "street": "Evergreen Terrace", 
#         "street_nr": "742", 
#         "postal_code": "12345", 
#         "city": "Springfield"
#     }, 
#     "project_data": 
#     {
#         "project_name": "Demo", 
#         "days": "2", 
#         "times": 
#         [
#             {
#                 "start": "19:05", 
#                 "end": "11:05", 
#                 "date": "2024-02-02"
#             }, 
#             {
#                 "start": "23:05", 
#                 "end": "19:05", 
#                 "date": "2024-02-03"
#             }
#         ], 
#         "validity_period": "14"
#     }, 
#     "base_costs": 
#     {
#         "rides": "2", 
#         "distance": "6", 
#         "price_km": "0.45", 
#         "assembly_fee": "360", 
#         "vat_rate": "0"
#     }, 
#     "offers": 
#     [
#         {
#             "id": "232", 
#             "name": "Feuerspucken", 
#             "vat_rate": "7"
#         }, 
#         {
#             "id": "233", 
#             "name": "M\u00e4rchenerz\u00e4hlerei", 
#             "vat_rate": "19"
#         }
#     ], 
#     "offer_bundle": 
#     [
#         {
#             "id": "232", 
#             "name": "Feuerspucken", 
#             "vat_rate": "7"
#         }, 
#         {
#             "id": "233", 
#             "name": "M\u00e4rchenerz\u00e4hlerei", 
#             "vat_rate": "0"
#         }
#     ]
# }
def geierlamm_create_quotation(quotation_data):
    customer, base_costs, offers, offer_bundle = quotation_data["customer"], quotation_data["base_costs"], quotation_data["offers"], quotation_data["offer_bundle"] 
    project_data = date_formates(quotation_data["project_data"],)


    today = datetime.now()
    ymd = today.strftime("%Y.%m.%d")
    dmy = today.strftime("%d.%m.%Y")

    doc = DocxTemplate(path.join(path.dirname(__file__), f"../templates/geierlamm_template.docx"))
    context = {
         "customer": customer,
         "date": dmy,
         "project_data": project_data,
         "base_costs": base_costs,
         "offers": offers,
         "offer_bundle": offer_bundle
         }
    
    doc.render(context)
    doc.save(path.join(path.dirname(__file__), f"../data/geierlamm/{ymd}_{customer['name']}.docx"))
    
def date_formates(project_data):
    for time in project_data["times"]:
        if time["date"]:
            date_object = datetime.strptime(time["date"], "%Y-%m-%d")
            time["date"] = date_object.strftime('%d.%m.%Y')
    return project_data

def create_geierlamm_quotation_preview(quotation_data, db):
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
    base_costs["total_brutto"] = round((base_costs["travel_costs"] + float(base_costs["assembly_fee"])), 2)
    base_costs["vat"] = round((base_costs["total_brutto"] * float(base_costs["vat_rate"]) / 100), 2)
    base_costs["total_netto"] = round((base_costs["total_brutto"] - base_costs["vat"]), 2)
    
    # ensure all prices have have two decimal digits
    base_costs["travel_costs"] = "{:.2f}".format(base_costs["travel_costs"])
    base_costs["assembly_fee"] = "{:.2f}".format(float(base_costs["assembly_fee"]))
    base_costs["total_brutto"] = "{:.2f}".format(base_costs["total_brutto"])
    base_costs["vat"] = "{:.2f}".format(base_costs["vat"])
    base_costs["total_netto"] = "{:.2f}".format(base_costs["total_netto"])
   
    return base_costs

def get_offers(offers, total_base_costs, db):
    offer_list = []
    
    for offer in offers:
        offer_data = db.execute("SELECT name, price_brutto, description FROM offers WHERE offer_id = ?", (offer["id"],))[0]
        offer_data["price_total"] = round((float(offer_data["price_brutto"]) + float(total_base_costs)), 2)
        offer_data["vat_rate"] = int(offer["vat_rate"])
        offer_data["vat"] = round((offer_data["price_brutto"] * float(offer_data["vat_rate"]) / 100), 2)
        offer_data["price_netto"] = round((offer_data["price_brutto"] - offer_data["vat"]), 2)

        offer_data["price_total"] = "{:.2f}".format(offer_data["price_total"])
        offer_data["price_brutto"] = "{:.2f}".format(offer_data["price_brutto"])
        offer_data["vat"] = "{:.2f}".format(offer_data["vat"])
        offer_data["price_netto"] = "{:.2f}".format(offer_data["price_netto"])
        offer_list.append(offer_data)
    
    return offer_list

def get_offer_bundle(offer_bundle, total_base_costs, db):
    bundle = {
        "name": "",
        "price_brutto": 0,
        "price_total": 0,
        "price_netto": 0,
        "vat7": 0,
        "vat19": 0,
        }
    
    for offer in offer_bundle:
        offer_data = db.execute("SELECT name, price_brutto FROM offers WHERE offer_id = ?", (offer["id"],))[0]
        if bundle["name"] == "":
            bundle["name"] = offer_data["name"]
        else:
            bundle["name"] += " + " + offer_data["name"]
        brutto_price = offer_data["price_brutto"]
        bundle["price_brutto"] += brutto_price
        # vat rate calculation
        vat_rate = int(offer["vat_rate"])
        if vat_rate == 7:
            vat = round(brutto_price * 7 / 100)
            bundle["vat7"] += vat
            bundle["price_netto"] += round(brutto_price - vat, 2)
        elif vat_rate == 19:
            vat = round(brutto_price * 19 / 100)
            bundle["vat19"] += vat
            bundle["price_netto"] += round(brutto_price - vat, 2)
        else:
            bundle["price_netto"] += brutto_price

    bundle["price_total"] = bundle["price_brutto"] + float(total_base_costs)
    
    bundle["price_brutto"] = "{:.2f}".format(bundle["price_brutto"])
    bundle["price_total"] = "{:.2f}".format(bundle["price_total"])
    bundle["price_netto"] = "{:.2f}".format(bundle["price_netto"])
    bundle["vat7"] = "{:.2f}".format(bundle["vat7"])
    bundle["vat19"] = "{:.2f}".format(bundle["vat19"])
    return bundle