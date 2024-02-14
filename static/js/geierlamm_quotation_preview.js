function calculate_travel_costs() {
    rides = document.getElementById("rides").value
    distance = document.getElementById("distance").value
    price_km = document.getElementById("price_km").value

    document.getElementById("travel_costs").value = (rides * distance * price_km).toFixed(2)
    calculate_base_costs()
}

function calculate_base_costs() {
    const travel_costs = Number(document.getElementById("travel_costs").value)
    const assembly_fee = Number(document.getElementById("assembly_fee").value)
    const vat_rate = Number(document.getElementById("base_costs_vat_rate").value)
    const base_costs_total = travel_costs + assembly_fee
    const vat = base_costs_total * vat_rate / 100
    const base_costs_total_netto = base_costs_total - vat
    
    document.getElementById("base_costs_total").value = base_costs_total.toFixed(2)
    document.getElementById("base_costs_vat").value = vat.toFixed(2)
    document.getElementById("base_costs_total_netto").value = base_costs_total_netto.toFixed(2)
    calculate_offers_total_on_basecost_change()
} 
function calculate_offers_total_on_basecost_change() {
    //offers
    let offers = Array.from(document.getElementsByName("offer"))
    const base_costs_total = Number(document.getElementById("base_costs_total").value)
    offers.forEach(offer => {
        const price = Number(offer.querySelector("[name='price'").value)
        offer.querySelector("[name='price_total']").value = (price + base_costs_total).toFixed(2)
    })
    //offer bundle
    const offer_bundle_price = Number(document.getElementById("offer_bundle_price_with_discount").value)
    document.getElementById("offer_bundle_price_total").value = (offer_bundle_price + base_costs_total).toFixed(2)
}

function calculate_offer_on_price_change(element) {
    const price = Number(element.value)
    const base_costs_total = Number(document.getElementById("base_costs_total").value)
    const vat_rate = Number(element.parentElement.parentElement.parentElement.querySelector("[name='vat_rate'").value)
    const price_total = price + base_costs_total
    const vat = price * vat_rate / 100
    const price_netto = price - vat
    
    element.parentElement.parentElement.parentElement.querySelector("[name='price_total'").value = price_total.toFixed(2)
    element.parentElement.parentElement.parentElement.querySelector("[name='vat'").value = vat.toFixed(2)
    element.parentElement.parentElement.parentElement.querySelector("[name='price_netto'").value = price_netto.toFixed(2)
    
}

const offer_bundle_vat7 = Number(document.getElementById("offer_bundle_vat7").value)
const offer_bundle_vat19 = Number(document.getElementById("offer_bundle_vat19").value)
const offer_bundle_netto = Number(document.getElementById("offer_bundle_price_netto").value)
function calculate_bundle_on_discount_change() {
    const discount = Number(document.getElementById("discount").value)
    const price_netto = offer_bundle_netto * (100 - discount) / 100
    const vat7 = offer_bundle_vat7 * (100 - discount) / 100
    const vat19 = offer_bundle_vat19 * (100 - discount) / 100
    const price_brutto = price_netto + vat7 + vat19
    const price_total = price_brutto + Number(document.getElementById("base_costs_total").value)

    document.getElementById("offer_bundle_price_netto").value = price_netto.toFixed(2)
    document.getElementById("offer_bundle_vat19").value = vat19.toFixed(2)
    document.getElementById("offer_bundle_vat7").value = vat7.toFixed(2)
    document.getElementById("offer_bundle_price_brutto").value = price_brutto.toFixed(2)
    document.getElementById("offer_bundle_price_total").value = price_total.toFixed(2)
}

let offer_data = []
function get_offer_data() {
    let customer = {
        "name": document.getElementsByName("customer_name")[0].value,
        "street": document.getElementsByName("customer_street")[0].value,
        "street_nr": document.getElementsByName("customer_street_nr")[0].value,
        "postal_code": document.getElementsByName("customer_postal_code")[0].value,
        "city": document.getElementsByName("customer_city")[0].value
    }

    let project_data = {
        "project_name": document.getElementsByName("project_name")[0].value,
        "days": document.getElementsByName("days")[0].value,
        "times": [],
        "validity_period": document.getElementsByName("validity_period")[0].value
    }
    //get times
    time_rows = document.querySelectorAll("[name='times']");
    time_rows.forEach(time_row => {
        let time = {
            "start": time_row.querySelector("[name='start']").value,
            "end": time_row.querySelector("[name='end']").value,
            "date": time_row.querySelector("[name='date']").value
        }
        project_data.times.push(time)
    })

    let base_costs = {
        "rides": document.getElementsByName("rides")[0].value,
        "distance": document.getElementsByName("distance")[0].value,
        "price_km": document.getElementsByName("price_km")[0].value,
        "assembly_fee": document.getElementsByName("assembly_fee")[0].value,
        "travel_costs": document.getElementsByName("travel_costs")[0].value,
        "brutto": document.getElementsByName("base_costs_total")[0].value,
        "netto": document.getElementById("base_costs_total_netto").value,
        "vat_rate": document.getElementById("base_costs_vat_rate").value,
        "vat": document.getElementById("base_costs_vat").value
    }

    let offers = []
    //get offers
    const offer_array = document.querySelectorAll("[name='offer']")
    offer_array.forEach(offer_data => {
        const offer = {
            "name": offer_data.querySelector("[name='name']").value,
            "price_brutto": Number(offer_data.querySelector("[name='price']").value).toFixed(2),
            "price_total": offer_data.querySelector("[name='price_total']").value,
            "description": offer_data.querySelector("[name='description']").textContent,
            "price_netto": offer_data.querySelector("[name='price_netto']").value,
            "vat": Number(offer_data.querySelector("[name='vat']").value).toFixed(2),
            "vat_rate": offer_data.querySelector("[name='vat_rate']").value
        }
        offers.push(offer)
    })

    let offer_bundle = {
        "name": document.getElementsByName("offer_bundle_name")[0].value,
        "price_netto": Number(document.getElementById("offer_bundle_price_netto").value).toFixed(2),
        "discount": document.getElementById("discount").value,
        "vat7": Number(document.getElementById("offer_bundle_vat7").value).toFixed(2),
        "vat19": Number(document.getElementById("offer_bundle_vat19").value).toFixed(2),
        "price_brutto": Number(document.getElementsByName("offer_bundle_price_brutto")[0].value).toFixed(2),
        "price_total": Number(document.getElementsByName("offer_bundle_price_total")[0].value).toFixed(2),
        "description": document.getElementsByName("offer_bundle_description")[0].textContent,
        "discount": document.getElementsByName("discount")[0].value,
        
    }

    offer_data = {
        customer: customer,
        project_data: project_data,
        base_costs: base_costs,
        offers: offers,
        offer_bundle: offer_bundle
    }
}