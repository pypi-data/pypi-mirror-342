"""Fragfit - Utilities for handling chemical formulas in the context of mass spectrometry."""

from fragfit.version import (
    __version__,
    __author__,
    __license__,
    __description__
)

# Import main functions to the top level
from fragfit.formula import (
    charged_mass,
    uncharged_mass,
    form_to_mz,
    form_to_vec,
    vec_to_form,
    find_best_form,
    generate_all_forms,
    find_best_forms
)

from fragfit.adducts import (
    adduct_mass,
    parse_adduct,
    to_adduct,
    from_adduct
) 