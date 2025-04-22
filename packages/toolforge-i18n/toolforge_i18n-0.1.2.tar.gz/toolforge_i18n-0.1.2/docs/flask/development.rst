:gitlab_url: https://gitlab.wikimedia.org/lucaswerkmeister/toolforge_i18n/-/blob/main/docs/flask/development.rst

Developing a Flask tool using toolforge_i18n
============================================

This document explains how to work with toolforge_i18n during ongoing development of a tool.
It assumes that you already followed the :doc:`initial setup steps <setup>`.

Adding a message
----------------

To add a new message,
you need to add the message itself to ``i18n/en.json``,
document it in ``i18n/qqq.json``,
and then use it using the :py:func:`message <toolforge_i18n.message>` function
in your templates and/or Python code.
(You can do these steps in any order,
but all are needed before the message will work properly.)

To add a new message to the ``i18n/en.json`` file,
edit the file to add a new line with the message key and text,
along with a comma at the end of the previous last entry.
For example:

.. code-block:: json

    {
        "@metadata": {
            "authors": [
                "<your name here>"
            ]
        },
        "new-message-key": "This is the new message."
    }

The message key (``new-message-key`` above)
can be anything, though it’s customary to write it in “kebab case”,
i.e. all lowercase with hyphens to separate words.
You generally don’t need to include a fixed prefix for your tool’s name
(e.g. ``tool-name-new-message-key``) –
this will be handled on translatewiki.net instead.

The message text should be written in English
(toolforge_i18n doesn’t currently support other source languages,
though it might be possible to add support for this later if needed).
In simple messages, you can treat the message text as plain text,
though you may have to escape ``<`` as ``&lt;`` and ``&`` as ``&amp;``.
More complex messages may need variables and/or HTML formatting, as described below.

To document the message in the ``i18n/qqq.json`` file,
edit that file to add a new line with the message key and documentation,
along with a comma at the end of the previous last entry.
For example:

.. code-block:: json

    {
        "@metadata": {
            "authors": [
                "<your name here>"
            ]
        },
        "new-message-key": "This is the documentation for the new message."
    }

The documentation will be shown to translators on translatewiki.net.
It should be written in English,
and can use any Wikitext formatting available on that wiki (including templates).
If you aren’t sure how to document the message,
it’s possible to leave the documentation empty,
though it’s not recommended.

To use the message in the tool,
use the :py:func:`message <toolforge_i18n.message>` function.
Most of the time, you will use it in a template, where it is available automatically:

.. code-block:: html

    <p>
        {{ message('new-message-key') }}
    </p>

But you can also use it in the Python code by importing the function::

    from toolforge_i18n import ToolforgeI18n, message

    # ...

    msg = message('new-message-key')

Variables
---------

Messages can contain variables (also called parameters),
i.e. pieces of information passed into the message by your tool,
similar to variables in MediaWiki messages.

In the message text (``i18n/en.json``),
variables are written as a dollar sign followed by a number,
starting at 1,
just like in MediaWiki:

.. code-block:: json

    "page-not-found": "The page $1 does not exist.",
    "page-not-found-on-wiki": "The page $1 does not exist on $2."

In the message documentation (``i18n/qqq.json``),
it is customary to document the variables and their meaning similar to this:

.. code-block:: json

    "page-not-found-on-wiki": "General documentation for the message.\n\nParameters:\n* $1 - Documentation for the first parameter.\n* $2 - Documentation for the second parameter."

which will look like this when rendered as Wikitext:

    General documentation for the message.

    Parameters:

    * $1 - Documentation for the first parameter.
    * $2 - Documentation for the second parameter.

Next, define names for each variable in the ``tool_translations_config.py``,
by adding or extending :py:attr:`variables <toolforge_i18n.TranslationsConfig.variables>`::

    config = TranslationsConfig(
        variables={
            'page-not-found': ['title'],
            'page-not-found-on-wiki': ['title', 'wiki'],
        },
    )

Then, use these variable names to pass information into the message:

.. code-block:: html+jinja

    {{ message('page-not-found', title='Some title') }}

.. code-block:: python

    title = 'Some title'
    wiki = 'English Wikipedia'
    msg = message('page-not-found-on-wiki', title=title, wiki=wiki)

Variable formatting
-------------------

Some formatting directives are available for variables (most of them taken from MediaWiki):
plural formatting, gender formatting, hyperlink formatting, and list formatting.

Plural formatting uses the `PLURAL magic word <https://translatewiki.net/wiki/Special:MyLanguage/FAQ#PLURAL>`_:

.. code-block:: json

    "search-results": "Found {{PLURAL:$1|0=no results|one result|$1 results.}}"

To enable it, the name defined in :py:attr:`variables <toolforge_i18n.TranslationsConfig.variables>`
must either be ``num`` or begin with ``num_``::

    config = TranslationsConfig(
        variables={
            'search-results': ['num_results'],
        },
    )

.. code-block:: html+jinja

    {{ message('search-results', num_results=results | length) }}

Other plural forms in non-English languages (e.g. `dual <https://en.wikipedia.org/wiki/Dual_(grammatical_number)>`_ in some languages)
are supported as long as `Babel <https://pypi.org/project/Babel/>`_ supports them.

Gender formatting uses the `GENDER magic word <https://translatewiki.net/wiki/Special:MyLanguage/Gender>`_:

.. code-block:: json

    "contact-user": "Leave a message on {{GENDER:$1|his|her|their}} talk page."

To enable it, the name defined in :py:attr:`variables <toolforge_i18n.TranslationsConfig.variables>`
must either be ``user_name`` or begin with ``user_name_``::

    config = TranslationsConfig(
        variables={
            'contact-user': ['user_name'],
        },
    )

.. code-block:: html+jinja

    {{ message('contact-user', user_name='Some user name') }}

Often, the English message will use a user name in a way that does not require gender formatting in English,
e.g. in a “Logged in as *user name*” message.
However, some other languages will still need gender formatting in their translation.
In this case, it is customary to use ``GENDER`` in the English message text,
even if it is not actually needed in English,
as a hint to translators that it is available:

.. code-block:: json

    "logged-in": "{{GENDER:$1|Logged in}} as $1."

Then, languages which need the magic word, such as Italian, can use it:

.. code-block:: json

    "loggged-in": "{{GENDER:$1|Acceduto|Acceduta|Acceduto/a}} come $1."

And languages which don’t need it, such as German, can leave it out:

.. code-block:: json

    "logged-in": "Eingeloggt als $1."

(Though translators may not be aware of this and still use the magic word:

.. code-block:: json

    "logged-in": "{{GENDER:$1|Eingeloggt}} als $1."

This is unneeded, but harmless.)

Hyperlink formatting uses the same syntax as external links in MediaWiki,
i.e. the link URL and text, separated by a space and wrapped in one pair of square brackets.
The link URL should be a variable:

.. code-block:: json

    "login-hint": "You need to [$1 log in] before using this tool.",
    "policies": "Development of this tool is covered by the [$1 Universal Code of Conduct], the [$2 Code of Conduct for Wikimedia’s Technical Spaces] and the [$3 Friendly Space Policy]."

To enable it, the name defined in :py:attr:`variables <toolforge_i18n.TranslationsConfig.variables>`
must either be ``url`` or begin with ``url_``::

    config = TranslationsConfig(
        variables={
            'login-hint': ['url'],
            'policies': ['url_ucoc', 'url_coc', 'url_fsp'],
        },
    )

The URL may be dynamically generated
(e.g. a URL for another page of your tool, using :py:func:`url_for <flask.url_for>`),
or may simply be hard-coded in the template:

.. code-block:: html+jinja

    {{ message('login-hint', url=url_for('login')) }}
    {{ message('policies',
      url_ucoc='https://meta.wikimedia.org/wiki/Universal_Code_of_Conduct',
      url_coc='https://www.mediawiki.org/wiki/Code_of_Conduct',
      url_fsp='https://foundation.wikimedia.org/wiki/Friendly_space_policy') }}

List formatting has no special MediaWiki syntax,
but may be useful in some tools;
it can be used to format a list of values,
e.g. ``['a', 'b', 'c']`` will be formatted to “a, b, and c” in English.
In the message source, the variable is used without any magic word:

.. code-block:: json

    "see-also": "See also: $1"

To enable it, the name defined in :py:attr:`variables <toolforge_i18n.TranslationsConfig.variables>`
must either be ``list`` or begin with ``list_``::

    config = TranslationsConfig(
        variables={
            'see-also': ['list'],
        },
    )

.. code-block:: html+jinja

    {{ message('see-also', list=alternatives) }}

HTML formatting
---------------

If the message needs some formatting not covered by the previous section
(i.e., anything other than plural, gender, hyperlink or list formatting),
the formatting needs to be written in HTML.
(Wikitext formatting is not supported!)
For instance, an emphasized word would be written like this:

.. code-block:: json

    "message-with-emphasis": "This is the <em>new</em> message."

If you use HTML elements in your messages, you will probably also need to update your ``tool_translations_config.py``.
By default, only a very limited set of element and attribute names is allowed in messages;
this ensures that translations don’t cause problems by adding unexpected HTML markup.
New element names will need to be added to :py:attr:`allowed_html_elements <toolforge_i18n.TranslationsConfig.allowed_html_elements>`,
and attribute names should be added either there or in :py:attr:`allowed_global_attributes <toolforge_i18n.TranslationsConfig.allowed_global_attributes>`
depending on whether the attributes are specific to a certain element or not.
For example::

    config = TranslationsConfig(
        allowed_html_elements={
            'em': set(),  # the <em> element is allowed but with no special attributes
            'abbr': {'title'},  # the <abbr> element is allowed to have a title= attribute
        },
    )

(Most tools should not need to change the default ``allowed_global_attributes``, which are ``dir`` and ``lang``.)

If possible, it’s often better to keep the formatting out of the message.
For instance, if the message should be shown as part of an “alert” box,
the markup for this should be included in the template,
and the message should only contain the text inside.

.. code-block:: html+jinja

    <div class="alert alert-info">
        {{ message('some-alert') }}
    </div>

.. code-block:: json

   "some-alert": "Some alert message without HTML formatting"

However, if only part of the message should be formatted,
the formatting should be included in the message,
as shown in ``message-with-emphasis`` above.
`“Patchwork” or “lego” messages <https://www.mediawiki.org/wiki/Help:System_message#Avoid_fragmented_or_%22patchwork%22_messages>`_,
as in the following example, are strongly discouraged:

.. code-block:: html+jinja

    <!-- do not do this -->
    {{ message('msg1') }}<em>{{ message('msg2') }}</em>{{ message('msg3') }}

.. code-block:: json

    // do not do this
    "msg1": "This is the ",
    "msg2": "new",
    "msg3": " message."

HTML escaping
-------------

To ensure that formatted messages are safe to include in the tool’s HTML output,
and prevent `cross-site scripting (XSS) <https://en.wikipedia.org/wiki/Cross-site_scripting>`_ attacks,
toolforge_i18n uses and integrates with the `MarkupSafe <https://markupsafe.palletsprojects.com/>`_ library.
Translations are loaded as :py:class:`Markup <markupsafe.Markup>`, marking them as safe;
as mentioned above, toolforge_i18n automatically checks during message loading
that only allowed element names and attribute names are used.
(See also :py:attr:`check_translations <toolforge_i18n.TranslationsConfig.check_translations>`.)

When messages are formatted by the :py:func:`message <toolforge_i18n.message>` function
(using :py:func:`I18nFormatter <toolforge_i18n.I18nFormatter>` internally),
any non-``Markup`` arguments are automatically escaped.
This means that regular strings are safe to pass into messages:
With a message like

.. code-block:: json

    "msg": "$1"

and code like

.. code-block:: html+jinja

    {{ message('msg', param='<>') }}

the angle brackets will be escaped as ``&lt;&gt;``,
and look like plain angle brackets when rendered in a browser.

If you actually want to pass HTML into a message,
make sure to wrap it in ``Markup`` to mark it as markup that should not be escaped.
For example, if you want a “logged in” message to show the user name as a link
(the earlier example was simplified to only show it as plain text),
it might look like this:

.. code-block:: json

    "logged-in": "{{GENDER:$2|Logged in}} as $1."

.. code-block:: python

    config = TranslationsConfig(
        variables={
            'logged-in': ['user_link', 'user_name'],
        },
    )

.. code-block:: python

    user_name = 'Example'  # usually not hard-coded
    user_link = Markup(
        '<a href="https://meta.wikimedia.org/wiki/User:{}"><bdi>{}</bdi></a>'
    ).format(user_name.replace(' ', '_'), user_name)
    login_message = message('logged-in', user_name=user_name, user_link=user_link)

This example also demonstrates a few other things:

* MarkupSafe itself automatically escapes the user name when we call `Markup.format <https://markupsafe.palletsprojects.com/en/latest/formatting/#format-method>`_.
* The ``GENDER`` magic word requires the plain user name, so we use two variables, one for the user name and one for the link.
