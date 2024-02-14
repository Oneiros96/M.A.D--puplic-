function spawn_despawn_times(days) {
    days = days.value;
    times = document.getElementsByName("times");

    if (days > times.length) {
        const last_times_element = times[times.length - 1];
        const times_container = last_times_element.parentNode;

        for (let i = times.length; i < days; i++) {
            const new_times_element = last_times_element.cloneNode(true);
            times_container.appendChild(new_times_element);
        }
    } else if (days < times.length && days > 0) {
        const times_container = times[0].parentNode;

        for (let i = times.length - 1; i >= days; i--) {
            times_container.removeChild(times[i]);
        }
    }
}
