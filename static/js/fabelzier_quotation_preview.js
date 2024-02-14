function calculate_travel_costs() {
    rides = document.getElementById("rides").value
    distance = document.getElementById("distance").value
    price_km = document.getElementById("price_km").value

    document.getElementById("travel_costs").value = (rides * distance * price_km).toFixed(2)
    calculate_base_costs_total()
}

function calulate_staff_costs() {
    const staff = document.getElementById("staff").value
    const price_day = document.getElementById("price_day").value
    const days = document.getElementById("days").value
    
    document.getElementById("staff_costs").value = (staff * price_day * days).toFixed(2)
    
    calculate_base_costs_total()
}

function calculate_base_costs_total() {
    const travel_costs = Number(document.getElementById("travel_costs").value)
    const staff_costs = Number(document.getElementById("staff_costs").value)
    const assembly_fee = Number(document.getElementById("assembly_fee").value)

    document.getElementById("base_costs_total").value = (travel_costs +  staff_costs + assembly_fee).toFixed(2)
    calculate_offers_total_on_basecost_change()
} 

document.getElementById("base_costs_total").addEventListener("change", calculate_offers_total_on_basecost_change)

function calculate_offers_total_on_basecost_change() {
    //offers
    let offers = Array.from(document.getElementsByName("offer"))
    const base_costs_total = Number(document.getElementById("base_costs_total").value)
    offers.forEach(offer => {
        const price = Number(offer.querySelector("[name='price'").value)
        offer.querySelector("[name='price_total']").value = (price + base_costs_total).toFixed(2)
    })
    //offer bundle
    const offer_bundle_price = Number(document.getElementById("offer_bundle_price").value)
    document.getElementById("offer_bundle_price_total").value = (offer_bundle_price + base_costs_total).toFixed(2)
}

function calculate_offer_total_on_price_change(element) {
    const price = Number(element.value)
    const base_costs_total = Number(document.getElementById("base_costs_total").value)
    let price_total = element.parentElement.parentElement.querySelector("[name='price_total'")

    price_total.value = (price + base_costs_total).toFixed(2)
}
function calculate_offer_bundle_total_on_price_change(element) {
    const price = Number(element.value)
    const base_costs_total = Number(document.getElementById("base_costs_total").value)
    let price_total = element.parentElement.parentElement.querySelector("[name='offer_bundle_price_total'")

    price_total.value = (price + base_costs_total).toFixed(2)
}

function calculate_discount(element) {
    // price with discount
    const discount = Number(element.value)
    const price = Number(document.getElementById("offer_bundle_price").value)
    const price_with_dicount = (price * (100 - discount) / 100)

    document.getElementById("offer_bundle_price_with_discount").value = price_with_dicount.toFixed(2)
    // offer bundle total
    const base_costs_total = Number(document.getElementById("base_costs_total").value)
    console.log(base_costs_total)
    document.getElementById("offer_bundle_price_total").value = (price_with_dicount + base_costs_total).toFixed(2)

}
    


let offer_data = []
function get_offer_data() {
    let customer = {
        name: document.getElementsByName("customer_name")[0].value,
        street: document.getElementsByName("customer_street")[0].value,
        street_nr: document.getElementsByName("customer_street_nr")[0].value,
        postal_code: document.getElementsByName("customer_postal_code")[0].value,
        city: document.getElementsByName("customer_city")[0].value
    }

    let project_data = {
        project_name: document.getElementsByName("project_name")[0].value,
        days: document.getElementsByName("days")[0].value,
        times: [],
        validity_period: document.getElementsByName("validity_period")[0].value
    }
    //get times
    time_rows = document.querySelectorAll("[name='times']");
    time_rows.forEach(time_row => {
        let time = {
            start: time_row.querySelector("[name='start']").value,
            end: time_row.querySelector("[name='end']").value,
            date: time_row.querySelector("[name='date']").value
        }
        project_data.times.push(time)
    })

    let base_costs = {
        rides: document.getElementsByName("rides")[0].value,
        distance: document.getElementsByName("distance")[0].value,
        price_km: document.getElementsByName("price_km")[0].value,
        staff: document.getElementsByName("staff")[0].value,
        price_day: document.getElementsByName("price_day")[0].value,
        assembly_fee: document.getElementsByName("assembly_fee")[0].value,
        travel_costs: document.getElementsByName("travel_costs")[0].value,
        staff_costs: document.getElementsByName("staff_costs")[0].value,
        base_costs_total: document.getElementsByName("base_costs_total")[0].value
    }
    let offers = []
    //get offers
    const offer_array = document.querySelectorAll("[name='offer']")
    offer_array.forEach(offer_data => {
        const offer = {
            "name": offer_data.querySelector("[name='name']").value,
            "price": Number(offer_data.querySelector("[name='price']").value).toFixed(2),
            "price_total": offer_data.querySelector("[name='price_total']").value,
            "description": offer_data.querySelector("[name='description']").textContent,
        }
        offers.push(offer)
    })

    let offer_bundle = {
        "name": document.getElementsByName("offer_bundle_name")[0].value,
        "price": Number(document.getElementsByName("offer_bundle_price")[0].value).toFixed(2),
        "price_total": Number(document.getElementsByName("offer_bundle_price_total")[0].value).toFixed(2),
        "description": document.getElementsByName("offer_bundle_description")[0].textContent,
        "discount": document.getElementsByName("discount")[0].value,
        "price_total_with_discount": Number(document.getElementsByName("offer_bundle_price_with_discount")[0].value).toFixed(2)
    }

    offer_data = {
        customer: customer,
        project_data: project_data,
        base_costs: base_costs,
        offers: offers,
        offer_bundle: offer_bundle
    }
}
