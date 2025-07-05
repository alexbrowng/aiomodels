"""Global pytest config."""

import os
import random
import secrets

TEST_SEED = os.getenv("TEST_SEED") or secrets.token_hex(8)

random.seed(TEST_SEED)


def pytest_report_header():
    """Adding info in report header."""
    return f"Test seed: {TEST_SEED}"
