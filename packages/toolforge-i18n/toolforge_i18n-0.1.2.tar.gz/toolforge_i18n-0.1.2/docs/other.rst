:gitlab_url: https://gitlab.wikimedia.org/lucaswerkmeister/toolforge_i18n/-/blob/main/docs/other.rst

Using toolforge_i18n in a non-Flask tool
========================================

This section documents how to use toolforge_i18n in a tool that does not use the Flask framework.
The library does not yet include a lot of support for other frameworks,
but it should be possible to make it work.
If you put together a working integration with another framework,
please consider contacting the toolforge_i18n maintainer(s) about adding it to the library.

To set up the tool, you’ll want to follow similar steps as in :doc:`flask/setup`.
Make sure you only add ``toolforge_i18n`` to your dependencies
(without the ``[Flask]`` extra).
The ``tool_translations_config.py`` and ``i18n/`` directory should look the same.
The ``ToolforgeI18n`` and ``message`` imports will both not be available;
instead, you’ll want to import at least :py:func:`load_translations <toolforge_i18n.load_translations>`
and :py:class:`I18nFormatter <toolforge_i18n.I18nFormatter>`::

    from toolforge_i18n import I18nFormatter, load_translations

Somewhere in the initialization code of the tool,
you’ll want to load the translations::

    import tool_translations_config
    translations, documentation = load_translations(tool_translations_config.config)

(You probably won’t need the ``documentation``;
``load_translations`` returns it, but feel free to discard it.)
Skip the step about the ``<html>`` tag –
you might want to do something similar in your tool,
but :py:func:`push_html_lang <toolforge_i18n.push_html_lang>`
and :py:func:`pop_html_lang <toolforge_i18n.pop_html_lang>`
are Flask-specific.

When handling an incoming request,
you’ll need to determine the interface language somehow,
e.g. based on the user’s preferences or the request’s URL parameters and headers.
The functions :py:func:`lang_mw_to_bcp47 <toolforge_i18n.lang_mw_to_bcp47>`
and :py:func:`lang_bcp47_to_mw <toolforge_i18n.lang_bcp47_to_mw>`
may be useful to convert between language codes used by MediaWiki
and ones used by HTML and HTTP.

To use a message,
look up the message string in the ``translations`` based on the request language you determined
(perhaps using :py:func:`lang_fallbacks <toolforge_i18n.lang_fallbacks>` if the message is not defined in that language),
and format it using an :py:class:`I18nFormatter <toolforge_i18n.I18nFormatter>`.
The formatter should be created and used like this::

    # assume `language` is a MediaWiki language code
    formatter = I18nFormatter(
        locale_identifier=tool_translations_config.config.language_code_to_babel(language),
        get_gender=tool_translations_config.config.get_gender,
    )
    # assume `message` is a message string from `translations`
    # optionally, `kwargs` contains message variables
    formatted = formatter.format(message, **kwargs)

If your framework supports integrating with `MarkupSafe <https://markupsafe.palletsprojects.com/>`_,
it’s even better to wrap the ``message`` passed into the ``formatter`` in :py:class:`Markup <markupsafe.Markup>`,
so that unsafe strings in the ``kwargs`` are automatically escaped::

    formatted = cast(Markup, formatter.format(Markup(message), **kwargs))

During ongoing development of the tool,
you’ll want to follow similar steps as in :doc:`flask/development` to work on messages,
except that the :py:func:`message <toolforge_i18n.message>` function is not available –
you’ll have to format messages yourselves, as shown above.
Everything else about the message strings in ``i18n/`` and variable formatting still applies,
as do the remarks on HTML formatting and potentially having to adjust your :py:class:`TranslationsConfig <toolforge_i18n.TranslationsConfig>`;
the section on HTML escaping only applies if you can integrate with MarkupSafe, as mentioned above.
(It’s strongly recommended to use MarkupSafe integration if at all possible.)
