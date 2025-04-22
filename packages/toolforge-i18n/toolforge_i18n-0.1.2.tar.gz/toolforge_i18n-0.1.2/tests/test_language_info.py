from collections.abc import Callable
from typing import Any

import pytest

import toolforge_i18n._user_agent
from toolforge_i18n._language_info import lang_autonym, lang_bcp47_to_mw, lang_dir, lang_fallbacks, lang_mw_to_bcp47

toolforge_i18n._user_agent.set_user_agent(  # noqa: SLF001
    'toolforge-i18n test (https://gitlab.wikimedia.org/lucaswerkmeister/toolforge_i18n/; mail@lucaswerkmeister.de)'
)


@pytest.mark.parametrize(
    'code, expected', [('en', 'English'), ('de', 'Deutsch'), ('fa', 'فارسی'), ('bn-x-Q6747180', None)]
)
def test_lang_autonym(code: str, expected: str | None) -> None:
    assert lang_autonym(code) == expected


@pytest.mark.parametrize('code, expected', [('en', 'en'), ('simple', 'en-simple'), ('unknown', 'unknown')])
def test_lang_mw_to_bcp47(code: str, expected: str) -> None:
    assert lang_mw_to_bcp47(code) == expected


@pytest.mark.parametrize('code, expected', [('en', 'en'), ('en-simple', 'simple'), ('unknown', 'unknown')])
def test_lang_bcp47_to_mw(code: str, expected: str) -> None:
    assert lang_bcp47_to_mw(code) == expected


@pytest.mark.parametrize('code, expected', [('en', 'ltr'), ('fa', 'rtl'), ('unknown', 'auto')])
def test_lang_dir(code: str, expected: str) -> None:
    assert lang_dir(code) == expected


@pytest.mark.parametrize(
    'code, expected',
    [
        ('en', []),
        ('de', []),
        ('de-at', ['de']),
        ('sh', ['sh-latn', 'sh-cyrl', 'bs', 'sr-el', 'sr-latn', 'hr']),
    ],
)
def test_lang_fallbacks(code: str, expected: list[str]) -> None:
    assert lang_fallbacks(code) == expected


@pytest.mark.parametrize(
    'function, parameter, expected',
    [
        (lang_autonym, 'en', 'English'),
        (lang_mw_to_bcp47, 'simple', 'en-simple'),
        (lang_bcp47_to_mw, 'en-simple', 'simple'),
        (lang_dir, 'en', 'ltr'),
    ],
)
def test_no_caching_breakage(
    monkeypatch: pytest.MonkeyPatch,
    function: Callable[[str], str],
    parameter: str,
    expected: str,
) -> None:
    import mwapi  # type: ignore

    import toolforge_i18n._language_info

    # reset globals
    toolforge_i18n._language_info._language_info = None  # type: ignore # noqa: SLF001
    toolforge_i18n._language_info._by_bcp47 = None  # type: ignore # noqa: SLF001

    # simulate network error for first time
    with monkeypatch.context() as m:

        class TestSession(mwapi.Session):  # type: ignore
            def get(*_args: Any, **_kwargs: Any) -> Any:
                raise RuntimeError('simulated network error')

        m.setattr(toolforge_i18n._language_info.mwapi, 'Session', TestSession)  # type: ignore # noqa: SLF001
        with pytest.raises(RuntimeError, match='simulated network error'):
            function(parameter)

    # no network error second time, should work now
    assert function(parameter) == expected
