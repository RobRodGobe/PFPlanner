/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");

const script = fs.readFileSync(
  path.resolve(__dirname, "../../Frontend/static/js/house_affordability/custom_calculator.js"),
  "utf8"
);

test("down payment slider updates correctly in dollar mode", () => {
  document.body.innerHTML = `
    <form id="custom-form"></form>
    <div id="custom-results"></div>

    <input type="radio" name="dp_mode" value="percent">
    <input type="radio" name="dp_mode" value="dollar" checked>

    <input id="down_payment_slider" type="range" value="50">
    <input id="down_payment_max" value="100000">

    <div id="dp-max-row"></div>
    <span id="dp-min-label"></span>
    <span id="dp-max-label"></span>
    <div id="dp-slider-label"></div>

    <input id="income_pct_slider" value="25">
    <div id="income-pct-label"></div>
  `;

  eval(script);

  const sliderLabel = document.getElementById("dp-slider-label");
  const minLabel = document.getElementById("dp-min-label");
  const maxLabel = document.getElementById("dp-max-label");

  expect(minLabel.textContent).toBe("$0");
  expect(maxLabel.textContent).toBe("$100,000");
  expect(sliderLabel.textContent).toBe("50,000");
});
