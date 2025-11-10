# zincdl/utils.py


def subset_codes(levels, selected, exclusive=False):
    try:
        idx = next(i for i, (n, _) in enumerate(levels) if n == selected)
    except StopIteration:
        raise KeyError(f"Unknown reactivity level '{selected}'")
    codes = [levels[idx][1]] if exclusive else [code for _, code in levels[: idx + 1]]
    return list(dict.fromkeys(codes))


def resolve_map(mapping, key):
    keys = key if isinstance(key, list) else [key]
    codes = []

    for k in keys:
        if isinstance(k, str):
            if k.isdigit():  # "250" -> 250
                k = int(k)
            else:
                try:
                    kf = float(k)
                    if kf in mapping:
                        k = kf  # "2.5" -> 2.5
                except ValueError:
                    pass

        if k not in mapping:
            raise KeyError(f"Unknown key '{k}'")

        v = mapping[k]
        codes.extend(v if isinstance(v, list) else [v])
    return list(dict.fromkeys(codes))


def make_tranche_code(mw, logp, reac, purch, ph, charge):
    return f"{mw}{logp}{reac}{purch}{ph}{charge}"


FORMAT_SUFFIX = {
    "smi": ".smi",
    "txt": ".txt",
    "sdf": ".xaa.sdf.gz",
    "mol2": ".xaa.mol2.gz",
    "db2": ".xaa.db2.gz",
    "pdbqt": ".xaa.pdbqt.gz",
}


def make_tranche_url(code, fmt="smi", base="https://files2.docking.org/3D"):
    fmt = fmt.strip(".").lower()
    if fmt not in FORMAT_SUFFIX:
        raise ValueError(f"[ERROR] Unsupported format: {fmt}")
    subdir = f"{base}/{code[:2]}/{code[2:6]}/{code}"
    return f"{subdir}{FORMAT_SUFFIX[fmt]}"


def parse_list(ctx, param, value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        items = []
        for v in value:
            items.extend(v.split(","))
        return [x.strip() for x in items if x.strip()]
    return [x.strip() for x in value.split(",")]
