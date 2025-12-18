/**
 * @jest-environment jsdom
 */

test("custom calculator form has correct HTMX attributes", () => {
  document.body.innerHTML = `
    <form 
      id="custom-form"
      method="POST"
      hx-post="/house_affordability_custom"
      hx-target="#custom-results"
      hx-swap="innerHTML"
    >
      <input name="income">
      <input name="down_payment_slider">
      <input name="down_payment_max">
      <input name="interest_rate">
      <input name="loan_term">
      <input name="income_pct_slider">

      <input type="hidden" id="custom-advanced-state" name="custom_advanced_state" value="0">

      <button
        type="button"
        hx-get="/house_affordability_custom_advanced"
        hx-target="#custom-advanced-fields"
        hx-swap="innerHTML"
      >
        Advanced Options
      </button>

      <div id="custom-advanced-fields"></div>
      <button type="submit">Calculate</button>
    </form>

    <div id="custom-results"></div>
  `;

  const form = document.querySelector("form");
  expect(form.getAttribute("hx-post")).toBe("/house_affordability_custom");
  expect(form.getAttribute("hx-target")).toBe("#custom-results");
  expect(form.getAttribute("hx-swap")).toBe("innerHTML");

  const advButton = form.querySelector('button[type="button"]');
  expect(advButton.getAttribute("hx-get")).toBe("/house_affordability_custom_advanced");
  expect(advButton.getAttribute("hx-target")).toBe("#custom-advanced-fields");
  expect(advButton.getAttribute("hx-swap")).toBe("innerHTML");

  expect(document.getElementById("custom-results")).not.toBeNull();
  expect(document.getElementById("custom-advanced-fields")).not.toBeNull();
});
