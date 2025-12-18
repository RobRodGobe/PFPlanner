(function() {
    // --- DOM ELEMENTS ---
    const modeRadios = document.querySelectorAll('input[name="dp_mode"]');
    const slider = document.getElementById('down_payment_slider');
    const maxInput = document.getElementById('down_payment_max');
    const maxRow = document.getElementById('dp-max-row');

    const minLabel = document.getElementById('dp-min-label');
    const maxLabel = document.getElementById('dp-max-label');

    const sliderLabel = document.getElementById('dp-slider-label');

    const incomePctSlider = document.getElementById('income_pct_slider');
    const incomePctLabel = document.getElementById('income-pct-label');

    const form = document.getElementById('custom-form');
    const resultsContainer = document.getElementById('custom-results');

    // ✅ If running in Jest or partial DOM, bail out safely
    if (!slider || !maxInput || !maxRow || !minLabel || !maxLabel || !sliderLabel || !incomePctSlider || !incomePctLabel || !form || !resultsContainer) {
        if (typeof module !== "undefined") {
            module.exports = {
                updateIncomePctKnob: function(sliderEl, labelEl) {
                    const val = parseFloat(sliderEl.value || 0);
                    labelEl.textContent = val + "%";
                    const percent = val / 25;
                    labelEl.style.left = `calc(${percent * 100}% - 16px)`;
                }
            };
        }
        return;
    }

    // --- STATE ---
    let resultsVisible = false;

    // --- HELPERS ---
    function formatCurrency(value) {
        return '$' + Number(value).toLocaleString();
    }

    function getMode() {
        return document.querySelector('input[name="dp_mode"]:checked')?.value || 'dollar';
    }

    // --- DOWN PAYMENT SLIDER LOGIC ---
    function updateDpLabels() {
        const mode = getMode();
        const maxVal = parseFloat(maxInput.value || 0) || 0;
        const sliderVal = parseFloat(slider.value || 0) || 0;

        // Show/hide Max $ row
        maxRow.classList.toggle("hidden", mode === "percent");

        if (mode === 'percent') {
            minLabel.textContent = '0%';
            maxLabel.textContent = '100%';
            sliderLabel.textContent = sliderVal.toFixed(0) + '%';
        } else {
            minLabel.textContent = '$0';
            maxLabel.textContent = formatCurrency(maxVal);
            const currentDollar = maxVal * (sliderVal / 100);
            sliderLabel.textContent = Number(currentDollar).toLocaleString();
        }

        const percent = sliderVal / 100;
        sliderLabel.style.left = `calc(${percent * 100}% - 16px)`;
    }

    // --- INCOME % SLIDER LOGIC ---
    function updateIncomePctKnob() {
        const val = parseFloat(incomePctSlider.value || 0);
        incomePctLabel.textContent = val + "%";

        const percent = val / 25;
        incomePctLabel.style.left = `calc(${percent * 100}% - 16px)`;
    }

    // ✅ PURE TEST VERSION (Jest)
    function updateIncomePctKnobForTest(sliderEl, labelEl) {
        const val = parseFloat(sliderEl.value || 0);
        labelEl.textContent = val + "%";
        const percent = val / 25;
        labelEl.style.left = `calc(${percent * 100}% - 16px)`;
    }

    // --- EVENT BINDINGS ---
    modeRadios.forEach(r => r.addEventListener('change', updateDpLabels));
    slider.addEventListener('input', updateDpLabels);
    maxInput.addEventListener('input', updateDpLabels);
    incomePctSlider.addEventListener('input', updateIncomePctKnob);

    // --- INITIALIZE POSITIONS (no blip because HTML now sets initial left) ---
    updateDpLabels();
    updateIncomePctKnob();

    // --- AUTO-UPDATE LOGIC (RESTORED EXACTLY AS BEFORE) ---
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        if (evt.detail.target === resultsContainer) {
            resultsVisible = true;   // ✅ Only after first calculation
        }
    });

    form.addEventListener('input', function() {
        if (!resultsVisible) return;  // ✅ Do NOT auto-update before first Calculate
        if (typeof htmx !== "undefined") {
            htmx.trigger(form, 'submit');
        }
    });

    // ✅ EXPORT FOR JEST
    if (typeof module !== "undefined") {
        module.exports = {
            updateIncomePctKnob: updateIncomePctKnobForTest
        };
    }
})();
