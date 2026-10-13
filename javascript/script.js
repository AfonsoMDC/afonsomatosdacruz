/* ================================================================
   SCRIPT.JS — twee kleine dingen:
   1. Elementen met class "onthul" verschijnen zachtjes bij scrollen.
   2. Elke link met class "vergroot" opent het beeld groot in een venster.
   Zonder JavaScript werkt de site gewoon: alles is zichtbaar en de
   links openen het grote beeld in een nieuw tabblad.
   ================================================================ */

/* ---------- 1. Onthullen bij scrollen ---------- */
const onthulElementen = document.querySelectorAll(".onthul");
const wilMinderBeweging = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if ("IntersectionObserver" in window && !wilMinderBeweging) {
  const waarnemer = new IntersectionObserver((items) => {
    items.forEach((item) => {
      if (!item.isIntersecting) return;
      item.target.classList.add("zichtbaar");
      waarnemer.unobserve(item.target);
    });
  }, { threshold: 0.1, rootMargin: "0px 0px -5% 0px" });
  onthulElementen.forEach((element) => waarnemer.observe(element));
} else {
  onthulElementen.forEach((element) => element.classList.add("zichtbaar"));
}

/* ---------- 2. Beeldvenster (lightbox) ---------- */
const venster = document.querySelector(".beeldvenster");

if (venster) {
  const groteFoto = venster.querySelector("img");
  const bijschrift = venster.querySelector(".beeldvenster-bijschrift");
  const teller = venster.querySelector(".beeldvenster-teller");
  const alleLinks = [...document.querySelectorAll("a.vergroot")];
  let nummer = 0;

  function toonBeeld() {
    const link = alleLinks[nummer];
    groteFoto.src = link.href;
    groteFoto.alt = link.querySelector("img").alt;
    bijschrift.textContent = groteFoto.alt;
    teller.textContent = (nummer + 1) + " / " + alleLinks.length;
  }

  function stap(richting) {
    nummer = (nummer + richting + alleLinks.length) % alleLinks.length;
    toonBeeld();
  }

  alleLinks.forEach((link, index) => {
    link.addEventListener("click", (gebeurtenis) => {
      gebeurtenis.preventDefault();
      nummer = index;
      toonBeeld();
      venster.showModal();
    });
  });

  venster.querySelector(".beeldvenster-sluiten").addEventListener("click", () => venster.close());
  venster.querySelector(".beeldvenster-vorige").addEventListener("click", () => stap(-1));
  venster.querySelector(".beeldvenster-volgende").addEventListener("click", () => stap(1));

  // Klikken naast het beeld sluit het venster
  venster.addEventListener("click", (gebeurtenis) => {
    if (gebeurtenis.target === venster || gebeurtenis.target.classList.contains("beeldvenster-beeld")) venster.close();
  });

  // Pijltjestoetsen bladeren (Escape sluit vanzelf)
  venster.addEventListener("keydown", (gebeurtenis) => {
    if (gebeurtenis.key === "ArrowLeft") stap(-1);
    if (gebeurtenis.key === "ArrowRight") stap(1);
  });
}
