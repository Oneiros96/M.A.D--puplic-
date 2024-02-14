const draggables = document.querySelectorAll('.draggable')
draggables.forEach(draggable => {
    draggable.addEventListener("dragstart", () => {
        draggable.classList.add("dragging")
    })
    
    draggable.addEventListener("dragend", () => {
        draggable.classList.remove("dragging")
    })
    
});