# zincdl/core.py


import itertools
import logging
from .defaults import DEFAULTS
from .utils import (
    resolve_map,
    subset_codes,
    make_tranche_code,
    make_tranche_url,
)
from .tranche_mappings import (
    MW_MAP,
    LOGP_MAP,
    REACTIVITY_LEVELS,
    PURCHASABILITY_LEVELS,
    PH_MAP,
    CHARGE_MAP,
    PREDEFINED_SUBSETS,
)
from .download import check_urls

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

BASE_URL = "https://files2.docking.org/3D"


def generate_tranche_codes(
    mw_codes, logp_codes, reac_codes, purch_codes, ph_codes, ch_codes
):
    combos = itertools.product(
        mw_codes, logp_codes, reac_codes, purch_codes, ph_codes, ch_codes
    )
    return [
        make_tranche_code(mw, logp, reac, purch, ph, charge)
        for mw, logp, reac, purch, ph, charge in combos
    ]


def codes_to_urls(codes, fmt="smi", base=BASE_URL):
    return [make_tranche_url(c, fmt=fmt, base=base) for c in codes]


def generate_urls(
    mw=DEFAULTS["mw"],
    logp=DEFAULTS["logp"],
    subset=DEFAULTS["subset"],
    reactivity=DEFAULTS["reactivity"],
    purchasability=DEFAULTS["purchasability"],
    ph=DEFAULTS["ph"],
    charge=DEFAULTS["charge"],
    reac_exclusive=DEFAULTS["reac_exclusive"],
    purch_exclusive=DEFAULTS["purch_exclusive"],
    fmt=DEFAULTS["fmt"],
):
    logger.info("[INFO] Encoding ZINC tranches:")
    if subset:
        logger.info("[INFO] Using predefined subset: %s", subset)
        if subset not in PREDEFINED_SUBSETS:
            raise ValueError(f"[ERROR] Unknown subset {subset}")
        mw = PREDEFINED_SUBSETS[subset]["mw"]
        logp = PREDEFINED_SUBSETS[subset]["logp"]

    mw_codes = resolve_map(MW_MAP, mw)
    logp_codes = resolve_map(LOGP_MAP, logp)
    reac_codes = subset_codes(REACTIVITY_LEVELS, reactivity, reac_exclusive)
    purch_codes = subset_codes(PURCHASABILITY_LEVELS, purchasability, purch_exclusive)
    ph_codes = resolve_map(PH_MAP, ph)
    ch_codes = resolve_map(CHARGE_MAP, charge)

    tranche_codes = generate_tranche_codes(
        mw_codes, logp_codes, reac_codes, purch_codes, ph_codes, ch_codes
    )

    reac_label = f"{reactivity} (exclusive)" if reac_exclusive else reactivity
    purch_label = f"{purchasability} (exclusive)" if purch_exclusive else purchasability

    logger.info(f"  MW             : {mw}")
    logger.info(f"  LogP           : {logp}")
    logger.info(f"  Reactivity     : {reac_label}")
    logger.info(f"  Purchasability : {purch_label}")
    logger.info(f"  pH             : {ph}")
    logger.info(f"  Charge         : {charge}")
    logger.info(f"> # tranches     : {len(tranche_codes)}")

    logger.info(f"\n[INFO] Generating and checking URLs (format: {fmt})")
    urls = codes_to_urls(tranche_codes, fmt, BASE_URL)

    urls_checked = check_urls(urls)
    failed = [(u, ok) for u, ok in urls_checked if ok is not True]
    if failed:
        logger.debug(f"[DEBUG] Failed URLs ({len(failed)}): {[u for u, _ in failed]}")

    urls = [u for u, ok in urls_checked if ok]
    logger.info(f"> # active URLs  : {len(urls)} / {len(tranche_codes)}")

    return urls
