from contextlib import suppress as _suppress

with _suppress(ModuleNotFoundError):
    from pytest import register_assert_rewrite as _register_assert_rewrite  # noqa: PT013

    _register_assert_rewrite('toolforge_i18n._translations_checks')

from toolforge_i18n._formatters import (
    CommaSeparatedListFormatter,
    GenderFormatter,
    HyperlinkFormatter,
    I18nFormatter,
    PluralFormatter,
)
from toolforge_i18n._get_gender import get_gender_by_user_name
from toolforge_i18n._language_info import lang_autonym, lang_bcp47_to_mw, lang_dir, lang_fallbacks, lang_mw_to_bcp47
from toolforge_i18n._translations import TranslationsConfig, language_code_to_babel, load_translations
from toolforge_i18n._user_agent import get_user_agent, set_user_agent

with _suppress(ModuleNotFoundError):
    from toolforge_i18n._flask import (
        ToolforgeI18n,
        UnknownMessageWarning,
        add_lang_if_needed,
        interface_language_code_from_request,
        message,
        pop_html_lang,
        push_html_lang,
    )
