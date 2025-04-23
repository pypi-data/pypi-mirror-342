import convomeld.api
import doctest


def test_api_doctests():
    failed, attempted = doctest.testmod(convomeld.api)
    assert attempted > 0 and failed == 0
