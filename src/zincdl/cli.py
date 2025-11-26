# zincdl/cli.py


import click
import logging
from .tranche_mappings import (
    MW_MAP,
    LOGP_MAP,
    REACTIVITY_LEVELS,
    PURCHASABILITY_LEVELS,
    PH_MAP,
    CHARGE_MAP,
    PREDEFINED_SUBSETS,
)
from .defaults import DEFAULTS
from .utils import parse_list
from .core import generate_urls
from .download import download_urls, download_tranches


class FormatCommand(click.Command):
    """Custom command that preserves docstring newlines."""

    def format_help(self, ctx, formatter=None):
        formatter = formatter or ctx.make_formatter()
        formatter.width = 120
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_help_text(self, ctx, formatter):
        help_text = (self.help or "").rstrip("\n")
        if help_text:
            click.echo()
            click.echo(help_text)
            click.echo()


@click.command(cls=FormatCommand)
@click.option(
    "--subset",
    default=None,
    show_default=True,
    help=f"Preset subset of MW x logP grid (available: {', '.join(PREDEFINED_SUBSETS.keys())})",
)
@click.option(
    "--mw",
    type=str,
    callback=parse_list,
    default=str(DEFAULTS["mw"]),
    show_default=True,
    help=f"MW bins up to ... (available: {', '.join([str(k) for k in MW_MAP.keys()])})",
)
@click.option(
    "--logp",
    type=str,
    callback=parse_list,
    default=str(DEFAULTS["logp"]),
    show_default=True,
    help=f"logP bins up to ... (available: {', '.join([str(k) for k in LOGP_MAP.keys()])})",
)
@click.option(
    "--reactivity",
    type=click.Choice([n for n, _ in REACTIVITY_LEVELS]),
    default=DEFAULTS["reactivity"],
    show_default=True,
    help=f"Reactivity levels (available: {', '.join([n for n, _ in REACTIVITY_LEVELS])})",
)
@click.option(
    "--purchasability",
    type=click.Choice([n for n, _ in PURCHASABILITY_LEVELS]),
    default=DEFAULTS["purchasability"],
    show_default=True,
    help=f"Purchasability levels (available: {', '.join([n for n, _ in PURCHASABILITY_LEVELS])})",
)
@click.option(
    "--ph",
    type=str,
    callback=parse_list,
    default=str(DEFAULTS["ph"]),
    show_default=True,
    help=f"pH levels (available: {', '.join(PH_MAP.keys())})",
)
@click.option(
    "--charge",
    type=str,
    callback=parse_list,
    default=str(DEFAULTS["charge"]),
    show_default=True,
    help=f"Charge levels (available: {', '.join([str(k) for k in CHARGE_MAP.keys()])})",
)
@click.option(
    "--reac_exclusive",
    type=click.BOOL,
    default=DEFAULTS["reac_exclusive"],
    show_default=True,
    help="Use only the selected reactivity level (True) or cumulative (False).",
)
@click.option(
    "--purch_exclusive",
    type=click.BOOL,
    default=DEFAULTS["purch_exclusive"],
    show_default=True,
    help="Use only the selected purchasability level (True) or cumulative (False).",
)
@click.option(
    "--fmt",
    type=click.Choice(["smi", "txt", "sdf", "mol2", "db2", "pdbqt"]),
    default=DEFAULTS["fmt"],
    show_default=True,
    help="File format to be downloaded.",
)
@click.option("--download", is_flag=True, help="Download the generated tranche files")
@click.option(
    "--out_dir",
    default="downloads/zinc",
    show_default=True,
    help="Output directory for downloads",
)
@click.option("--verbose", is_flag=True, help="Enable verbose logging.")
def main(download, out_dir, verbose, **kwargs):
    """ZINC downloader CLI

    - ZINC tranches are browsable on https://zinc.docking.org/tranches
    - Background on tranche organization: https://wiki.docking.org/index.php/Tranche_Browser

Examples:
    zincdl --subset leadlike --fmt mol2
    zincdl --mw 300,325,350 --logp 2,2.5 --fmt sdf --download
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    for key in ["mw", "logp"]:
        if not kwargs[key]:
            kwargs[key] = None

    urls = generate_urls(**kwargs)

    if download:
        download_urls(urls, out_dir)
        download_tranches(urls, out_dir)


if __name__ == "__main__":
    main()
