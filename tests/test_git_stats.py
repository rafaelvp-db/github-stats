import os
from dotenv import load_dotenv
from github_stats import scrape
import pytest
import glob
import logging

load_dotenv()

@pytest.fixture
def repos():

    repos = scrape.get_repos(github_user = os.environ["GITHUB_USER_ID"])
    return repos


@pytest.fixture
def stats(repos):

    stats = scrape.get_repo_statistics(repos = repos, limit = 10)
    return stats


def test_write_stats(stats):

    logging.info(f"Stats: {stats}")
    output_path = os.environ["OUTPUT_PATH"]
    scrape.save_output(
        result_views = stats[0],
        result_clones = stats[1],
        output_path = output_path
    )

    output_files = glob.glob(f"{output_path}/*.json")
    assert len(output_files) > 0


def test_main():
    scrape.main()




