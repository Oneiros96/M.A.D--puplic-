let project_groups = document.querySelectorAll('.project_group')
eventlistener_project_groups()
//project groups
document.addEventListener('DOMContentLoaded', function() {
    var add_button = document.getElementById('add_group');
    add_button.addEventListener('click', function() {
        var parent_div = add_button.parentElement; // Get the parent div
        var new_row = document.createElement('div');
        new_row.className = 'row';
        new_row.innerHTML = '<table class="mb-3 project-table">'+
                                '<thead>'+
                                    '<tr>'+
                                        '<th class="col">' +
                                            '<input class="text-center form-control th" type="text" name="project_group" value="">'+
                                        '</th>' +
                                        '<th class="col-1">' +
                                            '<button class="btn btn-dark delete_project_day_tt" onclick="delete_project_group(this)">' +
                                                '<img src="/static/images/trash_can.png" width="25" height="25" alt="new-group" >' +
                                            '</button>' +
                                        '</th>' +
                                    '</tr>'+
                                '</thead>'+
                                '<tbody class="mb-1 project_group">'+
                                    '<tr>' +
                                        '<td> '+
                                        '<p>\n</p>'
                                        '</td>' +
                                    '</tr>'
                                '</tbody>'+
                            '</table>';
        
        tippy(new_row.querySelector(".delete_project_day_tt"), {
                content: "Projekttag löschen",
                arrow: true,
                placement: "bottom",
        })

        parent_div.parentNode.insertBefore(new_row, parent_div);
        project_groups = document.querySelectorAll('.project_group')
        eventlistener_project_groups()
  });
});

function delete_project_group(element) {
    parent = get_nth_parent(element, 5)
    parent.remove()
    project_groups = document.querySelectorAll('.project_group')
    eventlistener_project_groups()
}


// drop offers
let is_appending = false
function eventlistener_project_groups(){
    project_groups.forEach(project_group => {
        project_group.addEventListener("dragover", e => {
            e.preventDefault()
            const draggable = document.querySelector(".dragging")
            if (!is_appending && draggable) {
                is_appending = true
                const copy = draggable.cloneNode(true)
                copy.classList.remove("dragging")
                copy.innerHTML +=   '<td>' +
                                        '<button class="btn btn-dark delete_offer_tt" onclick="delete_offer(this)">' +
                                            '<img src="/static/images/trash_can.png" width="25" height="25" alt="new-group" >' +
                                        '</button>' +
                                    '</td>'
                
                tippy(copy.querySelector(".delete_offer_tt"), {
                    content: "Dienstleistung entfernen",
                    arrow: true,
                    placement: "bottom",
                })
                
                project_group.appendChild(copy);
                
                //timer after element is added, to avoid adding it mutiple times unwanted
                setTimeout(() => {
                    is_appending = false
                }, 1500);
            }
        })
    })
}
//get user data & do stuff with it
let offer_data = {}
function get_offer_data() {
    //consturcts dict's with userdata and appends them to the user_data variable
    let customer = {
        name: document.getElementsByName("customer_name")[0].value,
        street: document.getElementsByName("customer_street")[0].value,
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
        assembly_fee: document.getElementsByName("assembly_fee")[0].value
    }
    
    let projects = {}
    let project_tables = document.querySelectorAll(".project-table")
    project_tables.forEach(function(table, index){
        let project_group = table.querySelector(".th").value
        
        let offer_list = []
        let rows = table.querySelectorAll("tbody tr")

        if (rows.length > 1) {
            rows = Array.from(rows)
            rows.shift()
            rows.forEach(function(row){
                let tds = row.querySelectorAll("td")
                let project_id = tds[0].textContent
                let name = tds[1].textContent
    
                let offer = {
                    "id": project_id,
                    "name": name
                }
                offer_list.push(offer)
            })
            projects[project_group] = offer_list  
        }
    })

    offer_data = {
        customer: customer,
        project_data: project_data,
        base_costs: base_costs,
        projects: projects
    }
}

function save_quotation() {
    let data = {}
    data["data"] = offer_data
    data["quotation_name"] = document.getElementById("quotation_name").value
    data["quotation_id"] = document.getElementById("quotation_id").value
    data = JSON.stringify(data)

    fetch("/simplex/save_quotation", {
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

// tooltips
tippy(".add_project_day_tt", {
    content: "Projekttag hinzufügen",
    arrow: true,
    placement: "bottom",
})
delete_offers = document.querySelectorAll(".delete_offer_tt")
delete_offers.forEach(element => {
    tippy(element, {
        content: "Dienstleistung entfernen",
        arrow: true,
        placement: "bottom",
    })
})

delete_project_days = document.querySelectorAll(".delete_project_day_tt")
delete_project_days.forEach(element => {
    tippy(element, {
        content: "Projekttag entfernen",
        arrow: true,
        placement: "bottom",
    })
})