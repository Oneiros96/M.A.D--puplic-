function delete_offer(element) {
    parent = get_nth_parent(element, 2)
    parent.remove()
}