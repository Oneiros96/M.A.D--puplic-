function get_nth_parent(element, n) {
    let current_element = element;
    for (let i = 0; i < n; i++) {
        current_element = current_element.parentElement;
        if (!current_element) {
            return null; // Return null if there are not enough parents.
        }
    }
    return current_element;
}