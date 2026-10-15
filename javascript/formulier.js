// Verstuurt het contactformulier naar Formspree. Wordt alleen geladen op de startpagina.

const formulier = document.querySelector("#contact form");
const status = document.querySelector("#contact .status");

formulier.addEventListener("submit", async (gebeurtenis) => {
  gebeurtenis.preventDefault();
  status.textContent = formulier.dataset.bezig;
  const antwoord = await fetch(formulier.action, {
    method: "POST",
    body: new FormData(formulier),
    headers: { Accept: "application/json" },
  });
  if (antwoord.ok) {
    formulier.reset();
    status.textContent = formulier.dataset.gelukt;
  } else {
    status.textContent = formulier.dataset.mislukt;
  }
});
