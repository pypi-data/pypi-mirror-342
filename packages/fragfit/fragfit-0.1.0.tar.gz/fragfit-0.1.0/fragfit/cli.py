#!/usr/bin/env python3
"""Command-line interface for the fragfit package."""

import argparse
import csv
import sys
from typing import List, Optional, Tuple

import pandas as pd

from fragfit import (
    charged_mass,
    uncharged_mass,
    form_to_mz,
    adduct_mass,
    parse_adduct,
    to_adduct,
    from_adduct,
    find_best_form,
    generate_all_forms,
)


def create_parser() -> argparse.ArgumentParser:
    """Create a command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="FragFit: Utilities for chemical formulas and mass spectrometry MS2 fragments"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # find-formula command
    find_formula = subparsers.add_parser(
        "find-formula", help="Find the best formula for a given mass and parent formula"
    )
    find_formula.add_argument("mass", type=float, help="Mass to find formula for")
    find_formula.add_argument("parent", help="Parent formula")
    find_formula.add_argument(
        "--tolerance", type=float, default=0.01, help="Mass tolerance in Da (default: 0.01)"
    )
    find_formula.add_argument(
        "--charge", type=int, default=0, help="Charge state (default: 0)"
    )
    find_formula.add_argument(
        "--min-du", type=float, help="Minimum degree of unsaturation"
    )
    
    # calculate-mass command
    calc_mass = subparsers.add_parser(
        "calculate-mass", help="Calculate mass or m/z for a formula"
    )
    calc_mass.add_argument("formula", help="Chemical formula")
    calc_mass.add_argument(
        "--charge", type=int, default=0, help="Charge state (default: 0)"
    )
    calc_mass.add_argument(
        "--adduct", help="Adduct (e.g., '[M+H]+', '[M+Na]+', '[M-H]-')"
    )
    
    # adduct command
    adduct_parser = subparsers.add_parser(
        "adduct", help="Work with adducts"
    )
    adduct_parser.add_argument("formula", help="Chemical formula")
    adduct_parser.add_argument("adduct", help="Adduct (e.g., '[M+H]+', '[M+Na]+')")
    adduct_parser.add_argument(
        "--reverse", action="store_true", help="Remove adduct from formula"
    )
    
    # list-fragments command
    list_frags = subparsers.add_parser(
        "list-fragments", help="List all possible fragments of a parent formula"
    )
    list_frags.add_argument("parent", help="Parent formula")
    list_frags.add_argument(
        "--csv", help="Output CSV file (default: stdout)"
    )
    
    # analyze-file command
    analyze_file = subparsers.add_parser(
        "analyze-file", help="Analyze mass spec data from a CSV file"
    )
    analyze_file.add_argument("file", help="CSV file with mass spec data")
    analyze_file.add_argument(
        "--parent", help="Parent formula (if not specified in the file)"
    )
    analyze_file.add_argument(
        "--mass-column", default="m/z", help="Column name for mass values (default: 'm/z')"
    )
    analyze_file.add_argument(
        "--tolerance", type=float, default=0.01, help="Mass tolerance in Da (default: 0.01)"
    )
    analyze_file.add_argument(
        "--output", help="Output CSV file (default: stdout)"
    )
    
    return parser


def find_formula_cmd(args) -> None:
    """Run the find-formula command."""
    formula, mass, error = find_best_form(
        mass=args.mass,
        parent_form=args.parent,
        tolerance_da=args.tolerance,
        charge=args.charge,
        du_min=args.min_du
    )
    
    if formula is None:
        print(f"No formula found within {args.tolerance} Da of {args.mass}")
        return
    
    print(f"Best formula: {formula}")
    print(f"Theoretical mass: {mass:.6f}")
    print(f"Error (Da): {error:.6f}")


def calculate_mass_cmd(args) -> None:
    """Run the calculate-mass command."""
    if args.adduct:
        mass = adduct_mass(args.formula, args.adduct)
        print(f"{args.formula} with {args.adduct}: {mass:.6f}")
    elif args.charge != 0:
        mz = form_to_mz(args.formula, args.charge)
        print(f"{args.formula} with charge {args.charge}: m/z = {mz:.6f}")
    else:
        mass = charged_mass(args.formula, 0)
        print(f"{args.formula} neutral mass: {mass:.6f}")


def adduct_cmd(args) -> None:
    """Run the adduct command."""
    if args.reverse:
        result = from_adduct(args.formula, args.adduct)
        print(f"{args.formula} without {args.adduct}: {result}")
    else:
        result = to_adduct(args.formula, args.adduct)
        print(f"{args.formula} with {args.adduct}: {result}")


def list_fragments_cmd(args) -> None:
    """Run the list-fragments command."""
    fragments = generate_all_forms(args.parent)
    
    # Prepare data for output
    data = [["Formula", "Mass"]]
    for formula, mass in fragments:
        data.append([formula, f"{mass:.6f}"])
    
    # Output to CSV or stdout
    if args.csv:
        with open(args.csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"Wrote {len(fragments)} fragments to {args.csv}")
    else:
        for row in data:
            print(",".join(row))


def analyze_file_cmd(args) -> None:
    """Run the analyze-file command."""
    try:
        data = pd.read_csv(args.file)
        
        # Get parent formula
        parent_formula = args.parent
        if parent_formula is None:
            if "Parent Formula" in data.columns:
                parent_formula = data["Parent Formula"].iloc[0]
            else:
                print("Error: Parent formula not specified and not found in file")
                return
        
        # Process mass values
        results = []
        for _, row in data.iterrows():
            if args.mass_column not in row:
                print(f"Error: Mass column '{args.mass_column}' not found in file")
                return
            
            mass = row[args.mass_column]
            formula, th_mass, error = find_best_form(
                mass=mass,
                parent_form=parent_formula,
                tolerance_da=args.tolerance
            )
            
            # Prepare result row
            result = dict(row)
            result["Calculated Formula"] = formula
            result["Theoretical Mass"] = th_mass
            result["Error (Da)"] = error
            results.append(result)
        
        # Convert to DataFrame
        results_df = pd.DataFrame(results)
        
        # Output
        if args.output:
            results_df.to_csv(args.output, index=False)
            print(f"Wrote results to {args.output}")
        else:
            print(results_df.to_string())
    
    except Exception as e:
        print(f"Error: {e}")


def main(args: Optional[List[str]] = None) -> int:
    """Run the command-line interface."""
    parser = create_parser()
    args = parser.parse_args(args)
    
    if args.command is None:
        parser.print_help()
        return 1
    
    # Dispatch to the appropriate command
    if args.command == "find-formula":
        find_formula_cmd(args)
    elif args.command == "calculate-mass":
        calculate_mass_cmd(args)
    elif args.command == "adduct":
        adduct_cmd(args)
    elif args.command == "list-fragments":
        list_fragments_cmd(args)
    elif args.command == "analyze-file":
        analyze_file_cmd(args)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 