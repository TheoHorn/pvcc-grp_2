parent = document.querySelector("#orders")
document.querySelector("#orders_sort").onchange = (ev) => {
    element = ev.target
    nodes = parent.querySelectorAll(".order")
    array = []
    nodes.forEach((node) => {
      array.push(node)
      node.remove()
    })
    if (element.value.toLowerCase() == "user") {sort_by_user(array)}
    else if (element.value.toLowerCase() == "date") {sort_by_date(array)}
    array.forEach((node) => {
      parent.appendChild(node)
    });
}

function sort_by_user(array) {
    array.sort((a, b) => {
        return a.querySelector(".username").innerHTML.localeCompare(b.querySelector(".username").innerHTML);
    });
}

function sort_by_date(data){
    data.sort((b, a) => {
      return new Date(a.querySelector(".date").innerHTML) - new Date(b.querySelector(".date").innerHTML);
    });
  }