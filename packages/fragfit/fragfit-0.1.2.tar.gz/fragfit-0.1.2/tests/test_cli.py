"""
Tests for the CLI module.
"""

import unittest
from unittest.mock import patch
import sys
from io import StringIO

from fragfit.cli import main


class TestCLI(unittest.TestCase):
    """Test cases for CLI functionality."""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_help(self, mock_stdout):
        """Test help command."""
        with self.assertRaises(SystemExit):
            main(['--help'])
        output = mock_stdout.getvalue()
        self.assertIn('FragFit:', output)
        self.assertIn('find-formula', output)
        self.assertIn('calculate-mass', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_calculate_mass(self, mock_stdout):
        """Test calculate-mass command."""
        main(['calculate-mass', 'H2O'])
        output = mock_stdout.getvalue()
        self.assertIn('H2O neutral mass:', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_calculate_mass_with_charge(self, mock_stdout):
        """Test calculate-mass command with charge."""
        main(['calculate-mass', 'H2O', '--charge', '1'])
        output = mock_stdout.getvalue()
        self.assertIn('H2O with charge 1: m/z =', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_calculate_mass_with_adduct(self, mock_stdout):
        """Test calculate-mass command with adduct."""
        main(['calculate-mass', 'H2O', '--adduct', '[M+H]+'])
        output = mock_stdout.getvalue()
        self.assertIn('H2O with [M+H]+:', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_adduct(self, mock_stdout):
        """Test adduct command."""
        main(['adduct', 'H2O', '[M+H]+'])
        output = mock_stdout.getvalue()
        self.assertIn('H2O with [M+H]+:', output)
        self.assertIn('H3O', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_adduct_reverse(self, mock_stdout):
        """Test adduct command with reverse option."""
        main(['adduct', 'H3O', '[M+H]+', '--reverse'])
        output = mock_stdout.getvalue()
        self.assertIn('H3O without [M+H]+:', output)
        self.assertIn('H2O', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_formula(self, mock_stdout):
        """Test find-formula command."""
        main(['find-formula', '18.01', 'H2O', '--tolerance', '0.1'])
        output = mock_stdout.getvalue()
        self.assertIn('Best formula:', output)
        self.assertIn('H2O', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_fragments(self, mock_stdout):
        """Test list-fragments command."""
        main(['list-fragments', 'H2O'])
        output = mock_stdout.getvalue()
        self.assertIn('Formula,Mass', output)
        self.assertIn('H,', output)
        self.assertIn('O,', output)
        self.assertIn('H2,', output)
        self.assertIn('HO,', output)
        self.assertIn('H2O,', output)


if __name__ == '__main__':
    unittest.main() 