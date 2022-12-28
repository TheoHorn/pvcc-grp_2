/** Change the display value for the cost */
document.querySelectorAll(".buy_quantity").forEach((element) => {
  element.onchange = () => {
    let quantity = parseFloat(element.value);
    let price = parseFloat(element.parentNode.parentNode.querySelector(".price").innerHTML);
    let total = (quantity * price).toFixed(2);
    element.parentNode.querySelector(".cost_float").innerHTML = total; 
  }  
})