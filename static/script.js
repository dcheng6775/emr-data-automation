function changetotext(x) { 
    if (x != 1) {
        document.querySelector(`.js-input${x}`).innerHTML = 
        `<input type="text" name="text${x}">
         <button type="button" onclick="changetofile(${x})">I want to add a file instead. </button>`;}
    else {
        document.querySelector(`.js-input${x}`).innerHTML = 
        `<input type="text" name="text${x}" required>
        <button type="button" onclick="changetofile(${x})">I want to add a file instead. </button>`;}
      }

function changetofile(x) {
    if (x != 1) {
        document.querySelector(`.js-input${x}`).innerHTML = 
        `<input type="file" name="file${x}">
         <button type="button" onclick="changetotext(${x})">I want to add a text instead. </button>`;}
    else {
        document.querySelector(`.js-input${x}`).innerHTML = 
        `<input type="file" name="file${x}" required>
         <button type="button" onclick="changetotext(${x})">I want to add a text instead. </button>`;}
      }
