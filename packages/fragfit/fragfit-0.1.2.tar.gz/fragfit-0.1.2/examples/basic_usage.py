#!/usr/bin/env python3
"""
Basic usage examples for the fragfit package.
"""

import pandas as pd
from fragfit import (
    charged_mass,
    uncharged_mass,
    form_to_mz,
    adduct_mass,
    to_adduct,
    from_adduct,
    find_best_form,
    generate_all_forms
)

def basic_mass_calculations():
    """Demonstrate basic mass calculations."""
    print("===== Basic Mass Calculations =====")
    
    # Calculate charged mass
    water_charged = charged_mass("H2O", 1)
    print(f"Water (H2O) with +1 charge: {water_charged:.6f}")
    
    # Calculate uncharged mass
    water_uncharged = uncharged_mass(water_charged, 1)
    print(f"Water (H2O) after removing charge: {water_uncharged:.6f}")
    
    # Calculate m/z
    glucose_mz = form_to_mz("C6H12O6", 1)
    print(f"Glucose (C6H12O6) m/z with +1 charge: {glucose_mz:.6f}")
    print()

def adduct_examples():
    """Demonstrate working with adducts."""
    print("===== Adduct Examples =====")
    
    # Calculate adduct masses
    formulas = ["C6H12O6", "C10H20O5", "C8H10N4O2"]  # Glucose, Example lipid, Caffeine
    adducts = ["[M+H]+", "[M+Na]+", "[M+K]+", "[M-H]-"]
    
    print("Formula\t\tAdduct\t\tMass")
    print("-" * 40)
    
    for formula in formulas:
        for adduct in adducts:
            try:
                mass = adduct_mass(formula, adduct)
                print(f"{formula}\t{adduct}\t{mass:.6f}")
            except Exception as e:
                print(f"{formula}\t{adduct}\tError: {e}")
    
    # Demonstrate formula conversion with adducts
    formula = "C6H12O6"  # Glucose
    adduct = "[M+Na]+"
    
    with_adduct = to_adduct(formula, adduct)
    print(f"\n{formula} with {adduct} = {with_adduct}")
    
    original = from_adduct(with_adduct, adduct)
    print(f"{with_adduct} without {adduct} = {original}")
    print()

def fragment_fitting():
    """Demonstrate fragment fitting."""
    print("===== Fragment Fitting =====")
    
    # Example parent compound (glucose)
    parent = "C6H12O6"
    
    # Generate all possible fragments
    print(f"Generating all possible fragments from {parent}...")
    all_fragments = generate_all_forms(parent)
    print(f"Generated {len(all_fragments)} possible fragments")
    
    # Example fragment masses
    test_masses = [
        60.021,  # C2H4O2
        90.032,  # C3H6O3
        120.042,  # C4H8O4
        150.053,  # C5H10O5
    ]
    
    print("\nFitting fragments to masses:")
    print("Mass\t\tBest Match\tTheoretical Mass\tError (Da)")
    print("-" * 70)
    
    for mass in test_masses:
        best_form, best_mass, error = find_best_form(
            mass=mass,
            parent_form=parent,
            tolerance_da=0.01
        )
        
        print(f"{mass:.6f}\t{best_form}\t\t{best_mass:.6f}\t\t{error:.6f}")
    print()

def analyze_real_data():
    """Analyze example MS2 data from a CSV file."""
    try:
        data = pd.read_csv("test_formulas.csv")
        
        print("===== Example Data Analysis =====")
        print(f"Loaded {len(data)} fragments from CSV file")
        
        # Extract parent formula
        parent_formula = data["Parent Formula"].iloc[0]
        print(f"Parent formula: {parent_formula}")
        
        # Process fragments without formulas
        missing_formulas = data[data["Formula"].isna()]
        if len(missing_formulas) > 0:
            print(f"\nFinding formulas for {len(missing_formulas)} fragments without assigned formulas:")
            print("m/z\t\tIntensity\tBest Match\tTheoretical Mass\tError (Da)")
            print("-" * 80)
            
            for _, row in missing_formulas.iterrows():
                mass = row["m/z"]
                intensity = row["Intensity"]
                
                best_form, best_mass, error = find_best_form(
                    mass=mass,
                    parent_form=parent_formula,
                    tolerance_da=0.01
                )
                
                print(f"{mass:.5f}\t{intensity:.1f}\t\t{best_form}\t\t{best_mass:.5f}\t\t{error:.5f}")
        
    except FileNotFoundError:
        print("Note: test_formulas.csv file not found. Skipping data analysis example.")

if __name__ == "__main__":
    basic_mass_calculations()
    adduct_examples()
    fragment_fitting()
    analyze_real_data() 