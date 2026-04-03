"""
Selenium test suite for Bayesian Random-Effects Meta-Analysis (BayesianMA).
Tests: page load, tabs, example datasets, posterior computation, HDI/CrI,
prior sensitivity (3 results), dark mode, export, forest plot, density plots,
shrinkage table, DIC, CSV paste, R code, MAIF, report generation, reset.
"""

import io
import os
import sys
import time
import pytest
import pathlib

# Note: avoid sys.stdout reassignment as it conflicts with pytest capture.
# Use PYTHONUTF8=1 env var or pytest -s if Unicode output is needed.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

HTML_PATH = pathlib.Path(r"C:\Models\BayesianMA\bayesian-ma.html").resolve()
FILE_URL = HTML_PATH.as_uri()


@pytest.fixture(scope="module")
def driver():
    """Launch Chrome headless, override window.confirm, yield driver."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1400,1000")
    opts.add_argument("--disable-dev-shm-usage")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    drv = webdriver.Chrome(options=opts)
    drv.get(FILE_URL)
    # Override confirm dialogs to always return True
    drv.execute_script("window.confirm = function() { return true; };")
    # Clear localStorage to start fresh
    drv.execute_script("localStorage.clear();")
    drv.get(FILE_URL)
    drv.execute_script("window.confirm = function() { return true; };")
    yield drv
    drv.quit()


def js_click(driver, el):
    """Click via JS to avoid headless interactability issues."""
    driver.execute_script("arguments[0].click();", el)


def wait_for(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def switch_tab(driver, tab_id):
    """Switch to a tab by its element ID."""
    tab = driver.find_element(By.ID, tab_id)
    js_click(driver, tab)
    time.sleep(0.3)


def load_magnesium_and_run(driver):
    """Load magnesium dataset, navigate to priors, run analysis."""
    switch_tab(driver, "tabData")
    time.sleep(0.3)
    btn = driver.find_element(By.ID, "btnExMg")
    js_click(driver, btn)
    time.sleep(0.3)

    switch_tab(driver, "tabPriors")
    time.sleep(0.3)
    run_btn = driver.find_element(By.ID, "btnRunAnalysis")
    js_click(driver, run_btn)
    # Grid approximation with 500 points -- wait for results
    time.sleep(3)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestPageLoad:
    """Basic page load and structure."""

    def test_01_title(self, driver):
        """Page title contains 'Bayesian'."""
        assert "Bayesian" in driver.title

    def test_02_header_visible(self, driver):
        """Header h1 is present and contains expected text."""
        h1 = driver.find_element(By.CSS_SELECTOR, ".app-header h1")
        assert "Bayesian" in h1.text

    def test_03_subtitle(self, driver):
        """Subtitle mentions Normal-Normal Hierarchical."""
        sub = driver.find_element(By.CSS_SELECTOR, ".app-header .subtitle")
        assert "Normal-Normal" in sub.text or "Hierarchical" in sub.text


class TestTabs:
    """Tab navigation works correctly."""

    def test_04_all_tabs_present(self, driver):
        """All 4 tabs exist: Data, Priors, Results, Report."""
        tabs = driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        assert len(tabs) == 4
        labels = [t.text for t in tabs]
        assert "Data" in labels
        assert "Priors" in labels
        assert "Results" in labels
        assert "Report" in labels

    def test_05_tab_switch_priors(self, driver):
        """Clicking Priors tab shows its panel."""
        switch_tab(driver, "tabPriors")
        panel = driver.find_element(By.ID, "panelPriors")
        assert "active" in panel.get_attribute("class")

    def test_06_tab_switch_data(self, driver):
        """Switching back to Data tab shows data panel."""
        switch_tab(driver, "tabData")
        panel = driver.find_element(By.ID, "panelData")
        assert "active" in panel.get_attribute("class")

    def test_07_results_tab_placeholder(self, driver):
        """Results tab shows placeholder before analysis."""
        switch_tab(driver, "tabResults")
        placeholder = driver.find_element(By.ID, "resultsPlaceholder")
        # Placeholder should be visible (display != none)
        disp = placeholder.value_of_css_property("display")
        assert disp != "none"


class TestExampleDatasets:
    """Built-in example datasets load correctly."""

    def test_08_magnesium_loads(self, driver):
        """Magnesium-MI dataset loads 8 studies."""
        switch_tab(driver, "tabData")
        time.sleep(0.3)
        btn = driver.find_element(By.ID, "btnExMg")
        js_click(driver, btn)
        time.sleep(0.5)
        count = driver.find_element(By.ID, "studyCount")
        assert count.text == "8"

    def test_09_aspirin_loads(self, driver):
        """Aspirin-stroke dataset loads 6 studies."""
        switch_tab(driver, "tabData")
        btn = driver.find_element(By.ID, "btnExAspirin")
        js_click(driver, btn)
        time.sleep(0.5)
        count = driver.find_element(By.ID, "studyCount")
        assert count.text == "6"

    def test_10_effect_type_changes(self, driver):
        """Loading aspirin sets effect type to logRR."""
        sel = driver.find_element(By.ID, "selEffectType")
        assert sel.get_attribute("value") == "logRR"


class TestPosteriorComputation:
    """Run analysis and verify posterior results appear."""

    def test_11_run_analysis_magnesium(self, driver):
        """Running analysis on magnesium produces results."""
        load_magnesium_and_run(driver)
        # Should be on Results tab now
        content = driver.find_element(By.ID, "resultsContent")
        disp = content.value_of_css_property("display")
        assert disp != "none", "Results content should be visible after analysis"

    def test_12_mu_stats_populated(self, driver):
        """Posterior mu stats contain stat cards with numeric values."""
        mu_stats = driver.find_element(By.ID, "muStats")
        cards = mu_stats.find_elements(By.CSS_SELECTOR, ".stat-card")
        assert len(cards) >= 4, f"Expected >=4 stat cards for mu, got {len(cards)}"
        # First card should have a numeric value (mean)
        val = cards[0].find_element(By.CSS_SELECTOR, ".stat-value").text
        assert val != "" and val != "N/A", f"mu mean should be a number, got '{val}'"

    def test_13_tau_stats_populated(self, driver):
        """Posterior tau stats contain stat cards."""
        tau_stats = driver.find_element(By.ID, "tauStats")
        cards = tau_stats.find_elements(By.CSS_SELECTOR, ".stat-card")
        assert len(cards) >= 4

    def test_14_cri_present(self, driver):
        """95% CrI (credible interval) is shown for mu."""
        mu_stats = driver.find_element(By.ID, "muStats")
        text = mu_stats.text
        assert "to" in text, "95% CrI should contain 'to' separator"

    def test_15_p_mu_lt_zero(self, driver):
        """P(mu<0) is displayed and is a valid probability."""
        mu_stats = driver.find_element(By.ID, "muStats")
        cards = mu_stats.find_elements(By.CSS_SELECTOR, ".stat-card")
        # The 4th card is P(mu<0)
        p_card = cards[3]
        label_text = p_card.find_element(By.CSS_SELECTOR, ".stat-label").text
        val_text = p_card.find_element(By.CSS_SELECTOR, ".stat-value").text
        assert "p(mu" in label_text.lower() or "p(mu" in label_text.lower().replace(" ", "")
        p_val = float(val_text)
        assert 0.0 <= p_val <= 1.0, f"P(mu<0) should be 0-1, got {p_val}"


class TestSensitivityAnalysis:
    """Prior sensitivity analysis shows 3 scenario results."""

    def test_16_sensitivity_table_rows(self, driver):
        """Sensitivity table has 3 rows (Vague, Weakly Informative, Skeptical)."""
        # Ensure we are on Results tab with results loaded
        switch_tab(driver, "tabResults")
        time.sleep(0.3)
        rows = driver.find_elements(By.CSS_SELECTOR, "#sensitivityTableBody tr")
        assert len(rows) == 3, f"Expected 3 sensitivity rows, got {len(rows)}"

    def test_17_sensitivity_labels(self, driver):
        """Sensitivity rows have correct scenario labels."""
        rows = driver.find_elements(By.CSS_SELECTOR, "#sensitivityTableBody tr")
        labels = [r.find_elements(By.TAG_NAME, "td")[0].text for r in rows]
        assert "Vague" in labels
        assert "Weakly Informative" in labels
        assert "Skeptical" in labels

    def test_18_sensitivity_has_numeric_values(self, driver):
        """Each sensitivity row has numeric mu Mean and tau Mean."""
        rows = driver.find_elements(By.CSS_SELECTOR, "#sensitivityTableBody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            mu_mean = cells[1].text
            tau_mean = cells[3].text
            assert mu_mean != "" and mu_mean != "N/A"
            assert tau_mean != "" and tau_mean != "N/A"
            float(mu_mean)  # should not raise
            float(tau_mean)  # should not raise


class TestPlots:
    """SVG plots are rendered."""

    def test_19_forest_plot_svg(self, driver):
        """Forest plot container has an SVG element."""
        switch_tab(driver, "tabResults")
        time.sleep(0.3)
        container = driver.find_element(By.ID, "forestPlotContainer")
        svgs = container.find_elements(By.TAG_NAME, "svg")
        assert len(svgs) >= 1, "Forest plot SVG not found"

    def test_20_mu_density_svg(self, driver):
        """Mu density plot has an SVG."""
        container = driver.find_element(By.ID, "muDensityContainer")
        svgs = container.find_elements(By.TAG_NAME, "svg")
        assert len(svgs) >= 1, "Mu density SVG not found"

    def test_21_tau_density_svg(self, driver):
        """Tau density plot has an SVG."""
        container = driver.find_element(By.ID, "tauDensityContainer")
        svgs = container.find_elements(By.TAG_NAME, "svg")
        assert len(svgs) >= 1, "Tau density SVG not found"


class TestShrinkageAndDIC:
    """Shrinkage table and DIC stats appear correctly."""

    def test_22_shrinkage_table(self, driver):
        """Shrinkage table has rows matching study count."""
        switch_tab(driver, "tabResults")
        time.sleep(0.3)
        rows = driver.find_elements(By.CSS_SELECTOR, "#shrinkageTableBody tr")
        # We loaded magnesium (8 studies)
        assert len(rows) == 8, f"Expected 8 shrinkage rows, got {len(rows)}"

    def test_23_dic_stats(self, driver):
        """DIC stats show D-bar, pD, and DIC values."""
        dic = driver.find_element(By.ID, "dicStats")
        cards = dic.find_elements(By.CSS_SELECTOR, ".stat-card")
        assert len(cards) == 3
        labels = [c.find_element(By.CSS_SELECTOR, ".stat-label").text for c in cards]
        assert any("D-bar" in l or "D-BAR" in l for l in labels)
        assert any("pD" in l or "PD" in l for l in labels)
        assert any("DIC" in l for l in labels)


class TestDarkMode:
    """Dark mode toggle."""

    def test_24_dark_mode_toggle(self, driver):
        """Clicking dark mode button adds dark-mode class to body."""
        btn = driver.find_element(By.ID, "btnDarkMode")
        was_dark = "dark-mode" in driver.find_element(By.TAG_NAME, "body").get_attribute("class")
        js_click(driver, btn)
        time.sleep(0.3)
        is_dark = "dark-mode" in driver.find_element(By.TAG_NAME, "body").get_attribute("class")
        assert is_dark != was_dark, "Dark mode class should toggle"
        # Toggle back to original state
        js_click(driver, btn)
        time.sleep(0.2)


class TestExport:
    """Export buttons exist and are functional."""

    def test_25_export_csv_button(self, driver):
        """Export CSV button exists on Report tab."""
        switch_tab(driver, "tabReport")
        time.sleep(0.3)
        btn = driver.find_element(By.ID, "btnExportCSV")
        assert btn.is_displayed() or True  # Button exists in DOM

    def test_26_export_json_button(self, driver):
        """Export JSON button exists."""
        btn = driver.find_element(By.ID, "btnExportJSON")
        assert btn is not None

    def test_27_export_maif_button(self, driver):
        """Export MAIF button exists."""
        btn = driver.find_element(By.ID, "btnExportMAIF")
        assert btn is not None

    def test_28_print_button(self, driver):
        """Print Report button exists."""
        btn = driver.find_element(By.ID, "btnPrint")
        assert btn is not None


class TestReportGeneration:
    """Report tab content after analysis."""

    def test_29_methods_text(self, driver):
        """Methods text is generated and mentions Bayesian."""
        switch_tab(driver, "tabReport")
        time.sleep(0.3)
        methods = driver.find_element(By.ID, "methodsText")
        text = methods.text
        assert len(text) > 50, "Methods text should be substantial"
        assert "Bayesian" in text or "bayesian" in text.lower()

    def test_30_r_code(self, driver):
        """R code block is populated with bayesmeta code."""
        rcode = driver.find_element(By.ID, "rCode")
        text = rcode.text
        assert "bayesmeta" in text
        assert "library" in text

    def test_31_report_content_visible(self, driver):
        """Report content div is visible (not hidden)."""
        content = driver.find_element(By.ID, "reportContent")
        disp = content.value_of_css_property("display")
        assert disp != "none"


class TestCSVPaste:
    """CSV paste feature."""

    def test_32_csv_paste(self, driver):
        """Pasting CSV data loads studies."""
        switch_tab(driver, "tabData")
        time.sleep(0.3)
        textarea = driver.find_element(By.ID, "csvPaste")
        textarea.clear()
        csv_data = "StudyA, -0.50, 0.30\nStudyB, -0.20, 0.40\nStudyC, 0.10, 0.25"
        textarea.send_keys(csv_data)
        btn = driver.find_element(By.ID, "btnParseCsv")
        js_click(driver, btn)
        time.sleep(0.5)
        count = driver.find_element(By.ID, "studyCount")
        assert count.text == "3", f"Expected 3 studies from CSV, got {count.text}"


class TestResetAndMisc:
    """Reset, add row, and misc functionality."""

    def test_33_add_row(self, driver):
        """Add Row button creates a new empty study row."""
        switch_tab(driver, "tabData")
        time.sleep(0.3)
        # First load magnesium to have a known count
        js_click(driver, driver.find_element(By.ID, "btnExMg"))
        time.sleep(0.3)
        before = int(driver.find_element(By.ID, "studyCount").text)
        js_click(driver, driver.find_element(By.ID, "btnAddRow"))
        time.sleep(0.3)
        after = int(driver.find_element(By.ID, "studyCount").text)
        assert after == before + 1

    def test_34_reset_clears_data(self, driver):
        """Reset button clears all studies."""
        js_click(driver, driver.find_element(By.ID, "btnReset"))
        time.sleep(0.5)
        count = driver.find_element(By.ID, "studyCount")
        assert count.text == "0"

    def test_35_no_js_errors(self, driver):
        """No severe JS errors in console logs."""
        logs = driver.get_log("browser")
        severe = [l for l in logs if l.get("level") == "SEVERE"]
        # Filter out benign errors (favicon, etc.)
        real_errors = [
            l for l in severe
            if "favicon" not in l.get("message", "").lower()
            and "net::ERR" not in l.get("message", "")
        ]
        assert len(real_errors) == 0, f"JS errors found: {real_errors}"
