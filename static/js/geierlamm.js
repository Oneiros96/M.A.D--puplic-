// drop offers
let is_appending = false
function drop(event) {
    event.preventDefault();
    const draggable = document.querySelector(".dragging");
    const target = event.target;
    const tbody = target.closest("tbody");

    if (!is_appending && draggable && tbody) {
        is_appending = true;
        const copy = draggable.cloneNode(true);
        copy.classList.remove("dragging");
        copy.innerHTML += '<td>' +
                            '<select class="form-select text-center" name="vat_rate">' +
                                '<option>0</option>' +
                                '<option selected>7</option>' +
                                '<option>19</option>' +
                            '</select>' +
                        '</td>' +
                        '<td>'+
                            '% MwSt.'+
                        '</td>' +
                        '<td>' +
                            '<button class="btn btn-dark delete_offer_tt" onclick="delete_offer(this)">' +
                                '<img src="/static/images/trash_can.png" width="25" height="25" alt="new-group" >' +
                            '</button>' +
                        '</td>';

        tippy(copy.querySelector(".delete_offer_tt"), {
            content: "Dienstleistung entfernen",
            arrow: true,
            placement: "bottom",
        })
        tbody.appendChild(copy);

        setTimeout(() => {
            is_appending = false;
        }, 1500);
    }
}
document.getElementById("offers").addEventListener("dragover", (event) => drop(event))
document.getElementById("offer_bundle").addEventListener("dragover", (event) => drop(event))


function save_geierlamm_quotation() {
    let data = {}
    data["data"] = offer_data
    data["quotation_name"] = document.getElementById("quotation_name").value
    data["quotation_id"] = document.getElementById("quotation_id").value
    data = JSON.stringify(data)

    fetch("/geierlamm/save_quotation", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json' 
        },
        body: data
    })
    .catch(error => {
        console.error('Error:', error)
    })
}

//offer data
let offer_data = {}
function get_offer_data() {
    let customer = {
        name: document.getElementsByName("customer_name")[0].value,
        street: document.getElementsByName("customer_street")[0].value,
        street_nr: document.getElementsByName("street_nr")[0].value,
        postal_code: document.getElementsByName("postal_code")[0].value,
        city: document.getElementsByName("city")[0].value
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
            start: time_row.querySelector("[name='start_time']").value,
            end: time_row.querySelector("[name='end_time']").value,
            date: time_row.querySelector("[name='date']").value
        }
        project_data.times.push(time)
    })

    let base_costs = {
        rides: document.getElementsByName("rides")[0].value,
        distance: document.getElementsByName("distance")[0].value,
        price_km: document.getElementsByName("price_km")[0].value,
        assembly_fee: document.getElementsByName("assembly_fee")[0].value,
        vat_rate: document.getElementsByName("base_cost_vat_rate")[0].value
    }

    
    let offers = []
    //get offers
    const offers_table = document.getElementById("offers")
    let offer_rows = offers_table.querySelectorAll("tr")
    if (offer_rows.length > 1) {
        offer_rows = Array.from(offer_rows)
        offer_rows.shift()
        offer_rows.forEach(function (row) {
            let tds = row.querySelectorAll("td")
            let offer_id = tds[0].textContent
            let name = tds[1].textContent
            let vat_rate = row.querySelector("[name='vat_rate'").value

            let offer = {
                "id": offer_id,
                "name": name,
                "vat_rate": vat_rate

            }
            offers.push(offer)
        }) 
    }

    let offer_bundle = []
    //get offer_bundle
    const offer_bundle_table = document.getElementById("offer_bundle")
    let offer_bundle_rows = offer_bundle_table.querySelectorAll("tr")
    if (offer_bundle_rows.length > 1) {
        offer_bundle_rows = Array.from(offer_bundle_rows)
        offer_bundle_rows.shift()
        offer_bundle_rows.forEach(function (row) {
            let tds = row.querySelectorAll("td")
            let offer_id = tds[0].textContent
            let name = tds[1].textContent
            let vat_rate = row.querySelector("[name='vat_rate'").value

            let offer = {
                "id": offer_id,
                "name": name,
                "vat_rate": vat_rate
            }
            offer_bundle.push(offer)
        }) 
    }

    offer_data = {
        customer: customer,
        project_data: project_data,
        base_costs: base_costs,
        offers: offers,
        offer_bundle: offer_bundle
    }
}

trashcans = document.querySelectorAll(".delete_offer_tt")
trashcans.forEach(element => {
    tippy(element, {
        content: "Dienstleistung entfernen",
        arrow: true,
        placement: "bottom",
    })
})
