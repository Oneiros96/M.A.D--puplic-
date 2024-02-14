window.onload = function() {
    let description_elements = document.querySelectorAll("textarea");
    for (let element of description_elements) {
        adjust_textarea_size(element);
    }
};

function caluculate_total_price_pp() {
    const price_total = Number(document.getElementById("total_cost").value)
    const participants = Number(document.getElementById("participants").value)

    document.getElementById("total_cost_pp").value = (price_total / participants).toFixed(2)
}

function calculate_total_price() {
    const project_days = document.querySelectorAll("[name='project_day']")
    let total_price = Number(document.getElementById("base_costs_total").value)
    
    project_days.forEach(project_day => {
        total_price += Number(project_day.querySelector("[name='project_cost'").value)
    })

    document.getElementById("total_cost").value = total_price.toFixed(2)
    caluculate_total_price_pp()
}

function calculate_base_costs_vat_and_netto() {
    const base_costs_total = Number(document.getElementById("base_costs_total").value)
    let vat = (base_costs_total * 7 / 100).toFixed(2)
    let base_costs_total_netto = base_costs_total - vat

    document.getElementById("base_costs_total_netto").value = base_costs_total_netto
    document.getElementById("vat").value = vat
}

function calculate_projects_and_project_day_total() {
    const project_days = document.querySelectorAll("[name='project_day']")
    const participants = Number(document.getElementById("participants").value)

    project_days.forEach(project_day => {
        const projects = project_day.querySelectorAll("[name='offer']")
        let project_day_price_pp = 0
        
        projects.forEach(project => {
            const price = Number(project.querySelector("[name='price_brutto'").value)
            let price_total = (price * participants).toFixed(2) 
            project.querySelector("[name='price_total']").value = price_total
            project_day_price_pp += price
        })
        project_day.querySelector("[name='project_cost_pp'").value = project_day_price_pp
        project_day.querySelector("[name='project_cost'").value = (project_day_price_pp * participants).toFixed(2)
    })
    calculate_total_price()
}

function calculate_base_cost_pp() {
    const participants = Number(document.getElementById("participants").value)
    const base_cost_total = Number(document.getElementById("base_costs_total").value)

    document.getElementById("base_cost_total_pp").value = (base_cost_total / participants).toFixed(2)
}

function calculate_base_cost() {
    //reisekosten+personalkosten+assembly fee
    const travel_costs = Number(document.getElementById("travel_costs").value)
    const staff_cost = Number(document.getElementById("staff_costs").value)
    const assembly = Number(document.getElementById("assembly_fee").value)

    document.getElementById("base_costs_total").value = (travel_costs + staff_cost + assembly).toFixed(2)
    calculate_base_costs_vat_and_netto()
    calculate_base_cost_pp()
    calculate_total_price()
}

function calculate_travel_costs() {
    const rides = Number(document.getElementById("rides").value)
    const distance = Number(document.getElementById("distance").value)
    const price_km = Number(document.getElementById("price_km").value)

    document.getElementById("travel_costs").value = (rides * distance * price_km).toFixed(2)
    calculate_base_cost()
}

function calculate_staff_costs() {
    const staff = Number(document.getElementById("staff").value)
    const days = Number(document.getElementById("days").value)
    const price_day = Number(document.getElementById("price_day").value)

    document.getElementById("staff_costs").value = (staff * days * price_day).toFixed(2)
    calculate_base_cost()
}

function calculate_offer_total_on_pp_change(element) {
    const price_pp = Number(element.value)
    const offer = element.parentElement.parentElement
    const participants = Number(document.getElementById("participants").value)

    offer.querySelector("[name='price_total']").value = (price_pp * participants).toFixed(2)
    calculate_projects_and_project_day_total()

}

let offer_data = {}
function get_offer_data() {
    let customer = {
        name: document.getElementsByName("customer_name")[0].value,
        street: document.getElementsByName("street")[0].value,
        street_nr: document.getElementsByName("street_nr")[0].value,
        postal_code: document.getElementsByName("postal_code")[0].value,
        city: document.getElementsByName("city")[0].value
    }

    let project_data = {
        days: document.getElementsByName("days")[0].value,
        participants: document.getElementsByName("participants")[0].value,
        project_name: document.getElementsByName("project_name")[0].value,
        project_theme: document.getElementsByName("project_theme")[0].value,
        customer_staff: document.getElementsByName("customer_staff")[0].value,
        validity_period: document.getElementsByName("validity_period")[0].value
    }
    let base_costs = {
        rides: document.getElementsByName("rides")[0].value,
        distance: document.getElementsByName("distance")[0].value,
        price_km: document.getElementsByName("price_km")[0].value,
        staff: document.getElementsByName("staff")[0].value,
        price_day: document.getElementsByName("price_day")[0].value,
        assembly_fee: document.getElementsByName("assembly_fee")[0].value,
        vat: document.getElementsByName("vat")[0].value,
        total_netto: document.getElementsByName("total_netto")[0].value,
        total_brutto: document.getElementsByName("base_costs_total")[0].value,
        per_participant: document.getElementsByName("per_participant")[0].value,
        staff_cost: document.getElementsByName("staff_costs")[0].value,
        travel_costs: document.getElementsByName("travel_costs")[0].value
    }

    let project_days = []
    const project_days_data = document.querySelectorAll("[name='project_day']")
    project_days_data.forEach(project_day_data => {
        let project_day = {
            name: project_day_data.querySelector("[name='project_name']").value,
            cost: Number(project_day_data.querySelector("[name='project_cost']").value).toFixed(2),
            cost_pp: Number(project_day_data.querySelector("[name='project_cost_pp']").value).toFixed(2),
            offers: []
        }
        const offers_data = project_day_data.querySelectorAll("[name='offer']")
        offers_data.forEach(offer_data => {
            let offer = {
                name: offer_data.querySelector("[name='name']").value,
                description: offer_data.querySelector("[name='description']").value,
                price_brutto: Number(offer_data.querySelector("[name='price_brutto']").value).toFixed(2),
                price_total: Number(offer_data.querySelector("[name='price_total']").value).toFixed(2)
            }
            project_day.offers.push(offer)
        })
        project_days.push(project_day)
    })

    offer_data = {
        customer: customer,
        project_data: project_data,
        base_costs: base_costs,
        project_days: project_days,
        total_cost: Number(document.getElementById("total_cost").value).toFixed(2),
        total_cost_pp: Number(document.getElementById("total_cost_pp").value).toFixed(2)
    }
}

