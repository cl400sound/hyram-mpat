"""
Copyright 2015-2022 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

You should have received a copy of the GNU General Public License along with HyRAM+.
If not, see https://www.gnu.org/licenses/.
"""

import os
import unittest

import numpy as np

import hyram.qra.effects as hyram_effects
import hyram.phys.api as phys_api
import hyram.phys._comps as phys_comps
from hyram.utilities import misc_utils


class TestThermalEffects(unittest.TestCase):
    """
    Test calculation and plotting of thermal effects
    """
    def setUp(self):
        self.amb_fluid = phys_api.create_fluid('AIR',
                                               temp=288,  # K
                                               pres=101325)  # Pa
        self.rel_fluid = phys_api.create_fluid('H2',
                                               temp=288,  # K
                                               pres=35e6,  # Pa
                                               phase='none')
        self.rel_angle = 0  # radians
        self.site_length = 20  # m
        self.site_width = 12  # m
        leak_diams = [0.001, 0.003]  # m
        self.orifices = [phys_comps.Orifice(leak_diam) for leak_diam in leak_diams]
        self.rel_humid = 0.89
        self.not_nozzle_model = 'yuce'
        self.locations = [(5, 0, 1), (6, 1, 2), (7, 0, 2)]  # m
        self.create_plots = True
        self.output_dir = misc_utils.get_temp_folder()
        self.verbose=False

    def test_calc_thermal_effects(self):
        flux_dict = hyram_effects.calc_thermal_effects(self.amb_fluid,
                                                       self.rel_fluid,
                                                       self.rel_angle,
                                                       self.site_length,
                                                       self.site_width,
                                                       self.orifices,
                                                       self.rel_humid,
                                                       self.not_nozzle_model,
                                                       self.locations,
                                                       self.create_plots,
                                                       self.output_dir,
                                                       self.verbose)
        self.assertGreater(max(flux_dict['fluxes']), 0)
        self.assertGreater(len(flux_dict['all_pos_files']), 0)

    def test_zero_occupants(self):
        locations = []
        flux_dict = hyram_effects.calc_thermal_effects(self.amb_fluid,
                                                       self.rel_fluid,
                                                       self.rel_angle,
                                                       self.site_length,
                                                       self.site_width,
                                                       self.orifices,
                                                       self.rel_humid,
                                                       self.not_nozzle_model,
                                                       locations,
                                                       self.create_plots,
                                                       self.output_dir,
                                                       self.verbose)
        self.assertEqual(len(flux_dict['fluxes']), 0)


class TestOverpressureEffects(unittest.TestCase):
    """
    Test calculation and plotting of overpressure effects
    """
    def setUp(self):
        leak_diams = [0.001, 0.003]  # m
        self.orifices = [phys_comps.Orifice(leak_diam) for leak_diam in leak_diams]
        self.notional_nozzle_model = 'yuce'
        self.release_fluid = phys_api.create_fluid('H2',
                                                   temp=288,  # K
                                                   pres=35e6,  # Pa
                                                   phase='none')
        self.ambient_fluid = phys_api.create_fluid('AIR',
                                                   temp=288,  # K
                                                   pres=101325)  # Pa
        self.release_angle = 0  # radians
        self.overp_method = 'bst'
        self.locations = [(5, 0, 1), (6, 1, 2), (7, 0, 2)]  # m
        self.site_length = 20  # m
        self.site_width = 12  # m
        self.BST_mach_flame_speed = 0.35
        self.TNT_equivalence_factor = 0.03
        self.create_plots = True
        self.output_dir = None
        self.verbose = False

    def test_calc_overp_effects_TNT(self):
        overp_dict = hyram_effects.calc_overp_effects(self.orifices,
                                                      self.notional_nozzle_model,
                                                      self.release_fluid,
                                                      self.ambient_fluid,
                                                      self.release_angle,
                                                      self.locations,
                                                      self.site_length,
                                                      self.site_width,
                                                      'tnt',
                                                      self.BST_mach_flame_speed,
                                                      self.TNT_equivalence_factor,
                                                      self.create_plots,
                                                      self.output_dir,
                                                      self.verbose)
        self.assertGreater(max(overp_dict['overpressures']), 0)
        self.assertGreater(max(overp_dict['impulses']), 0)
        self.assertGreater(len(overp_dict['all_pos_overp_files']), 0)
        self.assertGreater(len(overp_dict['all_pos_impulse_files']), 0)

    def test_calc_overp_effects_BST(self):
        overp_dict = hyram_effects.calc_overp_effects(self.orifices,
                                                      self.notional_nozzle_model,
                                                      self.release_fluid,
                                                      self.ambient_fluid,
                                                      self.release_angle,
                                                      self.locations,
                                                      self.site_length,
                                                      self.site_width,
                                                      'bst',
                                                      self.BST_mach_flame_speed,
                                                      self.TNT_equivalence_factor,
                                                      self.create_plots,
                                                      self.output_dir,
                                                      self.verbose)
        self.assertGreater(max(overp_dict['overpressures']), 0)
        self.assertGreater(max(overp_dict['impulses']), 0)
        self.assertGreater(len(overp_dict['all_pos_overp_files']), 0)
        self.assertGreater(len(overp_dict['all_pos_impulse_files']), 0)

    def test_calc_overp_effects_Bauwens(self):
        overp_dict = hyram_effects.calc_overp_effects(self.orifices,
                                                      self.notional_nozzle_model,
                                                      self.release_fluid,
                                                      self.ambient_fluid,
                                                      self.release_angle,
                                                      self.locations,
                                                      self.site_length,
                                                      self.site_width,
                                                      'bauwens',
                                                      self.BST_mach_flame_speed,
                                                      self.TNT_equivalence_factor,
                                                      self.create_plots,
                                                      self.output_dir,
                                                      self.verbose)
        self.assertGreater(max(overp_dict['overpressures']), 0)
        self.assertTrue(np.all(np.isnan(overp_dict['impulses'])))
        self.assertGreater(len(overp_dict['all_pos_overp_files']), 0)
        self.assertEqual(len(overp_dict['all_pos_impulse_files']), 0)

    def test_zero_occupants(self):
        locations = []
        overp_dict = hyram_effects.calc_overp_effects(self.orifices,
                                                      self.notional_nozzle_model,
                                                      self.release_fluid,
                                                      self.ambient_fluid,
                                                      self.release_angle,
                                                      locations,
                                                      self.site_length,
                                                      self.site_width,
                                                      self.overp_method,
                                                      self.BST_mach_flame_speed,
                                                      self.TNT_equivalence_factor,
                                                      self.create_plots,
                                                      self.output_dir,
                                                      self.verbose)
        self.assertEqual(len(overp_dict['overpressures']), 0)
        self.assertEqual(len(overp_dict['impulses']), 0)



class TestEffectPlots(unittest.TestCase):
    """
    Test plotting of thermal and overpressure effects
    """
    def test_plot_effect_positions(self):
        effects = [0.06, 0.01]
        effect_label = 'Test Effect [units]'
        output_dir = misc_utils.get_temp_folder()
        filename = 'test_effect_positions.png'
        filepathname = os.path.join(output_dir, filename)
        title = 'Test Effect Positions Plot'
        x_locations = [1, 5]
        z_locations = [1, 2]
        length = 20
        width = 12
        hyram_effects.plot_effect_positions(effects, 
                                            effect_label,
                                            filepathname,
                                            title,
                                            x_locations,
                                            z_locations,
                                            length,
                                            width)
        self.assertTrue(os.path.isfile(filepathname))



if __name__ == "__main__":
    unittest.main()
