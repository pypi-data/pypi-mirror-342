"""
Tests for the adducts module.
"""

import unittest
import numpy as np

from fragfit.adducts import (
    adduct_mass,
    parse_adduct,
    to_adduct,
    from_adduct
)

class TestAdducts(unittest.TestCase):
    """Test cases for adduct functions."""
    
    def test_parse_adduct(self):
        """Test parse_adduct function."""
        # Test positive adducts
        self.assertEqual(parse_adduct("[M+H]+"), ([('H', 1)], 1))
        self.assertEqual(parse_adduct("[M+Na]+"), ([('Na', 1)], 1))
        
        # Test negative adducts
        self.assertEqual(parse_adduct("[M-H]-"), ([('H', -1)], -1))
        
    def test_to_adduct(self):
        """Test to_adduct function."""
        # Test adding proton
        self.assertEqual(to_adduct("C6H12O6", "[M+H]+"), "C6H13O6")
        
        # Test adding sodium
        self.assertEqual(to_adduct("C6H12O6", "[M+Na]+"), "C6H12NaO6")
        
        # Test adding complex adduct
        self.assertEqual(to_adduct("C6H12O6", "[M+NH4]+"), "C6H16NO6")
    
    def test_from_adduct(self):
        """Test from_adduct function."""
        # Test removing proton
        self.assertEqual(from_adduct("C6H13O6", "[M+H]+"), "C6H12O6")
        
        # Test removing sodium
        self.assertEqual(from_adduct("C6H12NaO6", "[M+Na]+"), "C6H12O6")
        
    def test_adduct_mass(self):
        """Test adduct_mass function."""
        # Test protonated adduct
        self.assertAlmostEqual(adduct_mass("C6H12O6", "[M+H]+"), 181.0701, places=4)
        
        # Test sodium adduct
        self.assertAlmostEqual(adduct_mass("C6H12O6", "[M+Na]+"), 203.0521, places=4)
        
        # Test negative mode adduct
        self.assertAlmostEqual(adduct_mass("C6H12O6", "[M-H]-"), 180.0639, places=4)

if __name__ == '__main__':
    unittest.main() 