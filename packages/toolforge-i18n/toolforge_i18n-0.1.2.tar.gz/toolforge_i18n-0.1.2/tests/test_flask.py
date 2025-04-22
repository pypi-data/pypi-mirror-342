from typing import Any
from unittest.mock import NonCallableMock

import flask
import pytest
from markupsafe import Markup

import toolforge_i18n._user_agent
from toolforge_i18n._flask import (
    UnknownMessageWarning,
    add_lang_if_needed,
    assert_html_language_codes_empty,
    init_html_language_codes,
    interface_language_code_from_request,
    message,
    pop_html_lang,
    push_html_lang,
)

toolforge_i18n._user_agent.set_user_agent(  # noqa: SLF001
    'toolforge-i18n test (https://gitlab.wikimedia.org/lucaswerkmeister/toolforge_i18n/; mail@lucaswerkmeister.de)'
)


@pytest.fixture
def app() -> flask.Flask:
    return flask.Flask(__name__)


def test_html_lang_stack(app: flask.Flask) -> None:
    with app.test_request_context():
        init_html_language_codes()
        assert push_html_lang('en') == Markup('lang="en" dir="ltr"')
        assert push_html_lang('ar') == Markup('lang="ar" dir="rtl"')
        assert pop_html_lang('ar') == Markup('')
        assert pop_html_lang('en') == Markup('')
        response: Any = 'unused argument that should be returned unchanged'
        assert assert_html_language_codes_empty(response) == response


def test_html_lang_stack_wrong_order(app: flask.Flask) -> None:
    with app.test_request_context():
        init_html_language_codes()
        assert push_html_lang('en') == Markup('lang="en" dir="ltr"')
        assert push_html_lang('ar') == Markup('lang="ar" dir="rtl"')
        with pytest.raises(AssertionError):
            pop_html_lang('en')


def test_html_lang_stack_not_empty(app: flask.Flask) -> None:
    with app.test_request_context():
        init_html_language_codes()
        assert push_html_lang('en') == Markup('lang="en" dir="ltr"')
        assert push_html_lang('ar') == Markup('lang="ar" dir="rtl"')
        assert pop_html_lang('ar') == Markup('')
        response: Any = 'unused argument that should be returned unchanged'
        with pytest.raises(AssertionError):
            assert_html_language_codes_empty(response)


def test_add_lang_if_needed(app: flask.Flask) -> None:
    with app.test_request_context():
        init_html_language_codes()
        push_html_lang('en')
        assert add_lang_if_needed(Markup('msg'), 'ar') == Markup('<span lang="ar" dir="rtl">msg</span>')


def test_add_lang_if_needed_unneeded(app: flask.Flask) -> None:
    with app.test_request_context():
        init_html_language_codes()
        push_html_lang('en')
        push_html_lang('ar')
        assert add_lang_if_needed(Markup('msg'), 'ar') == Markup('msg')


def test_interface_language_code_from_request_params(app: flask.Flask) -> None:
    with app.test_request_context('/?uselang=simple'):
        translations: dict[str, dict[str, str]] = {
            'en': {},
            'en-us': {},
            'simple': {},
        }
        assert interface_language_code_from_request(translations) == 'simple'


def test_interface_language_code_from_request_headers(app: flask.Flask) -> None:
    with app.test_request_context(headers=[('Accept-Language', 'de;q=0.9, en-simple;q=0.8, en;q=0.7')]):
        translations: dict[str, dict[str, str]] = {
            'en': {},
            'en-us': {},
            'simple': {},
        }
        assert interface_language_code_from_request(translations) == 'simple'


def test_interface_language_code_from_request_nothing(app: flask.Flask) -> None:
    with app.test_request_context():
        translations: dict[str, dict[str, str]] = {
            'en': {},
            'en-us': {},
            'simple': {},
        }
        assert interface_language_code_from_request(translations) == 'en'


def test_message_unknown(app: flask.Flask) -> None:
    # mock just enough of a real ToolforgeI18n to make message() work for this test;
    # currently this seems easier than using the real ToolforgeI18n,
    # though it might be worth reevaluating this later
    mock_i18n = NonCallableMock()
    mock_i18n.translations = {}
    app.extensions['toolforge_i18n'] = mock_i18n
    with app.test_request_context():
        flask.g.interface_language_code = 'en'
        flask.g.qqx = False
        flask.g.html_language_codes = ['en']
        # warns as expected
        with pytest.warns(UnknownMessageWarning, match=r'Message ["\']foo["\'] not found in \[["\']en["\']\]'):
            assert message('foo') == '<span lang="qqx" dir="auto">⧼foo⧽</span>'
        # does not try to format the unknown message
        with pytest.warns(UnknownMessageWarning):
            msg = message('{bar}', bar='baz')
            assert '{bar}' in msg
            assert 'baz' not in msg
