//Bean name script
function getName(el){
    let row = el.closest('tr');
    let index = row.rowIndex;
    let name = row.cells[1].innerHTML;
    return name;
    };
// When the DOM content is loaded, assign the value of the name of the bean in each row for the hidden inputs.
document.addEventListener('DOMContentLoaded', function() {
beanNameList = document.getElementsByClassName('BeanName');
for (let i = 0; i < beanNameList.length; i++) {
    let el_beanName = beanNameList[i];
    let name = getName(el_beanName);
    // Assign the name value to the input elements with class name beanName and detailedBeanName in that row
    el_beanName.value = name;
}
});    
