# noqa: INP001
import sys

import pytest


def test_metadata() -> None:
    if sys.version_info < (3, 11):
        with pytest.raises(FutureWarning):
            from ozi_spec import METADATA
    else:
        from ozi_spec import METADATA
    METADATA.asdict()
