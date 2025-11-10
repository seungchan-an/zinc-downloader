# zincdl/cli.py


import click
import asyncio
import logging
from .defaults import DEFAULTS
from .utils import parse_list
from .core import generate_urls
from .download import download_tranches

@click.command()
@click.option("--subset", default=None, help="Preset subset (e.g. leadlike, goldilocks)")
@click.option("--mw", type=str, callback=parse_list, default=str(DEFAULTS["mw"]))
@click.option("--logp", type=str, callback=parse_list, default=str(DEFAULTS["logp"]))
@click.option("--reactivity", default=DEFAULTS["reactivity"])
@click.option("--purchasability", default=DEFAULTS["purchasability"])
@click.option("--ph", type=str, callback=parse_list, default=str(DEFAULTS["ph"]))
@click.option("--charge", type=str, callback=parse_list, default=str(DEFAULTS["charge"]))
@click.option("--reac_exclusive/--no_reac_exclusive", default=DEFAULTS["reac_exclusive"])
@click.option("--purch_exclusive/--no_purch_exclusive", default=DEFAULTS["purch_exclusive"])
@click.option("--fmt", default="smi")
@click.option("--download", is_flag=True, help="Download the generated tranche files")
@click.option("--outdir", default="downloads/zinc", help="Output directory for downloads")
@click.option('--verbose', is_flag=True, help='Enable verbose logging')
def main(download, outdir, verbose, **kwargs):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    for key in ["mw", "logp"]:
        if not kwargs[key]:
            kwargs[key] = None

    urls = generate_urls(**kwargs)

    if download:
        asyncio.run(download_tranches(urls, outdir))


if __name__ == "__main__":
    main()
