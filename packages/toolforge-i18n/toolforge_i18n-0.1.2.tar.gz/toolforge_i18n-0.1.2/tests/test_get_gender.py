from typing import Literal

import pytest

from toolforge_i18n._get_gender import get_gender_by_user_name


@pytest.mark.parametrize(
    'user, expected',
    [
        ('علاء', 'm'),
        ('Harmonia Amanda', 'f'),
        ('Nikki', 'n'),
        (None, 'n'),
    ],
)
def test_get_gender(user: str | None, expected: Literal['m', 'n', 'f']) -> None:
    assert get_gender_by_user_name(user) == expected
