import warnings
from collections.abc import Callable
from typing import Any, Never

import bs4

import toolforge_i18n._formatters as formatters
from toolforge_i18n._translations import TranslationsConfig


def unused(*_args: object, **_kwargs: object) -> Never:
    raise RuntimeError('This function should not be called!')


def check_message_keys(translations: dict[str, dict[str, str]], language_code: str) -> None:
    """Check for extraneous message keys.

    The translations for the given language should not contain
    any message keys that are not in the English translations.
    """
    language_keys = set(translations[language_code].keys())
    english_keys = set(translations['en'].keys())
    extra_keys = language_keys.difference(english_keys)
    assert not extra_keys


def check_message_documentation(
    translations_config: TranslationsConfig, translations: dict[str, dict[str, str]], documentation: dict[str, str]
) -> None:
    """Check message documentation keys.

    All English messages should have a documentation message,
    and all documentation messages should match an existing English message.
    """
    documented_keys = set(documentation.keys())
    expected_documented_keys = {key for key in translations['en'] if key not in translations_config.derived_messages}
    assert documented_keys == expected_documented_keys


def check_message_html_elements(
    translations_config: TranslationsConfig,
    translations: dict[str, dict[str, str]],
    language_code: str,
    message_key: str,
) -> None:
    """Check HTML elements in the message translation.

    Parses the message as HTML,
    and checks that all the element and attribute names are allowed by the config.

    This test protects against malicious translations.
    If it fails for an English source message after you changed it,
    you probably need to update the tool translations config to allow the element or attribute name.
    If it fails for a translation in another language, you need to be very careful.
    If you are sure that the translation is safe,
    you may want to update the tool translations config in this case as well;
    but if the translation contains HTML that should not be allowed
    (e.g. "script", "style" or "img" elements or any attributes starting with "on"),
    you should not use it and instead revert it on translatewiki.net.
    """
    message = translations[language_code][message_key]
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=bs4.MarkupResemblesLocatorWarning)
        soup = bs4.BeautifulSoup(message, features='html.parser')
    for element in soup.find_all():
        assert element.name in translations_config.allowed_html_elements
        allowed_attributes = (
            translations_config.allowed_html_elements[element.name] | translations_config.allowed_global_attributes
        )
        for attr in element.attrs:
            assert attr in allowed_attributes


def check_message_variables(
    translations_config: TranslationsConfig,
    translations: dict[str, dict[str, str]],
    language_code: str,
    message_key: str,
) -> None:
    """Test that the translation uses variables correctly.

    This test checks that all the variables are used in the translation
    (except that PLURAL and GENDER variables are allowed to be unused if not needed),
    with the right format, and never used with the wrong format.
    The translation isn’t actually formatted in this test.

    See the TranslationConfig.variables docstring
    for the meaning of the different variable names / prefixes.
    """
    message = translations[language_code][message_key]
    for variable in translations_config.variables.get(message_key, []):
        if variable == 'url' or variable.startswith('url_'):
            assert '{' + variable + '!h:' in message
            assert '{' + variable + '!g:' not in message
            assert '{' + variable + '!p:' not in message
            assert '{' + variable + '!l}' not in message
            assert '{' + variable + '}' not in message
        elif variable == 'user_name' or variable.startswith('user_name_'):
            assert '{' + variable + '!g:' in message or '{' + variable not in message
            assert '{' + variable + '!h:' not in message
            assert '{' + variable + '!p:' not in message
            assert '{' + variable + '!l}' not in message
            assert '{' + variable + '}' not in message
        elif variable == 'num' or variable.startswith('num_'):
            assert '{' + variable + '!p:' in message or '{' + variable not in message
            assert '{' + variable + '!h:' not in message
            assert '{' + variable + '!g:' not in message
            assert '{' + variable + '!l}' not in message
            # assert '{' + variable + '}' not in message  # allowed, e.g. {{PLURAL:$1||$1 forms}}
        elif variable == 'list' or variable.startswith('list_'):
            assert '{' + variable + '!l}' in message
            assert '{' + variable + '!h:' not in message
            assert '{' + variable + '!g:' not in message
            assert '{' + variable + '!p:' not in message
            assert '{' + variable + '}' not in message
        else:
            assert '{' + variable + '}' in message
            assert '{' + variable + '!h:' not in message
            assert '{' + variable + '!g:' not in message
            assert '{' + variable + '!p:' not in message
            assert '{' + variable + '!l}' not in message


def check_message_formatting(
    translations_config: TranslationsConfig,
    translations: dict[str, dict[str, str]],
    language_code: str,
    message_key: str,
) -> None:
    """Test that the translation uses variables correctly.

    This test actually formats the translation,
    with example values for different variable formats,
    and makes sure that nothing crashes and the formatted variables appear in the result.

    One of the problems this catches is using a URL variable inside a GENDER variable,
    e.g. in "{{GENDER:$2|Logged in as $1.}}" –
    this does not work because, when the URL in $1 is expanded first,
    a colon inside it (e.g. in "https://...") is misinterpreted as the ":" separator in GENDER.
    Such translations need to be changed,
    e.g. to "{{GENDER:$2|Logged in}} as $1."

    See the TranslationConfig.variables docstring
    for the meaning of the different variable names / prefixes.
    """
    message = translations[language_code][message_key]

    url = 'https://example.com/test?foo=bar#baz'
    assert_contains = []
    get_gender: Callable[[str], str] = unused
    params: dict[str, Any] = {}
    for variable in translations_config.variables.get(message_key, []):
        if variable == 'url' or variable.startswith('url_'):
            params[variable] = url
            assert_contains.append(url)
        elif variable == 'user_name' or variable.startswith('user_name_'):
            get_gender = lambda user_name: 'n'  # noqa: E731, ARG005
            params[variable] = 'User name'
        elif variable == 'num' or variable.startswith('num_'):
            params[variable] = 123
        elif variable == 'list' or variable.startswith('list_'):
            item_1 = formatters.markup_type('<a href="{url}">{variable} A</a>').format(url=url, variable=variable)
            item_2 = formatters.markup_type('<a href="{url}">{variable} B</a>').format(url=url, variable=variable)
            params[variable] = [item_1, item_2]
            assert_contains.append(item_1)
            assert_contains.append(item_2)
        else:
            value = formatters.markup_type('<a href="{url}">{variable}</a>').format(url=url, variable=variable)
            params[variable] = value
            assert_contains.append(value)

    formatter = formatters.I18nFormatter(
        locale_identifier=translations_config.language_code_to_babel(language_code),
        get_gender=get_gender,
    )
    formatted = formatter.format(message, **params)

    for assertion in assert_contains:
        assert assertion in formatted


def check_all_translations(
    translations_config: TranslationsConfig,
    translations: dict[str, dict[str, str]],
    documentation: dict[str, str],
) -> None:
    if not __debug__:
        raise AssertionError(
            'Translation checks are implemented using `assert`; you must run this code without optimization (-O) enabled!'
        )
    check_message_documentation(translations_config, translations, documentation)
    for language_code in translations:
        check_message_keys(translations, language_code)
        for message_key in translations[language_code]:
            check_message_html_elements(translations_config, translations, language_code, message_key)
            check_message_variables(translations_config, translations, language_code, message_key)
            check_message_formatting(translations_config, translations, language_code, message_key)
