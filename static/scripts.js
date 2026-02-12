function setLocked(state) {
  document.querySelectorAll("button, input, select, textarea")
    .forEach(el => el.readonly = state);
}

document.addEventListener("submit", async e => {
  const form = e.target;

  if (form.matches('[data-noredirect]')) {
    console.log("yey");
    e.preventDefault();
    setLocked(true);

    await fetch(form.action, {
      method: "POST",
      body: new FormData(form)
    });
    
    if (!form.matches('[data-norefresh]')) {
      location.reload();
    }
  }
});
