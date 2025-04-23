"""Core adduct utilities for mass spectrometry."""

import sys
import numpy as np
import molmass

def parse_adduct(adduct):
    """Parses an adduct string into a list of tuples of atoms and their amounts and the charge of the adduct."""
    d_lookup = {
        # return [(Atom, amount)], charge)

        # Positive mode adducts
        "[M]+": ([], 1),
        "[M+H]+": ([('H', 1)], 1),
        "[M+Na]+": ([('Na', 1)], 1),
        "[M+K]+": ([('K', 1)], 1),
        "[M+NH4]+": ([('N', 1), ("H", 4)], 1),
        "[M+CH3OH+H]+": ([('C', 1), ('H', 5), ('O', 1)], 1),
        "[M+ACN+H]+": ([('C', 2), ('H', 4), ('N', 1)], 1),
        "[M+2H]2+": ([('H', 2)], 2),
        # Negative mode adducts
        "[M]-": ([], -1),
        "[M-H]-": ([('H', -1)], -1),
        "[M-H2O-H]-": ([('H', -3), ('O', -1)], 1),
        "[M+Na-2H]-": ([('Na', 1), ('H', -2)], -1),
        "[M+K-2H]-": ([('K', 1), ('H', -2)], -1),
        "[M+Cl]-": ([('Cl', 1)], -1),
        "[M+FA-H]-": ([('H', 1), ('C', 1), ('O', 2)], -1),
        "[M+HAc-H]-": ([('C', 2), ("H", 3), ("O", 2)], -1),
        "[M-2H]2-": ([('H', -2)], -2)
    }
    if adduct not in d_lookup:
        sys.exit(f"Error - don't know how to parse adduct {adduct}")
    return d_lookup[adduct]

def to_adduct(form, adduct):
    """Computes the chemical formula of the adduct version of a given formula."""
    # Handle the newer molmass API
    composition = molmass.Formula(form).composition()
    fd = {}
    for element in composition:
        fd[element] = composition[element].count
    
    adduct_amends = parse_adduct(adduct)[0]
    for (e, add_e) in adduct_amends:
        if e not in fd:
            fd[e] = 0
        fd[e] += add_e
    if np.any([x < 0 for x in list(fd.values())]):
        raise ValueError(f"Created an impossible formula with {form} and adduct {adduct}")
    res = molmass.Formula(''.join([f"{k}{v}" for k, v in fd.items() if v > 0])).formula
    return res

def from_adduct(form, adduct):
    """Computes the chemical formula of the unadducted version of a given formula."""
    # Handle the newer molmass API
    composition = molmass.Formula(form).composition()
    fd = {}
    for element in composition:
        fd[element] = composition[element].count
        
    adduct_amends = parse_adduct(adduct)[0]
    for (e, add_e) in adduct_amends:
        if e not in fd:
            fd[e] = 0
        fd[e] -= add_e
    if np.any([x < 0 for x in list(fd.values())]):
        sys.exit(f"Error - created an impossible formula with {form} and adduct {adduct}")
    res = molmass.Formula(''.join([f"{k}{v}" for k, v in fd.items() if v > 0])).formula
    return res

def adduct_mass(mass, adduct):
    """Calculates the mass of an ion with an adduct given its uncharged mass and adduct."""
    # Avoid circular imports with local import
    from fragfit.formula.core import charged_mass, form_to_mz
    
    adduct_amends, adduct_charge = parse_adduct(adduct)
    adduct_atoms = ''.join([''.join([x[0] for i in range(x[1])]) for x in adduct_amends])
    if adduct_atoms != '':
        adduct_mass = form_to_mz(adduct_atoms, adduct_charge)
    else:
        adduct_mass = 0.0
    res = charged_mass(mass, adduct_charge)
    res = res + adduct_mass
    return res 