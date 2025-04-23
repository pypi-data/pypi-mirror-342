from src.tgedr.ds.pytorch.utils import get_device


def test_get_device():
    actual = get_device()
    assert ("mps" == actual.type) or ("cpu" == actual.type)
