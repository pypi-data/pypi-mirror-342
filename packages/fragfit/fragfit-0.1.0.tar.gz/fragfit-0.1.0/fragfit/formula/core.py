"""Core formula utilities for mass spectrometry."""

import sys
import re
import numpy as np
import molmass
import more_itertools

# Import functions from adducts module to avoid circular imports
from fragfit.adducts.core import adduct_mass, parse_adduct, to_adduct, from_adduct

def charged_mass(mass, charge):
    """Calculates the mass of a charged ion given its uncharged mass and charge."""
    if isinstance(mass, str):
        mass = molmass.Formula(mass).isotope.mass
    em = (-1 * int(charge)) * molmass.ELECTRON.mass
    res = mass + em
    return res

def uncharged_mass(mass, charge):
    """Calculates the mass of an uncharged ion given its charged mass and charge."""
    if isinstance(mass, str):
        mass = molmass.Formula(mass).isotope.mass
    em = int(charge) * molmass.ELECTRON.mass
    res = mass + em
    return res

def form_to_mz(form, charge, adduct=None):
    """Computes the m/z of a charged ion given its chemical formula and charge."""
    if adduct is not None:
        adduct_amends, charge = parse_adduct(adduct)
        form = to_adduct(form, adduct)
    res = charged_mass(molmass.Formula(form).isotope.mass, charge=charge)
    res = abs(res / charge)
    return res

def get_refs(ref_formula="CHNOPSNa"):
    """Returns the reference elements and their masses for a given reference formula."""
    # Handle the newer molmass API
    composition = molmass.Formula(ref_formula).composition()
    ref_elements = list(composition.keys())
    t_masses = np.array([molmass.Formula(x).isotope.mass for x in ref_elements])
    return (ref_elements, t_masses)

def form_to_vec(form, ref_formula="CHNOPSNa"):
    """Converts a chemical formula to a vector of element counts."""
    (ref_elements, _) = get_refs(ref_formula)
    # Handle the newer molmass API
    composition = molmass.Formula(form).composition()
    fd = {}
    for element in composition:
        fd[element] = composition[element].count
    
    for e in ref_elements:
        if e not in fd:
            fd[e] = 0
    return np.array([fd[k] for k in ref_elements])

def vec_to_form(vec, ref_formula="CHNOPSNa"):
    """Converts a vector of element counts to a chemical formula."""
    (ref_elements, _) = get_refs(ref_formula)
    vec = [round(x, 2) for x in vec]
    formula_str = "".join([f"{e}{int(vec[i_e])}" if vec[i_e] >= 0.99 else "" for i_e, e in enumerate(ref_elements)])
    res = molmass.Formula(formula_str).formula
    return res

def generate_all_forms(parent_form):
    """Generates all possible chemical formulas that are subformulas of a given parent formula."""
    # Handle the newer molmass API
    composition = molmass.Formula(parent_form).composition()
    l1 = []
    for element in composition:
        count = composition[element].count
        l1.append([element for x in range(int(count))])
    
    l2 = list(np.concatenate(l1).flat)

    m_forms_tuples = (x for l in range(1, len(l2) + 1) for x in more_itertools.distinct_combinations(l2, l))
    m_forms_tuples_converted = (tuple((molmass.Formula(x).formula for x in t)) for t in m_forms_tuples)
    m_forms = (molmass.Formula("".join(t)) for t in m_forms_tuples_converted)
    
    out_list = [(m.formula, m.isotope.mass) for m in m_forms]
    return out_list

def find_best_forms(mass, all_forms, tolerance_da=0.005, charge=0, verbose=False, du_min=None):
    """Finds the best chemical formulas for a given mass from a list of possible formulas."""
    if charge != 0:
        mass = uncharged_mass(mass, charge)
    found_hits = [(x[0], x[1], abs(x[1] - mass)) for x in all_forms if abs(x[1] - mass) <= tolerance_da]
    output = found_hits
    if len(output) == 0:
        output = [(None, None, None)]
    else:
        output = sorted(output, key=lambda tup: tup[-1])

    if du_min is not None:
        output_filtered = []
        val_table = {}
        for e in ["H", "F", "Cl", "Br", "I", "Li", "Na", "K", "Rb", "Cs"]:
            val_table[e] = 1
        for e in ["O", "S", "Se", "Be", "Mg", "Ca", "Sr", "Ba"]:
            val_table[e] = 2
        for e in ["N", "P", "B", "As", "Sb"]:
            val_table[e] = 3
        for e in ["C", "Si", "Ge", "Sn"]:
            val_table[e] = 4
        for form, th_mass, error in output:
            if form is None:
                continue
            du_form = 0
            # Handle the newer molmass API
            composition = molmass.Formula(form).composition()
            for E in composition:
                nE = composition[E].count
                E_clean = re.sub(r'\d', '', E)  # strip the atom of the isotope label if it has one
                if E_clean in val_table:
                    vE = val_table[E_clean]
                else:
                    vE = 2
                du_form += nE * (vE - 2)
            du_form = 1 + (0.5 * du_form)
            if du_form >= du_min:
                output_filtered.append((form, th_mass, error))
        if len(output_filtered) == 0:
            output_filtered = [(None, None, None)]
        output = output_filtered
    best_forms = [x[0] for x in output]
    th_masses = [x[1] for x in output]
    errors = [x[2] for x in output]
    if charge != 0:
        th_masses = [charged_mass(m, charge) if m else None for m in th_masses]
    output = (best_forms, th_masses, errors)
    return output

def find_best_form(mass, parent_form, tolerance_da=0.005, charge=0, verbose=False, du_min=None):
    """Convenience function to find the best formula for a given mass from a parent formula."""
    all_forms = generate_all_forms(parent_form)
    forms, masses, errors = find_best_forms(mass, all_forms, tolerance_da, charge, verbose, du_min)
    
    # Return the best match (first element)
    if forms[0] is None:
        return None, None, None
    
    return forms[0], masses[0], errors[0] 