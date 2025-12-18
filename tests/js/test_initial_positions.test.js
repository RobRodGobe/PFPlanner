/**
 * @jest-environment jsdom
 */

test("initial slider label positions match HTML defaults", () => {
  document.body.innerHTML = `
    <div id="dp-slider-label" style="left: calc(20% - 16px);"></div>
    <div id="income-pct-label" style="left: calc(100% - 16px);"></div>
  `;

  const dp = document.getElementById("dp-slider-label");
  const inc = document.getElementById("income-pct-label");

  expect(dp.style.left).toBe("calc(20% - 16px)");
  expect(inc.style.left).toBe("calc(100% - 16px)");
});
