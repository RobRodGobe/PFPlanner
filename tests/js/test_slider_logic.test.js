/**
 * @jest-environment jsdom
 */
const { updateIncomePctKnob } = require("../../Frontend/static/js/custom_calculator.js");

test("slider label updates", () => {
  document.body.innerHTML = `
    <input id="income_pct_slider" type="range" value="25" max="25">
    <div id="income-pct-label"></div>
  `;

  const slider = document.getElementById("income_pct_slider");
  const label = document.getElementById("income-pct-label");

  slider.value = 10;

  // ✅ Call the pure function directly
  updateIncomePctKnob(slider, label);

  expect(label.textContent).toBe("10%");
});
