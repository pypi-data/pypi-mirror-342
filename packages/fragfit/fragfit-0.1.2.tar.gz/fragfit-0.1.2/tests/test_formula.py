"""
Tests for the formula module.
"""

import unittest
import numpy as np

from fragfit.formula import (
    charged_mass, 
    uncharged_mass, 
    form_to_mz, 
    find_best_form
)
from fragfit.adducts import adduct_mass, parse_adduct

class TestFormula(unittest.TestCase):
    """Test cases for formula functions."""
    
    def test_charged_mass(self):
        """Test charged_mass function."""
        # Test with numeric mass
        self.assertAlmostEqual(charged_mass(100.0, 1), 99.9994514, places=6)
        self.assertAlmostEqual(charged_mass(100.0, -1), 100.0005486, places=6)
        
        # Test with formula
        self.assertAlmostEqual(charged_mass("H2O", 1), 18.0100, places=4)
    
    def test_uncharged_mass(self):
        """Test uncharged_mass function."""
        # Test with numeric mass
        self.assertAlmostEqual(uncharged_mass(99.9994514, 1), 100.0, places=6)
        self.assertAlmostEqual(uncharged_mass(100.0005486, -1), 100.0, places=6)
    
    def test_form_to_mz(self):
        """Test form_to_mz function."""
        # Test m/z calculation
        self.assertAlmostEqual(form_to_mz("C6H12O6", 1), 180.0628, places=4)
        self.assertAlmostEqual(form_to_mz("C6H12O6", 2), 90.0311, places=4)
    
    def test_find_best_form(self):
        """Test find_best_form function."""
        # Create a simple test case
        form, mass, error = find_best_form(
            mass=180.063,
            parent_form="C10H20O10",
            tolerance_da=0.01
        )
        
        self.assertEqual(form, "C6H12O6")
        self.assertAlmostEqual(mass, 180.0634, places=4)
        self.assertLess(error, 0.01)
    
    def test_adduct_mass(self):
        """Test adduct_mass function."""
        # Test with H+ adduct
        self.assertAlmostEqual(adduct_mass("C6H12O6", "[M+H]+"), 181.0701, places=4)
        
        # Test with Na+ adduct
        self.assertAlmostEqual(adduct_mass("C6H12O6", "[M+Na]+"), 203.0521, places=4)

if __name__ == '__main__':
    unittest.main() 