(function () {
  const flows = {
    booking: {
      title: "Objednanie pacienta",
      lines: [
        ["Pacient", "Dobrý deň, chcem sa objednať na vyšetrenie."],
        ["AI Recepcia", "Rozumiem. Povedzte mi prosím meno a dátum narodenia."],
        ["Pacient", "Ján Novák, 12. 3. 1988."],
        ["AI Recepcia", "Ďakujem. Aký je dôvod vyšetrenia?"],
        ["Pacient", "Bolesť zuba."],
        ["AI Recepcia", "Môžem vám ponúknuť zajtra 10:30 alebo 14:10. Ktorý termín vyhovuje?"],
        ["Pacient", "10:30."],
        ["AI Recepcia", "Hotovo. Termín som zapísala do kalendára a posielam potvrdenie e-mailom. Prajete si ešte niečo?"]
      ]
    },
    change: {
      title: "Zmena termínu",
      lines: [
        ["Pacient", "Potrebujem zmeniť termín na budúci týždeň."],
        ["AI Recepcia", "Jasné. Povedzte mi prosím meno a pôvodný dátum termínu."],
        ["Pacient", "Ján Novák, utorok 11:00."],
        ["AI Recepcia", "Našla som váš termín. Môžem ponúknuť stredu 9:40 alebo štvrtok 16:20. Ktorý vyhovuje?"],
        ["Pacient", "Štvrtok 16:20."],
        ["AI Recepcia", "Potvrdené. Termín som presunula a posielam nové potvrdenie."]
      ]
    },
    cancel: {
      title: "Zrušenie termínu",
      lines: [
        ["Pacient", "Chcem zrušiť termín."],
        ["AI Recepcia", "Rozumiem. Povedzte mi prosím meno a dátum termínu."],
        ["Pacient", "Ján Novák, zajtra 10:30."],
        ["AI Recepcia", "Termín som zrušila. Ak chcete, môžem hneď ponúknuť náhradný termín."]
      ]
    },
    faq: {
      title: "FAQ (ordinácia)",
      lines: [
        ["Pacient", "Kedy máte otvorené a kde vás nájdem?"],
        ["AI Recepcia", "Ordinačné hodiny sú Po–Pi 8:00–16:00. Adresa: podľa webu ambulancie. Chcete sa aj objednať?"],
        ["Pacient", "Áno."],
        ["AI Recepcia", "Super, poďme na to. Povedzte mi meno a dátum narodenia…"]
      ]
    },
    urgent: {
      title: "Urgentná situácia (fallback)",
      lines: [
        ["Pacient", "Mám silné krvácanie po zákroku."],
        ["AI Recepcia", "Rozumiem. Toto je urgentné. Okamžite vás prepájam na personál ambulancie. Zostaňte prosím na linke."]
      ]
    }
  };

  function render(flowKey) {
    const flow = flows[flowKey] || flows.booking;
    const titleEl = document.getElementById("demo_title");
    const outEl = document.getElementById("demo_out");
    if (!outEl) return;
    if (titleEl) titleEl.textContent = flow.title;

    outEl.innerHTML = "";
    for (const [who, text] of flow.lines) {
      const row = document.createElement("div");
      row.className = "row";
      const badge = document.createElement("div");
      badge.className = "who";
      badge.textContent = who;
      const msg = document.createElement("div");
      msg.className = "msg";
      msg.textContent = text;
      row.appendChild(badge);
      row.appendChild(msg);
      outEl.appendChild(row);
    }
  }

  function bind() {
    const buttons = document.querySelectorAll("[data-flow]");
    for (const b of buttons) {
      b.addEventListener("click", () => {
        for (const x of buttons) x.classList.remove("active");
        b.classList.add("active");
        render(b.getAttribute("data-flow"));
      });
    }
    const first = document.querySelector("[data-flow].active") || document.querySelector("[data-flow]");
    if (first) render(first.getAttribute("data-flow"));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();

