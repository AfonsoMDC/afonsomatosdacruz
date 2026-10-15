// Vergroting van beelden in een venster. Wordt alleen geladen op pagina's met beeldtegels.
const venster = document.querySelector("dialog");
const grootBeeld = venster.querySelector("img");
const titelVeld = venster.querySelector(".titel");
const tekstVeld = venster.querySelector(".tekst");
const tellerVeld = venster.querySelector(".teller");

let beelden = [];
let huidig = 0;

function toonBeeld() {
  grootBeeld.src = beelden[huidig].src;
  grootBeeld.alt = beelden[huidig].alt;
  tellerVeld.textContent = beelden.length > 1 ? `${huidig + 1} / ${beelden.length}` : "";
}

function stap(richting) {
  huidig = (huidig + richting + beelden.length) % beelden.length;
  toonBeeld();
}

document.querySelectorAll("[data-beelden]").forEach((tegel) => {
  tegel.addEventListener("click", (gebeurtenis) => {
    gebeurtenis.preventDefault();
    beelden = JSON.parse(tegel.dataset.beelden);
    huidig = Number(tegel.dataset.start || 0);
    titelVeld.textContent = tegel.dataset.titel || "";
    tekstVeld.textContent = tegel.dataset.tekst || "";
    venster.classList.toggle("enkel", beelden.length === 1);
    toonBeeld();
    venster.showModal();
  });
});

venster.querySelector(".sluiten").addEventListener("click", () => venster.close());
venster.querySelector(".vorige").addEventListener("click", () => stap(-1));
venster.querySelector(".volgende").addEventListener("click", () => stap(1));
venster.addEventListener("keydown", (gebeurtenis) => {
  if (gebeurtenis.key === "ArrowLeft") stap(-1);
  if (gebeurtenis.key === "ArrowRight") stap(1);
});
