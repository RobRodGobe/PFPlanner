/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");

// ✅ Mock HTMX so auto-update works in Jest
global.htmx = {
  trigger: (el, eventName) => {
    el.dispatchEvent(new Event(eventName));
  }
};

const script = fs.readFileSync(
  path.resolve(__dirname, "../../Frontend/static/js/custom_calculator.js"),
  "utf8"
);

test("auto-update does NOT trigger before first calculation", () => {
  document.body.innerHTML = `
    <form id="custom-form"></form>
    <div id="custom-results"></div>

    <input type="radio" name="dp_mode" value="dollar" checked>
    <input id="down_payment_slider" type="range" value="20">
    <input id="down_payment_max" value="200000">

    <div id="dp-max-row"></div>
    <span id="dp-min-label"></span>
    <span id="dp-max-label"></span>
    <div id="dp-slider-label"></div>

    <input id="income_pct_slider" value="25">
    <div id="income-pct-label"></div>
  `;

  eval(script);

  const form = document.getElementById("custom-form");

  let triggered = false;
  form.addEventListener("submit", () => (triggered = true));

  form.dispatchEvent(new Event("input"));

  expect(triggered).toBe(false);
});

test("auto-update triggers AFTER first calculation", () => {
  document.body.innerHTML = `
    <form id="custom-form"></form>
    <div id="custom-results"></div>

    <input type="radio" name="dp_mode" value="dollar" checked>
    <input id="down_payment_slider" type="range" value="20">
    <input id="down_payment_max" value="200000">

    <div id="dp-max-row"></div>
    <span id="dp-min-label"></span>
    <span id="dp-max-label"></span>
    <div id="dp-slider-label"></div>

    <input id="income_pct_slider" value="25">
    <div id="income-pct-label"></div>
  `;

  eval(script);

  const form = document.getElementById("custom-form");
  const results = document.getElementById("custom-results");

  let triggered = false;
  form.addEventListener("submit", () => (triggered = true));

  // ✅ Simulate HTMX swap using the live DOM reference
  document.body.dispatchEvent(
    new CustomEvent("htmx:afterSwap", {
      detail: { target: document.getElementById("custom-results") }
    })
  );

  // ✅ Now auto-update should fire
  form.dispatchEvent(new Event("input"));

  expect(triggered).toBe(true);
});
