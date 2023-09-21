function deRequire(elClass) {
  el = document.getElementsByClassName(elClass);

  var atLeastOneChecked = false; //at least one cb is checked
  for (i = 0; i < el.length; i++) {
    if (el[i].checked === true) {
      atLeastOneChecked = true;
    }
  }

  if (atLeastOneChecked === true) {
    for (i = 0; i < el.length; i++) {
      el[i].required = false;
    }
  } else {
    for (i = 0; i < el.length; i++) {
      el[i].required = true;
    }
  }
}

function toggle(source, elClass) {
  checkboxes = document.getElementsByClassName(elClass);
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}