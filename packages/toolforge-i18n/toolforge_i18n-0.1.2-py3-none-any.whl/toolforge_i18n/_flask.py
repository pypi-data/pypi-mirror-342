from collections.abc import Callable
from typing import cast
from warnings import warn

import flask
import werkzeug
from markupsafe import Markup

from toolforge_i18n._formatters import I18nFormatter
from toolforge_i18n._language_info import lang_bcp47_to_mw, lang_dir, lang_fallbacks, lang_mw_to_bcp47
from toolforge_i18n._translations import load_translations


class UnknownMessageWarning(UserWarning):
    """Warning issued by :py:func:`~message` when a message is not defined.

    This warning usually indicates one of two problems:

    1. a typo in the message key
       (whether in the :py:func:`~message` call or in ``i18n/en.json``), or
    2. a message that was not added to ``i18n/en.json`` yet.
    """

    def __init__(self, message_code: str, language_codes: list[str]) -> None:
        """Create the warning. This should only be called within toolforge_i18n.

        message_code is the code (or key) of the message that was not found in the translations;
        language_codes are the translations in which the message was searched for.
        """
        self.message_code = message_code
        self.language_codes: list[str] = []
        for language_code in language_codes:
            if language_code not in self.language_codes:
                self.language_codes.append(language_code)
        message = f'Message {message_code!r} not found in {self.language_codes}'
        super().__init__(message)


def init_html_language_codes() -> None:
    """Initialize the stack of HTML language codes.

    The stack is used to track whether a message needs to be wrapped
    in a new HTML element to set the lang= and dir= attributes,
    or whether it’s in the same language as the surrounding markup.
    It’s maintained by :py:func:`~message`, :py:func:`~push_html_lang` and :py:func:`~pop_html_lang`.
    """
    flask.g.html_language_codes = []


def push_html_lang(language_code: str) -> Markup:
    """Push an HTML language code to the stack.

    Many tools will not need to call this,
    as it’s called by the :py:func:`~message` function automatically.
    However, if you also add localized text from other sources than messages,
    you should call this function with the MediaWiki language code you are using;
    for example, in a Jinja2 template:

    .. code-block:: html+jinja

        <span {{ push_html_lang(label.language) }}>
          {{ label.value }}
        </span{{ pop_html_lang(label.language) }}>
    """
    html_language_code = lang_mw_to_bcp47(language_code)
    flask.g.html_language_codes.append(html_language_code)
    return Markup(r'lang="{}" dir="{}"').format(html_language_code, lang_dir(html_language_code))


def add_lang_if_needed(message: Markup, language_code: str) -> Markup:
    """Wrap the given message in a language-tagged element if necessary.

    Given a (formatted) message in a certain language (MediaWiki language code),
    wrap it in a ``<span>`` with ``lang=`` and ``dir=`` attributes
    if the current language on top of the stack is different.
    Note that :py:func:`~message` calls this function automatically,
    so you generally don’t need to use this function yourself.
    """
    if flask.g.html_language_codes and flask.g.html_language_codes[-1] == language_code:
        return message
    return Markup('<span {}>{}</span{}>').format(push_html_lang(language_code), message, pop_html_lang(language_code))


def pop_html_lang(language_code: str) -> Markup:
    """Pop an HTML language code from the stack.

    See :py:func:`~push_html_lang` for details.
    """
    html_language_code = lang_mw_to_bcp47(language_code)
    assert flask.g.html_language_codes.pop() == html_language_code
    return Markup(r'')


def assert_html_language_codes_empty(response: werkzeug.Response) -> werkzeug.Response:
    """Assert that the stack of HTML language codes is depleted.

    This is called at the end of a request;
    if the assertion fails, some :py:func:`~push_html_lang` call is missing
    a corresponding :py:func:`~pop_html_lang` call.
    """
    assert flask.g.html_language_codes == []
    return response


def interface_language_code_from_request(translations: dict[str, dict[str, str]]) -> str:
    """Default implementation to determine the language code of a request.

    This function supports the ``?uselang=`` URL parameter
    and otherwise determines the language based on the request’s ``Accept-Language`` header.
    You may want to override this method to implement a persistent language preference;
    to keep the features mentioned above,
    your implementation should generally look like this::

        from toolforge_i18n import interface_language_code_from_request

        def interface_language_code(translations):
            # ?uselang= takes precedence if present
            if 'uselang' in flask.request.args:
                return interface_language_code_from_request(translations)
            # try persistent language preference (e.g. from flask.session) next
            # ...
            # finally, fall back to Accept-Language:
            return interface_language_code_from_request(translations)

        # ...later, pass the implementation into ToolforgeI18n:
        i18n = ToolforgeI18n(app, interface_language_code)
    """
    if 'uselang' in flask.request.args:
        return flask.request.args['uselang']
    available_bcp47_languages = [lang_mw_to_bcp47(code) for code in translations]
    best_bcp47_language = flask.request.accept_languages.best_match(available_bcp47_languages, 'en')
    return lang_bcp47_to_mw(best_bcp47_language)


def _message_with_language(message_code: str) -> tuple[Markup, str, bool]:
    interface_language_code = cast(str, flask.g.interface_language_code)
    language_codes = [interface_language_code, *lang_fallbacks(interface_language_code), 'en']
    translations = flask.current_app.extensions['toolforge_i18n'].translations
    for language_code in language_codes:
        try:
            text = translations[language_code][message_code]
        except LookupError:
            continue
        else:
            return Markup(text), language_code, True
    warn(UnknownMessageWarning(message_code, language_codes), stacklevel=4)
    return Markup('⧼{message_code}⧽').format(message_code=message_code), 'qqx', False


def _message_qqx(message_code: str, **kwargs: object) -> Markup:
    message = Markup('(')
    message += message_code
    if kwargs:
        message += ': '
        first = True
        for key, value in kwargs.items():
            if first:
                first = False
            else:
                message += ', '
            message += key
            message += '='
            message += repr(value)
    message += ')'
    return message


def _message(message_code: str, **kwargs: object) -> Markup:
    if flask.g.qqx:
        return _message_qqx(message_code, **kwargs)
    message, language, do_format = _message_with_language(message_code)
    if do_format and kwargs:
        config = flask.current_app.extensions['toolforge_i18n'].config
        formatter = I18nFormatter(
            locale_identifier=config.language_code_to_babel(language),
            get_gender=config.get_gender,
        )
        # I18nFormatter returns Markup given Markup
        message = cast(Markup, formatter.format(message, **kwargs))
    return add_lang_if_needed(message, language)


def message(message_code: str, **kwargs: object) -> Markup:
    """Format an interface message in the user interface language.

    The kwargs may contain (named) arguments,
    using the argument names defined in :py:attr:`~TranslationsConfig.variables`.

    This method is available as a template global, and is usually used there
    (but may also be imported and called from Python code).
    """
    # this function, which is exported for calling from Python code,
    # just adds one stack level before calling _message(),
    # while _message() is directly registered as a template global;
    # this means that the warning from _message_with_language(), with stacklevel=4,
    # will report the tool’s message() call correctly in two scenarios:
    # 1. tool python -> message() -> _message() -> _message_with_language()
    # 2. tool template -> Jinja2 -> _message() -> _message_with_language()
    # (of course, this is somewhat brittle and might break with Jinja2 changes,
    # but it works well enough as of 2024-10-03 under Flask 3.0.3 + Jinja2 3.1.4)
    return _message(message_code, **kwargs)


class ToolforgeI18n:
    """Flask extension for toolforge_i18n.

    Basic usage::

        app = flask.Flask(__name__)
        i18n = ToolforgeI18n(app)
    """

    def __init__(
        self,
        app: flask.Flask | None = None,
        interface_language_code: Callable[[dict[str, dict[str, str]]], str] = interface_language_code_from_request,
    ):
        import tool_translations_config

        self.config = tool_translations_config.config
        self.translations, self.documentation = load_translations(self.config)
        self.interface_language_code = interface_language_code
        if app is not None:
            self.init_app(app)

    def init_app(self, app: flask.Flask) -> None:
        app.extensions['toolforge_i18n'] = self
        app.add_template_global(_message, name='message')
        app.add_template_filter(lang_mw_to_bcp47)
        app.add_template_global(push_html_lang)
        app.add_template_global(pop_html_lang)
        app.before_request(init_html_language_codes)
        app.after_request(assert_html_language_codes_empty)

        @app.before_request
        def init_interface_language_code() -> None:
            interface_language_code = self.interface_language_code(self.translations)
            if interface_language_code == 'qqx':
                flask.g.interface_language_code = 'en'
                flask.g.qqx = True
            else:
                flask.g.interface_language_code = interface_language_code
                flask.g.qqx = False
