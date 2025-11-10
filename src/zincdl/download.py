# zincdl/download.py

import os
import aiohttp
import aiofiles
import asyncio
import random
import logging
from tqdm.asyncio import tqdm_asyncio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/122.0 Safari/537.36"
RANGE_HDR = {
    "User-Agent": UA,
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


async def check_url(session, url, timeout=5, retries=3):
    for attempt in range(retries + 1):
        try:
            async with session.head(
                url, headers=RANGE_HDR, timeout=timeout, allow_redirects=True
            ) as r:
                # logger.info(f"[DEBUG] {url} {attempt} -> status {r.status}")
                if r.status in (200, 206):  # OK / partial content
                    return url, True
                if r.status == 404:  # not found
                    return url, False
                if r.status in (
                    408,
                    429,
                    500,
                    502,
                    503,
                    504,
                ):  # temporary or overload
                    wait = ((2**attempt) + random.random()) / 2
                    await asyncio.sleep(wait)
                    continue
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.debug(f"[DEBUG] {url} attempt {attempt} failed: {e}")
            await asyncio.sleep(0.5 * (attempt + 1))
            continue
    return url, None


async def check_urls(urls, max_concurrent=4, timeout=5):
    connector = aiohttp.TCPConnector(
        limit=max_concurrent,
        ttl_dns_cache=300,
        enable_cleanup_closed=True,
        force_close=False,
    )
    timeout_cfg = aiohttp.ClientTimeout(sock_connect=timeout, sock_read=timeout)
    async with aiohttp.ClientSession(
        connector=connector, timeout=timeout_cfg, auto_decompress=False
    ) as session:

        # results = await asyncio.gather(*(check_url(session, u, timeout) for u in urls))
        results = await tqdm_asyncio.gather(
            *(check_url(session, u, timeout) for u in urls),
            total=len(urls),
            desc="[PROGRESS] Checking availability",
            ncols=100,
            dynamic_ncols=False,
        )

        return results


async def download_tranche(session, url, out_dir, chunk_size=8192, retries=3):
    filename = os.path.join(out_dir, os.path.basename(url))
    for attempt in range(retries):
        try:
            async with session.get(url) as r:
                if r.status == 200:
                    async with aiofiles.open(filename, "wb") as f:
                        async for chunk in r.content.iter_chunked(chunk_size):
                            await f.write(chunk)
                            await asyncio.sleep(random.uniform(0, 0.05))
                    return filename, True
        except Exception:
            await asyncio.sleep(0.5 * (attempt + 1))
    return filename, False


async def download_tranches(urls, out_dir="downloads/zinc", max_concurrent=4):
    os.makedirs(out_dir, exist_ok=True)
    connector = aiohttp.TCPConnector(
        limit=max_concurrent,
        ttl_dns_cache=300,
        enable_cleanup_closed=True,
        force_close=False,
    )
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [download_tranche(session, u, out_dir) for u in urls]
        results = []
        for coro in tqdm_asyncio.as_completed(
            tasks,
            total=len(tasks),
            desc="[PROGRESS] Downloading ZINC tranches",
            ncols=100,
            dynamic_ncols=False,
        ):
            result = await coro
            results.append(result)
        return results
