:gitlab_url: https://gitlab.wikimedia.org/lucaswerkmeister/toolforge_i18n/-/blob/main/docs/flask/setup.rst

Setting up toolforge_i18n in a Flask tool
=========================================

This document explains how to start using toolforge_i18n in a Wikimedia Toolforge tool.
It assumes that you already have some source code for a tool,
written in Python using the `Flask <https://flask.palletsprojects.com/>`_ framework
(even if it’s just some boilerplate code that doesn’t do anything yet).
You may have created this tool, for instance,
by following the `My first Flask OAuth tool <https://wikitech.wikimedia.org/wiki/Help:Toolforge/My_first_Flask_OAuth_tool>`_ tutorial.

To start using toolforge_i18n, follow these steps:

- Add ``toolforge_i18n[Flask]`` to your tool’s dependencies.
  The exact location of your dependencies depends on your tool’s setup;
  they may be listed in ``pyproject.toml`` (``dependencies`` in the ``[project]`` section),
  in a ``requirements.in`` file (if using `pip-tools <https://pip-tools.readthedocs.io/>`_),
  in a ``requirements.txt`` file,
  or somewhere else.

- In your tool’s source code,
  add a file ``tool_translations_config.py`` with at least the following contents::

      from toolforge_i18n import TranslationsConfig

      config = TranslationsConfig()

  Later, you may want to customize parts of the :py:class:`TranslationsConfig <toolforge_i18n.TranslationsConfig>`,
  such as the message :py:attr:`variables <toolforge_i18n.TranslationsConfig.variables>`;
  see the class documentation for details.

- Create an ``i18n/`` directory,
  with ``en.json`` and ``qqq.json`` files.
  Initially, both files may look like this:

  .. code-block:: json

    {
        "@metadata": {
            "authors": [
                "<your name here>"
            ]
        }
    }

  Actual messages will be added here :doc:`later <development>`.

- In your tool’s source code (probably ``app.py``),
  add the following import::

      from toolforge_i18n import ToolforgeI18n, message

  And add this line shortly after creating the ``app``
  (which usually looks like ``app = flask.Flask(__name__)``)::

      i18n = ToolforgeI18n(app)

- In all the templates of the tool which contain an ``<html>`` tag,
  change the opening and closing tags to look like this:

  .. code-block:: html+jinja

      <html {{ push_html_lang( g.interface_language_code ) }}>
          <!-- ... -->
      </html{{ pop_html_lang( g.interface_language_code ) }}>

  (Hopefully this is just a single template which all other templates `inherit <https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance>`_;
  in tools created using `cookiecutter-toolforge <https://github.com/lucaswerkmeister/cookiecutter-toolforge/>`_,
  this template is called ``base.html``.)
  This will add ``lang=`` and ``dir=`` attributes to the ``<html>`` tag,
  and messages used subsequently inside the template
  will automatically add those attributes if necessary
  (in case of language fallback).

- Optionally, set up CI for your tool, and run ``pytest`` in it.
  This will automatically run tests that ensure the translations are safe.
  A basic CI setup for tools on Wikimedia GitLab might look like this
  (``.gitlab-ci.yml``):

  .. code-block:: yaml

      stages:
        - test

      variables:
        PYTHONDONTWRITEBYTECODE: "1"
        PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

      test-job:
        stage: test
        image: python:3.11
        cache:
          - key: pip-python-3.11
            paths:
              - .cache/pip
        script:
          - python3 -m pip install -r requirements.txt
          - python3 -m pip install pytest
          - pytest

  See also the :py:attr:`check_translations <toolforge_i18n.TranslationsConfig.check_translations>` flag for ``tool_translations_config``.

Now you should be ready to start :doc:`adding the first messages <development>`.
(Tip: once you’ve started turning parts of the interface into messages,
and are beginning to lose track of which texts are already messages and which are still hard-coded,
load the tool with `?uselang=qqx` –
anything that still looks like normal English text then still needs to be turned into a message.)

Once you have added some messages and otherwise feel ready,
you will then want to `register your project on translatewiki.net <https://translatewiki.net/wiki/Special:MyLanguage/Translating:New_project>`_.
Translatewiki.net will import the initial messages and their documentation from ``i18n/en.json`` and ``i18n/qqq.json``,
start collecting translations from translators,
and periodically export them to other files in ``i18n/`` via merge requests (aka pull requests) to your tool’s code.
(Ideally, those merge requests will run ``pytest`` in CI, as mentioned above.)
You should merge these merge requests and deploy them to Toolforge at your convenience.
