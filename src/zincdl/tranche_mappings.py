# zincdl/tranche_mappings.py


# mappings for molecular weight, logP, reactivity, purchasability, pH, and charge
MW_MAP = {
    200: "A",
    250: "B",
    300: "C",
    325: "D",
    350: "E",
    375: "F",
    400: "G",
    425: "H",
    450: "I",
    500: "J",
    ">500": "K",
}

LOGP_MAP = {
    -1: "A",
    0: "B",
    1: "C",
    2: "D",
    2.5: "E",
    3: "F",
    3.5: "G",
    4: "H",
    4.5: "I",
    5: "J",
    ">5": "K",
}

REACTIVITY_LEVELS = [
    ("anodyne", "A"),
    ("bother", "B"),
    ("clean", "C"),
    ("standard", "E"),
    ("mild", "E"),
    ("reactive", "G"),
    ("hot", "I"),
]

PURCHASABILITY_LEVELS = [
    ("base-in-stock", "A"),
    ("in-stock", "B"),
    ("agent", "C"),
    ("wait-ok", "D"),
    ("boutique", "E"),
    ("annotated", "F"),
]

CHARGE_MAP = {-2: "L", -1: "M", 0: "N", 1: "O", 2: "P"}

PH_MAP = {"ref": "R", "mid": "M", "high": "H", "low": "L"}

# presets
PREDEFINED_SUBSETS = {
    "none": {"mw": [], "logp": []},  # explicitly empty subset
    "all": {
        "mw": list(MW_MAP.keys()),
        "logp": list(LOGP_MAP.keys()),
    },
    "shards": {"mw": [200], "logp": list(LOGP_MAP.keys())},
    "fragments": {"mw": [200, 250], "logp": [-1, 0, 1, 2, 2.5, 3, 3.5]},
    "flagments": {"mw": [250, 300, 325], "logp": [-1, 0, 1, 2, 2.5, 3, 3.5]},
    "goldilocks": {"mw": [300, 325, 350], "logp": [2, 2.5, 3]},
    "leadlike": {"mw": [300, 325, 350], "logp": [-1, 0, 1, 2, 2.5, 3, 3.5]},
    "lugs": {
        "mw": [350, 375, 400, 425, 450],
        "logp": [-1, 0, 1, 2, 2.5, 3, 3.5, 4, 4.5],
    },
    "druglike": {
        "mw": [250, 300, 325, 350, 375, 400, 425, 450, 500],
        "logp": [-1, 0, 1, 2, 2.5, 3, 3.5, 4, 4.5, 5],
    },
    "big_n_greasy": {"mw": [500, ">500"], "logp": [4.5, 5, ">5"]},
}
