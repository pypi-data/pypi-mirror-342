# toolforge_i18n

**toolforge_i18n** is a library for making Wikimedia Toolforge tools written in Python translatable.
It’s especially geared towards Flask-based tools,
but should also be usable with other frameworks.

<!-- The entire next section is also included in docs/index.rst; keep them in sync. -->

## Features

- Make your tool translatable into dozens,
  potentially hundreds of languages!

- Easy integration with [translatewiki.net][]
  by reusing MediaWiki message file syntax.

- Full support for the [magic words][]
  `{{GENDER:}}` and `{{PLURAL:}}`,
  as well as for hyperlink syntax (`[url text]`)
  and list formatting.

- By default, support for a MediaWiki-like
  `?uselang=` URL parameter,
  including `?uselang=qqx` to see message keys.

- Correct conversion between MediaWiki language codes
  and HTML language codes / IETF BCP 47 language tags;
  for instance, `?uselang=simple` produces `<html lang="en-simple">`.

- Correct `lang=` and `dir=` in the face of language fallback:
  messages that (due to language fallback) don’t match the surrounding markup
  are automatically wrapped in a `<span>` with the right attributes.
  (Even MediaWiki doesn’t do this!
  Though, admittedly, MediaWiki doesn’t have the luxury of assuming
  that every message can be wrapped in a `<span>` –
  many MediaWiki messages are block elements that would rather need a `<div>`.)

- Includes checks to ensure all translations are safe,
  without unexpected elements (e.g. `<script>`)
  or attributes (e.g. `onclick=`),
  to protect against XSS attacks from translations.
  The tests are automatically registered via a pytest plugin
  and also run at tool initialization time.

## How to use it

See the [documentation](https://toolforge-i18n.readthedocs.io/en/latest/),
especially [the documentation for Flask tools](https://toolforge-i18n.readthedocs.io/en/latest/flask/index.html)
or [for non-Flask tools](https://toolforge-i18n.readthedocs.io/en/latest/other.html)
depending on which framework you use.

Please note that the library is still relatively new
and has not been used by many tools yet.
If anything is unclear or there are problems,
feel free to reach out to the maintainer(s)
and/or [file a task on Phabricator](https://phabricator.wikimedia.org/maniphest/task/edit/form/1/?project=toolforge_i18n).

## License

BSD-3-Clause.

[translatewiki.net]: https://translatewiki.net/
[magic words]: https://www.mediawiki.org/wiki/Special:MyLanguage/Help:Magic_words
[pip-tools]: https://pip-tools.readthedocs.io/en/latest/
