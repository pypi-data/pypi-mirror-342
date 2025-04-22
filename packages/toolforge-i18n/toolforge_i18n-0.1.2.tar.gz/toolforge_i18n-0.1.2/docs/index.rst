:gitlab_url: https://gitlab.wikimedia.org/lucaswerkmeister/toolforge_i18n/-/blob/main/docs/index.rst

toolforge_i18n documentation
============================

**toolforge_i18n** is a library for making Wikimedia Toolforge tools written in Python translatable.
It’s especially geared towards Flask based tools –
if your tool uses Flask, please see :doc:`flask/index`.
If your tool does not use Flask, see :doc:`other`.
You can also review the :doc:`api` at your convenience.

.. The entire next section is also included in README.md; keep them in sync.

Features
--------

- Make your tool translatable into dozens,
  potentially hundreds of languages!

- Easy integration with `translatewiki.net <https://translatewiki.net/>`_
  by reusing MediaWiki message file syntax.

- Full support for the `magic words <https://www.mediawiki.org/wiki/Special:MyLanguage/Help:Magic_words>`_
  ``{{GENDER:}}`` and ``{{PLURAL:}}``,
  as well as for hyperlink syntax (``[url text]``)
  and list formatting.

- By default, support for a MediaWiki-like
  ``?uselang=`` URL parameter,
  including ``?uselang=qqx`` to see message keys.

- Correct conversion between MediaWiki language codes
  and HTML language codes / IETF BCP 47 language tags;
  for instance, ``?uselang=simple`` produces ``<html lang="en-simple">``.

- Correct ``lang=`` and ``dir=`` in the face of language fallback:
  messages that (due to language fallback) don’t match the surrounding markup
  are automatically wrapped in a ``<span>`` with the right attributes.
  (Even MediaWiki doesn’t do this!
  Though, admittedly, MediaWiki doesn’t have the luxury of assuming
  that every message can be wrapped in a ``<span>`` –
  many MediaWiki messages are block elements that would rather need a ``<div>``.)

- Includes checks to ensure all translations are safe,
  without unexpected elements (e.g. ``<script>``)
  or attributes (e.g. ``onclick=``),
  to protect against XSS attacks from translations.
  The tests are automatically registered via a pytest plugin
  and also run at tool initialization time.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   flask/index
   other
