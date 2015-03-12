import pytest

import words


MOCK_PATH = "/my/languages/dict"
MOCK_DICTIONARY = """aaa
aaabbb
aaabbbccc
"""


class TestDictionary:
    def read(self):
        return MOCK_DICTIONARY

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass


def _open_test_dictionary(path):
    assert path == MOCK_PATH
    return TestDictionary()


@pytest.fixture
def fake_dictionary(monkeypatch):
    monkeypatch.setattr("__builtin__.open", _open_test_dictionary)


@pytest.fixture
def mock_cheater(fake_dictionary):
    return words.ScrabbleCheater(MOCK_PATH)


@pytest.fixture(params=[(("bbb"), []),
                        (("aaaa"), ["aaa"]),
                        (("AAAA"), ["aaa"]),
                        (("aaaabbbbbbb"), ["aaabbb", "aaa"])
                       ])
def find_inputs(request):
    return request.param


@pytest.fixture(params=[(("bbb"), ["aaabbb"]), (("z"), [])
                       ])
def suffix_inputs(request):
    return request.param


@pytest.fixture(params=[(("bbb"), []),
                        (("aa"), ["aaabbbccc", "aaabbb", "aaa"])
                       ])
def prefix_inputs(request):
    return request.param


@pytest.fixture(params=[(("bbb"), ["aaabbbccc", "aaabbb"]),
                        (("aa"), ["aaabbbccc", "aaabbb", "aaa"]),
                        (("c"), ["aaabbbccc"]),
                        (("z"), [])
                       ])
def contains_inputs(request):
    return request.param


def test_open_dictionary(mock_cheater):
    expected_words = ["aaa", "aaabbb", "aaabbbccc"]
    assert mock_cheater.words == expected_words


def test_find_words(mock_cheater, find_inputs):
    search, expected_found = find_inputs
    result = mock_cheater.find(search)
    assert result.words == expected_found


def test_find_suffix(mock_cheater, suffix_inputs):
    search, expected_found = suffix_inputs
    result = mock_cheater.ends_with(search)
    assert result.words == expected_found


def test_find_prefix(mock_cheater, prefix_inputs):
    search, expected_found = prefix_inputs
    result = mock_cheater.starts_with(search)
    assert result.words == expected_found


def test_contains(mock_cheater, contains_inputs):
    search, expected_found = contains_inputs
    result = mock_cheater.contains(search)
    assert result.words == expected_found
