const search_element = document.querySelectorAll(".search")

function search(e) {
    search_input = e.value.toLocaleLowerCase()

    search_element.forEach(element => {
        const element_name = element.querySelector("[name='name']").textContent.toLocaleLowerCase()
        const visible = element_name.includes(search_input)

        element.classList.toggle("hide", !visible)
    })
}