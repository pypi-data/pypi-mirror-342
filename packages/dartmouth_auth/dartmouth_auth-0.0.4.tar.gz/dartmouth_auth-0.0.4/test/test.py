import dartmouth_auth


def test_get_jwt():
    jwt = dartmouth_auth.get_jwt()
    assert jwt is not None


if __name__ == "__main__":
    test_get_jwt()
