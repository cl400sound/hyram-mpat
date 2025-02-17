"""
Copyright 2015-2022 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

You should have received a copy of the GNU General Public License along with HyRAM+.
If not, see https://www.gnu.org/licenses/.
"""

import unittest

import hyram.qra.risk as hyram_risk


class TestRiskMetricCalcs(unittest.TestCase):
    """
    Test basic calculation of risk metrics
    """
    def test_calc_pll(self):
        frequency = 1.12e-5  # per year
        consequence = 0.1  # fatalties
        pll = hyram_risk.calc_pll(frequency, consequence)
        # Hand-calculation of above numbers
        self.assertAlmostEqual(pll, 1.12e-6)

    def test_calc_far(self):
        pll = 2.5e-5  # fatalties/year
        total_occupants = 9
        far = hyram_risk.calc_far(pll, total_occupants)
        # Hand-calculation of above numbers
        self.assertAlmostEqual(far, 0.0317098)

    def test_zero_far_for_zero_pll(self):
        pll = 0.0  # fatalties/year
        total_occupants = 0
        far = hyram_risk.calc_far(pll, total_occupants)
        # Hand-calculation of above numbers
        self.assertAlmostEqual(far, 0.0)

    def test_calc_air(self):
        far = 0.03  # fatalties per 10^8 person*hours
        exposed_hours_per_year = 2000
        air = hyram_risk.calc_air(far, exposed_hours_per_year)
        # Hand-calculation of above numbers
        self.assertAlmostEqual(air, 6e-7)


class TestScenarioRiskCalcs(unittest.TestCase):
    """
    Test calculation of risk (PLL) for all scenarios
    """
    def test_calc_all_plls(self):
        frequencies = [1.0e-5, 2.0e-5]
        fatalities = [0.1, 0.2]
        plls = hyram_risk.calc_all_plls(frequencies, fatalities)
        # Hand-calculation of above numbers
        hand_calc_plls = [1.0e-6, 4.0e-6]
        for calc_pll, test_pll in zip(plls, hand_calc_plls):
            self.assertAlmostEqual(calc_pll, test_pll)

    def test_calc_risk_contributions(self):
        plls = [1.0e-6, 4.0e-6]
        total_pll, pll_contributions = hyram_risk.calc_risk_contributions(plls)
        # Hand-calculation of above numbers
        self.assertAlmostEqual(total_pll, 5e-6)
        hand_calc_contributions = [0.2, 0.8]
        for calc_value, test_value in zip(pll_contributions, hand_calc_contributions):
            self.assertAlmostEqual(calc_value, test_value)

    def test_calc_risk_contributions_handles_zeros(self):
        plls = [0.0, 0.0]
        total_pll, pll_contributions = hyram_risk.calc_risk_contributions(plls)
        # Hand-calculation of above numbers
        self.assertAlmostEqual(total_pll, 0.0)
        hand_calc_contributions = [0.0, 0.0]
        for calc_value, test_value in zip(pll_contributions, hand_calc_contributions):
            self.assertAlmostEqual(calc_value, test_value)



if __name__ == "__main__":
    unittest.main()
