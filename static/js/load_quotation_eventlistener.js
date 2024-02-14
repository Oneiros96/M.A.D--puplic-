document.getElementById("quotation_name").addEventListener("change", function() {
    let quotation_name = document.getElementById("quotation_name")
    let quotation_id = document.getElementById("quotation_id")

    let selected_quotation = document.querySelector('#saved_quotations option[value="' + quotation_name.value + '"]')

    if (selected_quotation) {
        quotation_id.value = selected_quotation.getAttribute('data-id')
    } else {
        quotation_id.value = ""
    }
})