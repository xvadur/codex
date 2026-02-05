(function () {
  function fmtEur(n) {
    try {
      return new Intl.NumberFormat("sk-SK", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n);
    } catch {
      return `EUR ${Math.round(n)}`;
    }
  }

  function clamp(v, min, max) {
    if (Number.isNaN(v)) return min;
    return Math.min(max, Math.max(min, v));
  }

  function readNum(id, fallback) {
    const el = document.getElementById(id);
    if (!el) return fallback;
    const v = Number(String(el.value || "").replace(",", "."));
    return Number.isFinite(v) ? v : fallback;
  }

  function update() {
    const calls = clamp(readNum("calc_calls", 1200), 0, 20000);
    const missedPct = clamp(readNum("calc_missed", 10), 0, 100);
    const convPct = clamp(readNum("calc_conv", 30), 0, 100);
    const value = clamp(readNum("calc_value", 100), 0, 10000);
    const fee = clamp(readNum("calc_fee", 500), 0, 20000);

    const missed = calls * (missedPct / 100);
    const converted = missed * (convPct / 100);
    const loss = converted * value;
    const roi = fee > 0 ? (loss / fee) : 0;

    const lossEl = document.getElementById("calc_loss");
    const roiEl = document.getElementById("calc_roi");
    if (lossEl) lossEl.textContent = fmtEur(loss);
    if (roiEl) roiEl.textContent = roi ? `${roi.toFixed(1)}x` : "—";

    const noteEl = document.getElementById("calc_note");
    if (noteEl) {
      noteEl.textContent =
        `Odhad: ${Math.round(missed)} zmeškaných hovorov → ${Math.round(converted)} objednávok. ` +
        `Ak je mesačný fee ${fmtEur(fee)}, návratnosť vychádza približne ${roi.toFixed(1)}x.`;
    }
  }

  function bind() {
    const ids = ["calc_calls", "calc_missed", "calc_conv", "calc_value", "calc_fee"];
    for (const id of ids) {
      const el = document.getElementById(id);
      if (!el) continue;
      el.addEventListener("input", update);
    }
    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();

