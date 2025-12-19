document.addEventListener("change", function (e) {
    if (e.target.name === "mode") {
        const adv = document.getElementById("advanced-fields");
        if (!adv) return; // ✅ prevents null.classList errors

        if (e.target.value === "advanced") {
            adv.classList.remove("hidden");
        } else {
            adv.classList.add("hidden");
        }
    }
});
