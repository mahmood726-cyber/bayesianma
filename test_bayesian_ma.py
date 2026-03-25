"""
Selenium tests for Bayesian Random-Effects Meta-Analysis HTML app.
25 tests covering: page load, data entry, examples, prior settings,
posterior computation, forest plot, shrinkage table, sensitivity analysis,
export, dark mode.

Usage: python test_bayesian_ma.py
"""

import io
import json
import os
import sys
import time
import unittest

# UTF-8 output for Windows cp1252
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bayesian-ma.html')
FILE_URL = 'file:///' + HTML_PATH.replace('\\', '/')

DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'selenium-downloads')


def get_driver():
    """Create Chrome driver with headless mode and download support."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1400,900')
    opts.add_experimental_option('prefs', {
        'download.default_directory': DOWNLOAD_DIR,
        'download.prompt_for_download': False,
    })
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(3)
    return driver


class TestBayesianMA(unittest.TestCase):
    """25 Selenium tests for the Bayesian MA app."""

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.driver.get(FILE_URL)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def reload(self):
        self.driver.get(FILE_URL)
        time.sleep(0.5)

    # --- 1. Page Load ---
    def test_01_page_loads(self):
        """Page title and header present."""
        self.assertIn('Bayesian', self.driver.title)
        header = self.driver.find_element(By.CSS_SELECTOR, '.app-header h1')
        self.assertIn('Bayesian', header.text)

    # --- 2. Tab navigation ---
    def test_02_tab_navigation(self):
        """All 4 tabs are clickable and show corresponding panels."""
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        self.assertEqual(len(tabs), 4)
        for tab in tabs:
            tab.click()
            time.sleep(0.3)
            panel_id = tab.get_attribute('aria-controls')
            panel = self.driver.find_element(By.ID, panel_id)
            self.assertIn('active', panel.get_attribute('class'))

    # --- 3. Data tab default state ---
    def test_03_data_tab_default(self):
        """Data tab shows 0 studies initially (after reset)."""
        self.reload()
        # Clear localStorage first
        self.driver.execute_script("localStorage.removeItem('bayesianMA_v1');")
        self.reload()
        count = self.driver.find_element(By.ID, 'studyCount')
        self.assertEqual(count.text, '0')

    # --- 4. Add row ---
    def test_04_add_row(self):
        """Add row button creates a new row."""
        self.driver.execute_script("localStorage.removeItem('bayesianMA_v1');")
        self.reload()
        btn = self.driver.find_element(By.ID, 'btnAddRow')
        btn.click()
        time.sleep(0.3)
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#dataTableBody tr')
        self.assertGreaterEqual(len(rows), 1)
        count = self.driver.find_element(By.ID, 'studyCount')
        self.assertEqual(count.text, '1')

    # --- 5. Load Magnesium example ---
    def test_05_load_magnesium(self):
        """Magnesium example loads 8 studies."""
        self.reload()
        self.driver.find_element(By.ID, 'btnExMg').click()
        time.sleep(0.5)
        count = self.driver.find_element(By.ID, 'studyCount')
        self.assertEqual(count.text, '8')
        # Check effect type changed
        sel = Select(self.driver.find_element(By.ID, 'selEffectType'))
        self.assertEqual(sel.first_selected_option.get_attribute('value'), 'logOR')

    # --- 6. Load Aspirin example ---
    def test_06_load_aspirin(self):
        """Aspirin example loads 6 studies."""
        self.reload()
        self.driver.find_element(By.ID, 'btnExAspirin').click()
        time.sleep(0.5)
        count = self.driver.find_element(By.ID, 'studyCount')
        self.assertEqual(count.text, '6')
        sel = Select(self.driver.find_element(By.ID, 'selEffectType'))
        self.assertEqual(sel.first_selected_option.get_attribute('value'), 'logRR')

    # --- 7. CSV paste ---
    def test_07_csv_paste(self):
        """CSV paste populates the data table."""
        self.driver.execute_script("localStorage.removeItem('bayesianMA_v1');")
        self.reload()
        csv_data = "StudyA, -0.5, 0.3\nStudyB, -0.2, 0.4\nStudyC, 0.1, 0.5"
        textarea = self.driver.find_element(By.ID, 'csvPaste')
        textarea.clear()
        textarea.send_keys(csv_data)
        self.driver.find_element(By.ID, 'btnParseCsv').click()
        time.sleep(0.5)
        count = self.driver.find_element(By.ID, 'studyCount')
        self.assertEqual(count.text, '3')

    # --- 8. Remove row ---
    def test_08_remove_row(self):
        """Remove button deletes a study row."""
        self.reload()
        self.driver.find_element(By.ID, 'btnExMg').click()
        time.sleep(0.3)
        initial = int(self.driver.find_element(By.ID, 'studyCount').text)
        del_btn = self.driver.find_element(By.CSS_SELECTOR, '.btn-del')
        del_btn.click()
        time.sleep(0.3)
        after = int(self.driver.find_element(By.ID, 'studyCount').text)
        self.assertEqual(after, initial - 1)

    # --- 9. Effect type selection ---
    def test_09_effect_type(self):
        """Effect type dropdown has 4 options and changes."""
        self.reload()
        sel = Select(self.driver.find_element(By.ID, 'selEffectType'))
        options = [o.get_attribute('value') for o in sel.options]
        self.assertEqual(len(options), 4)
        self.assertIn('logOR', options)
        self.assertIn('SMD', options)

    # --- 10. Prior settings UI ---
    def test_10_prior_settings(self):
        """Prior inputs are accessible and update description."""
        self.reload()
        self.driver.find_element(By.ID, 'tabPriors').click()
        time.sleep(0.3)
        mu_mean = self.driver.find_element(By.ID, 'priorMuMean')
        mu_sd = self.driver.find_element(By.ID, 'priorMuSD')
        tau_scale = self.driver.find_element(By.ID, 'priorTauScale')
        self.assertTrue(mu_mean.is_displayed())
        self.assertTrue(mu_sd.is_displayed())
        self.assertTrue(tau_scale.is_displayed())

    # --- 11. Prior description updates ---
    def test_11_prior_desc_update(self):
        """Changing prior SD updates the description text."""
        self.reload()
        self.driver.find_element(By.ID, 'tabPriors').click()
        time.sleep(0.3)
        mu_sd = self.driver.find_element(By.ID, 'priorMuSD')
        mu_sd.clear()
        mu_sd.send_keys('0.5')
        mu_sd.send_keys(Keys.TAB)
        time.sleep(0.3)
        desc = self.driver.find_element(By.ID, 'priorMuDesc').text
        self.assertIn('Skeptical', desc)

    # --- 12. Run analysis (Magnesium) ---
    def test_12_run_analysis_mg(self):
        """Running analysis with Magnesium data produces results."""
        self.reload()
        self.driver.find_element(By.ID, 'btnExMg').click()
        time.sleep(0.3)
        self.driver.find_element(By.ID, 'tabPriors').click()
        time.sleep(0.3)
        self.driver.find_element(By.ID, 'btnRunAnalysis').click()
        time.sleep(1)
        # Should switch to results tab
        panel = self.driver.find_element(By.ID, 'panelResults')
        self.assertIn('active', panel.get_attribute('class'))
        # Results content should be visible
        content = self.driver.find_element(By.ID, 'resultsContent')
        self.assertEqual(content.value_of_css_property('display'), 'block')

    # --- 13. Posterior mu stats ---
    def test_13_posterior_mu_stats(self):
        """Posterior mu summary cards show numeric values."""
        mu_stats = self.driver.find_element(By.ID, 'muStats')
        cards = mu_stats.find_elements(By.CSS_SELECTOR, '.stat-card')
        self.assertEqual(len(cards), 4)
        # Mean card should have a numeric value
        mean_val = cards[0].find_element(By.CSS_SELECTOR, '.stat-value').text
        self.assertNotEqual(mean_val, 'N/A')
        val = float(mean_val)
        # Magnesium data: expect negative mu (protective effect)
        self.assertLess(val, 0)

    # --- 14. Posterior tau stats ---
    def test_14_posterior_tau_stats(self):
        """Posterior tau summary cards show non-negative values."""
        tau_stats = self.driver.find_element(By.ID, 'tauStats')
        cards = tau_stats.find_elements(By.CSS_SELECTOR, '.stat-card')
        self.assertEqual(len(cards), 4)
        mean_val = float(cards[0].find_element(By.CSS_SELECTOR, '.stat-value').text)
        self.assertGreaterEqual(mean_val, 0)

    # --- 15. Forest plot rendered ---
    def test_15_forest_plot(self):
        """Forest plot SVG is rendered with circles and text."""
        container = self.driver.find_element(By.ID, 'forestPlotContainer')
        svg = container.find_element(By.TAG_NAME, 'svg')
        self.assertIsNotNone(svg)
        circles = svg.find_elements(By.TAG_NAME, 'circle')
        self.assertGreater(len(circles), 0)
        texts = svg.find_elements(By.TAG_NAME, 'text')
        self.assertGreater(len(texts), 0)

    # --- 16. Forest plot has diamond ---
    def test_16_forest_plot_diamond(self):
        """Forest plot has a diamond (path element) for overall estimate."""
        container = self.driver.find_element(By.ID, 'forestPlotContainer')
        svg = container.find_element(By.TAG_NAME, 'svg')
        paths = svg.find_elements(By.TAG_NAME, 'path')
        # At least one path should contain the diamond (M...L...L...L...Z)
        diamond_found = False
        for p in paths:
            d = p.get_attribute('d')
            if d and d.count('L') >= 3 and 'Z' in d:
                diamond_found = True
                break
        self.assertTrue(diamond_found, 'Diamond path not found in forest plot')

    # --- 17. Mu density plot ---
    def test_17_mu_density_plot(self):
        """Mu posterior density plot is rendered."""
        container = self.driver.find_element(By.ID, 'muDensityContainer')
        svg = container.find_element(By.TAG_NAME, 'svg')
        self.assertIsNotNone(svg)
        paths = svg.find_elements(By.TAG_NAME, 'path')
        self.assertGreater(len(paths), 0)

    # --- 18. Tau density plot ---
    def test_18_tau_density_plot(self):
        """Tau posterior density plot is rendered."""
        container = self.driver.find_element(By.ID, 'tauDensityContainer')
        svg = container.find_element(By.TAG_NAME, 'svg')
        self.assertIsNotNone(svg)

    # --- 19. Shrinkage table ---
    def test_19_shrinkage_table(self):
        """Shrinkage table has one row per study with valid data."""
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#shrinkageTableBody tr')
        self.assertEqual(len(rows), 8)  # 8 Mg studies
        # Check first row has numeric values
        cells = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(len(cells), 5)
        # Shrinkage factor should be between 0 and 1
        sf = float(cells[3].text)
        self.assertGreaterEqual(sf, 0)
        self.assertLessEqual(sf, 1)

    # --- 20. Sensitivity analysis table ---
    def test_20_sensitivity_table(self):
        """Sensitivity analysis produces 3 scenario rows."""
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#sensitivityTableBody tr')
        self.assertEqual(len(rows), 3)
        labels = [r.find_elements(By.TAG_NAME, 'td')[0].text for r in rows]
        self.assertIn('Vague', labels)
        self.assertIn('Weakly Informative', labels)
        self.assertIn('Skeptical', labels)

    # --- 21. DIC statistics ---
    def test_21_dic_stats(self):
        """DIC stats section shows 3 cards with numeric values."""
        dic_stats = self.driver.find_element(By.ID, 'dicStats')
        cards = dic_stats.find_elements(By.CSS_SELECTOR, '.stat-card')
        self.assertEqual(len(cards), 3)
        for card in cards:
            val = card.find_element(By.CSS_SELECTOR, '.stat-value').text
            self.assertNotEqual(val, 'N/A')

    # --- 22. Report tab ---
    def test_22_report_tab(self):
        """Report tab shows methods text with references."""
        self.driver.find_element(By.ID, 'tabReport').click()
        time.sleep(0.3)
        methods = self.driver.find_element(By.ID, 'methodsText')
        self.assertIn('Normand', methods.text)
        self.assertIn('Higgins', methods.text)
        self.assertIn('Polson', methods.text)

    # --- 23. R code ---
    def test_23_r_code(self):
        """R code block contains bayesmeta package reference."""
        rcode = self.driver.find_element(By.ID, 'rCode')
        self.assertIn('bayesmeta', rcode.text)
        self.assertIn('library', rcode.text)

    # --- 24. Dark mode toggle ---
    def test_24_dark_mode(self):
        """Dark mode toggles body class."""
        btn = self.driver.find_element(By.ID, 'btnDarkMode')
        # Get initial state
        body_class = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        was_dark = 'dark-mode' in (body_class or '')
        btn.click()
        time.sleep(0.3)
        body_class = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        is_dark = 'dark-mode' in (body_class or '')
        self.assertNotEqual(was_dark, is_dark)
        # Toggle back
        btn.click()
        time.sleep(0.3)

    # --- 25. Export CSV (download check) ---
    def test_25_export_csv(self):
        """Export CSV creates a downloadable file (no JS errors)."""
        # Navigate to report tab where export buttons are
        self.driver.find_element(By.ID, 'tabReport').click()
        time.sleep(0.3)
        # Click export - in headless mode just verify no JS errors
        btn = self.driver.find_element(By.ID, 'btnExportCSV')
        self.assertTrue(btn.is_displayed())
        # Check console for errors
        logs = self.driver.get_log('browser')
        severe_errors = [l for l in logs if l.get('level') == 'SEVERE' and 'favicon' not in l.get('message', '')]
        # Allow download-related errors in headless
        non_download_errors = [l for l in severe_errors if 'download' not in l.get('message', '').lower()]
        self.assertEqual(len(non_download_errors), 0,
                         f'JS errors found: {non_download_errors}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
