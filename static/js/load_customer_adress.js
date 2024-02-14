document.getElementById("customer_name").addEventListener("change", function(){
    let customer_name_input = this.value
    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                customer_data = JSON.parse(request.responseText)
                if (customer_data){
                    if (customer_data["street"]) {
                        document.getElementById("customer_street").value = customer_data["street"]
                    }
                    if (customer_data["street_nr"]) {
                        document.getElementById("street_nr").value = customer_data["street_nr"]
                    }
                    if (customer_data["postal_code"]) {
                        document.getElementById("postal_code").value = customer_data["postal_code"]
                    }
                    if (customer_data["city"]) {
                        document.getElementById("city").value = customer_data["city"]
                    }
                }
            } else {
            console.error('Error:', request.status, request.statusText);
            }
        }
    }

    request.open("GET", "/customer_data?customer_name_input=" + encodeURIComponent(customer_name_input), true)
    request.send()
})