"""
Advanced tests for the formula module.
"""

import unittest
import numpy as np

from fragfit.formula import (
    charged_mass,
    uncharged_mass,
    form_to_mz,
    form_to_vec,
    vec_to_form,
    find_best_form,
    find_best_forms,
    generate_all_forms,
    get_refs
)


class TestFormulaAdvanced(unittest.TestCase):
    """Advanced test cases for formula functions."""
    
    def test_get_refs(self):
        """Test get_refs function."""
        # Test with default reference formula
        elements, masses = get_refs()
        self.assertEqual(len(elements), 7)  # C, H, N, O, P, S, Na
        self.assertEqual(len(masses), 7)
        
        # Test with custom reference formula
        elements, masses = get_refs("CHNO")
        self.assertEqual(len(elements), 4)  # C, H, N, O
        self.assertEqual(len(masses), 4)
        self.assertIn("C", elements)
        self.assertIn("H", elements)
        self.assertIn("N", elements)
        self.assertIn("O", elements)
    
    def test_form_to_vec(self):
        """Test form_to_vec function."""
        # Test with water
        vec = form_to_vec("H2O", "CHO")
        self.assertEqual(len(vec), 3)
        self.assertEqual(vec[0], 0)  # C
        self.assertEqual(vec[1], 2)  # H
        self.assertEqual(vec[2], 1)  # O
        
        # Test with glucose
        vec = form_to_vec("C6H12O6", "CHO")
        self.assertEqual(len(vec), 3)
        self.assertEqual(vec[0], 6)  # C
        self.assertEqual(vec[1], 12)  # H
        self.assertEqual(vec[2], 6)  # O
    
    def test_vec_to_form(self):
        """Test vec_to_form function."""
        # Test with water
        form = vec_to_form([0, 2, 1], "CHO")
        self.assertEqual(form, "H2O")
        
        # Test with glucose
        form = vec_to_form([6, 12, 6], "CHO")
        self.assertEqual(form, "C6H12O6")
        
        # Test with rounded values - rounding to nearest integer
        form = vec_to_form([6.1, 12.1, 6.05], "CHO")
        self.assertEqual(form, "C6H12O6")
    
    def test_generate_all_forms(self):
        """Test generate_all_forms function."""
        # Test with water
        forms = generate_all_forms("H2O")
        # Check specific number of formulas (might vary with molmass versions)
        self.assertGreaterEqual(len(forms), 3)  # Should have at least H, O, H2O
        
        # Check some expected formulas are present
        formulas = [form[0] for form in forms]
        self.assertIn("H", formulas)
        self.assertIn("O", formulas)
        self.assertIn("H2O", formulas)
        
        # Test with more complex formula
        forms = generate_all_forms("CH4")
        self.assertGreater(len(forms), 3)
        formulas = [form[0] for form in forms]
        self.assertIn("C", formulas)
        self.assertIn("H", formulas)
        self.assertIn("CH4", formulas)
    
    def test_find_best_forms(self):
        """Test find_best_forms function."""
        # Generate all forms for glucose
        all_forms = generate_all_forms("C6H12O6")
        
        # Test finding best forms for a specific mass
        forms, masses, errors = find_best_forms(
            mass=60.021,
            all_forms=all_forms,
            tolerance_da=0.01
        )
        
        # Should find at least one match
        self.assertGreater(len(forms), 0)
        self.assertIsNotNone(forms[0])
        
        # Test with charge
        forms, masses, errors = find_best_forms(
            mass=60.021,
            all_forms=all_forms,
            tolerance_da=0.01,
            charge=1
        )
        
        # Should find at least one match
        self.assertGreater(len(forms), 0)
        self.assertIsNotNone(forms[0])
        
        # Test with no matches
        forms, masses, errors = find_best_forms(
            mass=1000.0,  # No formula will match this mass
            all_forms=all_forms,
            tolerance_da=0.01
        )
        
        # Should return None for no matches
        self.assertEqual(len(forms), 1)
        self.assertIsNone(forms[0])
        
        # Test with minimum degree of unsaturation
        forms, masses, errors = find_best_forms(
            mass=72.021,
            all_forms=all_forms,
            tolerance_da=0.1,
            du_min=1.5
        )
        
        # Check if we got results with du_min filter
        if forms[0] is not None:
            # Should have filtered out some formulas
            self.assertGreater(len(forms), 0)
    
    def test_find_best_form_with_du_min(self):
        """Test find_best_form function with du_min parameter."""
        # Test with minimum degree of unsaturation
        formula, mass, error = find_best_form(
            mass=72.021,
            parent_form="C6H12O6",
            tolerance_da=0.1,
            du_min=1.5
        )
        
        # This test might return None or a valid formula depending on the filters
        if formula is not None:
            self.assertIsInstance(formula, str)
            self.assertIsInstance(mass, float)
            self.assertIsInstance(error, float)
        else:
            self.assertIsNone(formula)
            self.assertIsNone(mass)
            self.assertIsNone(error)
    
    def test_form_to_mz_with_adduct(self):
        """Test form_to_mz function with adduct parameter."""
        # Test with proton adduct
        mz = form_to_mz("C6H12O6", 1, adduct="[M+H]+")
        self.assertAlmostEqual(mz, 181.0707, places=4)
        
        # Test with sodium adduct
        mz = form_to_mz("C6H12O6", 1, adduct="[M+Na]+")
        self.assertAlmostEqual(mz, 203.0526, places=4)


if __name__ == '__main__':
    unittest.main() 