import random
import typing

import pytest


@pytest.fixture(name="fixed_random_seed")
def fixture_fixed_random_seed() -> typing.Generator[None, None, None]:
    random.seed(42)
    try:
        yield
    finally:
        random.seed()
