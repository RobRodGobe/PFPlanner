/**
 * @jest-environment jsdom
 */

test("standard calculator form has correct HTMX attributes", () => {
  document.body.innerHTML = `
    <form 
      method="POST"
      hx-post="/house_affordability"
      hx-target="#results"
      hx-swap="innerHTML"
    >
      <input name="income">
      <input name="down_payment">
      <input name="interest_rate">
      <input name="loan_term">
      <input type="hidden" id="advanced-state" name="advanced_state" value="0">

      <button
        type="button"
        hx-get="/house_affordability"
        hx-target="#advanced-fields"
        hx-swap="innerHTML"
      >
        Advanced Options
      </button>

      <div id="advanced-fields"></div>
      <button type="submit">Calculate</button>
    </form>

    <div id="results"></div>
  `;

  const form = document.querySelector("form");
  expect(form.getAttribute("hx-post")).toBe("/house_affordability");
  expect(form.getAttribute("hx-target")).toBe("#results");
  expect(form.getAttribute("hx-swap")).toBe("innerHTML");

  const advButton = form.querySelector('button[type="button"]');
  expect(advButton.getAttribute("hx-get")).toBe("/house_affordability");
  expect(advButton.getAttribute("hx-target")).toBe("#advanced-fields");
  expect(advButton.getAttribute("hx-swap")).toBe("innerHTML");

  expect(document.getElementById("results")).not.toBeNull();
  expect(document.getElementById("advanced-fields")).not.toBeNull();
});
