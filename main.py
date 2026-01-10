import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
from datetime import datetime, timezone
import logging

LOG_FILE = "log.txt"


def load_base_urls(path: Path):
    base_urls = {}
    with path.open("r") as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        for row in reader:
            base_urls[row[0]] = row[1]

    return base_urls


def fetch_crowd_level(branch: str, base_url: str):
    path = "wp-admin/admin-ajax.php"
    url = urljoin(base_url, path)

    payload = {"action": "cxo_get_crowd_indicator"}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    response = requests.post(url, data=payload, headers=headers, timeout=10)

    response.raise_for_status()
    data = response.json()

    return branch, data["level"]


def get_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def save_results_to_disk(path: Path, results: dict[str, int]):
    timestamp = get_timestamp()

    with path.open("a") as f:
        writer = csv.writer(f)
        for branch, crowd_level in results.items():
            writer.writerow([timestamp, branch, crowd_level])


def setup_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_FILE, mode="a")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


_logger: logging.Logger | None = None


def get_logger():
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger


def fetch_results(base_urls: dict[str, str]) -> dict[str, int]:
    logger = get_logger()
    crowd_levels = {}
    with ThreadPoolExecutor(max_workers=len(base_urls)) as executor:
        future_to_branch = {
            executor.submit(fetch_crowd_level, branch, base_url): branch
            for branch, base_url in base_urls.items()
        }

        for future in as_completed(future_to_branch):
            try:
                branch, crowd_level = future.result()
                crowd_levels[branch] = crowd_level
                logger.info(
                    "Successfully retrieved crowd level for branch '%s'", branch
                )
            except:
                branch = future_to_branch[future]
                logger.exception("Request failed for branch '%s'", branch)

    return crowd_levels


def main():
    logger = get_logger()

    save_dir = Path("results")
    save_dir.mkdir(exist_ok=True)
    save_path = save_dir / "crowd_levels.csv"
    logger.info("Results will be saved to '%s'", save_path)

    base_urls = load_base_urls(Path("base_urls.csv"))
    crowd_levels = fetch_results(base_urls)

    save_results_to_disk(save_path, crowd_levels)


if __name__ == "__main__":
    main()
