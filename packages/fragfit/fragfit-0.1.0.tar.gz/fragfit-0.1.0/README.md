# FragFit

A Python library for handling chemical formulas and mass spectrometry MS2 fragments.

## Features

- Calculate charged and uncharged masses
- Handle different adducts and their effects on formulas and masses
- Find best-fitting formulas for fragments
- Generate all possible subformulas from a parent formula
- Convert between formula strings and element count vectors
- Command-line interface for common operations

## Installation

```bash
pip install fragfit
```

## Usage

### Basic Mass Calculations

```python
from fragfit import charged_mass, uncharged_mass, form_to_mz

# Calculate the mass of a charged ion
mass = charged_mass("H2O", 1)  # Water with +1 charge
print(f"Charged mass: {mass}")

# Calculate m/z value
mz = form_to_mz("C6H12O6", 1)  # Glucose with +1 charge
print(f"m/z: {mz}")
```

### Working with Adducts

```python
from fragfit import adduct_mass, to_adduct, from_adduct

# Calculate mass with sodium adduct
sodium_adduct_mass = adduct_mass("C6H12O6", "[M+Na]+")
print(f"Glucose with sodium adduct: {sodium_adduct_mass}")

# Get formula with adduct
sodium_adduct_formula = to_adduct("C6H12O6", "[M+Na]+")
print(f"Glucose with sodium adduct formula: {sodium_adduct_formula}")
```

### Finding Best-Fit Fragment Formulas

```python
from fragfit import find_best_form

# Find the best formula for a fragment
formula, mass, error = find_best_form(
    mass=180.063,
    parent_form="C10H20O10", 
    tolerance_da=0.01
)

print(f"Best formula: {formula}, Mass: {mass}, Error: {error}")
```

### Generating All Possible Subformulas

```python
from fragfit import generate_all_forms

# Generate all possible subformulas of glucose
all_forms = generate_all_forms("C6H12O6")
print(f"Found {len(all_forms)} possible subformulas")
```

## Command-Line Interface

FragFit includes a command-line interface for common operations:

### Finding the Best Formula for a Mass

```bash
fragfit find-formula 180.063 C10H20O10 --tolerance 0.01
```

### Calculating Mass or m/z

```bash
# Calculate mass with adduct
fragfit calculate-mass C6H12O6 --adduct "[M+Na]+"

# Calculate m/z with charge
fragfit calculate-mass C6H12O6 --charge 1
```

### Working with Adducts

```bash
# Add adduct to formula
fragfit adduct C6H12O6 "[M+Na]+"

# Remove adduct from formula
fragfit adduct C6H12NaO6 "[M+Na]+" --reverse
```

### Listing All Possible Fragments

```bash
# List to stdout
fragfit list-fragments C6H12O6

# Output to CSV
fragfit list-fragments C6H12O6 --csv fragments.csv
```

### Analyzing Mass Spec Data from a CSV File

```bash
fragfit analyze-file spec_data.csv --parent C5H11N --output results.csv
```

## License

MIT

## Author

Gabe Reder <gk@reder.io> 