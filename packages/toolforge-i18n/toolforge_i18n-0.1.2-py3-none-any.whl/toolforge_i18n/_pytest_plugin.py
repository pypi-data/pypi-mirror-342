import dataclasses
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Optional, cast

import pytest

from toolforge_i18n._translations import TranslationsConfig, load_translations
from toolforge_i18n._translations_checks import (
    check_message_documentation,
    check_message_formatting,
    check_message_html_elements,
    check_message_keys,
    check_message_variables,
)

translations_config_key = pytest.StashKey[TranslationsConfig]()
translations_key = pytest.StashKey[dict[str, dict[str, str]]]()
documentation_key = pytest.StashKey[dict[str, str]]()
language_code_key = pytest.StashKey[dict[str, str]]()
message_key_key = pytest.StashKey[str]()


def _in_toolforge_i18n(session: pytest.Session) -> bool:
    """Determine whether we’re in toolforge_i18n itself.

    In this case, the plugin should essentially be skipped:
    there’s no tool_translations_config here.
    """
    return session.path.name == 'toolforge_i18n'


def pytest_collection(session: pytest.Session) -> None:
    """Initialize the plugin by loading the translations.

    Tools configure their translations by creating an instance of TranslationsConfig
    and exporting it as the config member of a tool_translations_config module.
    Here, we import the config from there, load the translations and message documentation,
    and stash it all in the pytest session.

    If as a tool developer you get an ImportError from this function,
    you might have forgotten to create a tool_translations_config.py file;
    please see the toolforge_i18n README for instructions.
    """
    if _in_toolforge_i18n(session):
        return

    try:
        import tool_translations_config
    except ModuleNotFoundError:
        # pytest may not have added the session path to the sys.path yet;
        # try to do it now, respecting --import-mode if possible
        # (but with --import-mode=importlib, just add to sys.path anyway,
        # because I don’t know how to use importlib) –
        # improvement suggestions welcome :')
        import sys

        import_mode = session.config.getoption('--import-mode')
        if import_mode == 'append':
            sys.path.append(str(session.path))
        else:
            sys.path.insert(0, str(session.path))
        import tool_translations_config

    translations_config = tool_translations_config.config
    translations, documentation = load_translations(dataclasses.replace(translations_config, check_translations=False))
    session.stash[translations_config_key] = translations_config
    session.stash[translations_key] = translations
    session.stash[documentation_key] = documentation


def pytest_collect_directory(parent: pytest.Directory, path: Path) -> Optional['I18nDirectory']:
    """Custom collection for the i18n directory containing message JSON files."""
    if _in_toolforge_i18n(parent.session):
        return None
    translations_config = parent.session.stash[translations_config_key]
    if path == parent.session.path / translations_config.directory:
        return I18nDirectory.from_parent(parent, path=path)
    return None


class I18nDirectory(pytest.Directory):
    """Custom collector for the i18n directory.

    Collects qqq.json as DocumentationFile,
    and all other JSON files as TranslationsFile.
    Other tests in this directory cannot be collected;
    the collector tries to detect if users put tests there anyway,
    and will warn on test_*.py files or any subdirectories.
    """

    def collect(self) -> Iterable[pytest.Item | pytest.Collector]:
        files: dict[str, pytest.Item | pytest.Collector] = {}
        for direntry in os.scandir(self.path):
            if not direntry.is_file():
                if direntry.is_dir():
                    self.warn(
                        UserWarning(
                            f'Unexpected subdirectory in {self.path}; tests will not be collected here: {direntry.name}'
                        )
                    )
                continue
            path = Path(direntry.path)
            if path.suffix != '.json':
                if path.suffix == '.py' and path.stem.startswith('test_'):
                    self.warn(
                        UserWarning(
                            f'Unexpected test file in {self.path}; tests will not be collected here: {direntry.name}'
                        )
                    )
                continue
            if path.stem == 'qqq':
                files[path.stem] = DocumentationFile.from_parent(self, path=path)
            else:
                files[path.stem] = TranslationsFile.from_parent(self, path=path, language_code=path.stem)
        for stem in sorted(files):
            yield files[stem]


class TranslationsFile(pytest.File):
    """Custom collector for a message JSON file.

    Yields various Functions for the different checks from translations_checks.
    The language code and (where applicable) message key are added to the Function’s stash,
    from where the language_code and mesage_key fixtures (below) later retrieve it.
    """

    def __init__(self, *, path: Path, language_code: str, **kwargs: Any):
        super().__init__(
            path=path,
            **kwargs,
        )
        self.language_code = language_code

    def collect(self) -> Iterable[pytest.Item | pytest.Collector]:
        if self.language_code != 'en':
            fun = pytest.Function.from_parent(
                self,
                name='check_message_keys',
                callobj=check_message_keys,
            )
            fun.stash[language_code_key] = self.language_code  # type: ignore[misc]
            yield fun
        translations = self.session.stash[translations_key]
        for message_key in translations[self.language_code]:
            fun = pytest.Function.from_parent(
                self,
                name=f'check_message_html_elements[{message_key}]',
                callobj=check_message_html_elements,
            )
            fun.stash[language_code_key] = self.language_code  # type: ignore[misc]
            fun.stash[message_key_key] = message_key
            yield fun
            fun = pytest.Function.from_parent(
                self,
                name=f'check_message_variables[{message_key}]',
                callobj=check_message_variables,
            )
            fun.stash[language_code_key] = self.language_code  # type: ignore[misc]
            fun.stash[message_key_key] = message_key
            yield fun
            fun = pytest.Function.from_parent(
                self,
                name=f'check_message_formatting[{message_key}]',
                callobj=check_message_formatting,
            )
            fun.stash[language_code_key] = self.language_code  # type: ignore[misc]
            fun.stash[message_key_key] = message_key
            yield fun


class DocumentationFile(pytest.File):
    """Custom collector for a message documentation JSON file (qqq.json).

    Yields one Function for check_message_documentation.
    """

    def __init__(self, *, path: Path, **kwargs: Any):
        super().__init__(
            path=path,
            **kwargs,
        )

    def collect(self) -> Iterable[pytest.Item | pytest.Collector]:
        yield pytest.Function.from_parent(
            self,
            name='check_message_documentation',
            callobj=check_message_documentation,
        )


@pytest.fixture(scope='session')
def translations_config(request: pytest.FixtureRequest) -> TranslationsConfig:
    """Fixture for the tool translations config."""
    return request.session.stash[translations_config_key]


@pytest.fixture(scope='session')
def translations(request: pytest.FixtureRequest) -> dict[str, dict[str, str]]:
    """Fixture for the tool’s translations."""
    return request.session.stash[translations_key]


@pytest.fixture(scope='session')
def documentation(request: pytest.FixtureRequest) -> dict[str, str]:
    """Fixture for the tool’s documentation messages."""
    return request.session.stash[documentation_key]


@pytest.fixture
def language_code(request: pytest.FixtureRequest) -> str:
    """Fixture for a translation language code.

    Tests can use this fixture,
    together with the translations_config and (optionally) message_key fixtures,
    to implement additional checks for translations.
    The fixture is parameterized and yields all language codes for which translations exist
    (including 'en', but excluding 'qqq').
    """
    # Implementation note: normal tests actually get this fixture from pytest_generate_tests() below;
    # this fixture is only called by the tests added by this plugin,
    # which are added by the custom collectors above and bypass the Metafunc mechanism.
    return cast(str, request.node.stash[language_code_key])


@pytest.fixture
def message_key(request: pytest.FixtureRequest) -> str:
    """Fixture for a translation message key.

    Tests can use this fixture,
    together with the translations_config and language_code fixtures,
    to implement additional checks for translations.
    The fixture is parameterized and yields all message keys defined in the translations;
    if a test uses both language_code and message_key,
    then the test will only be called with combinations of both that exist in the translations
    (i.e. for each language_code, the message_key will skip messages
    that have not been translated into this language code yet).
    """
    # Implementation note: normal tests actually get this fixture from pytest_generate_tests() below;
    # this fixture is only called by the tests added by this plugin,
    # which are added by the custom collectors above and bypass the Metafunc mechanism.
    return cast(str, request.node.stash[message_key_key])


# https://docs.pytest.org/en/latest/how-to/parametrize.html#basic-pytest-generate-tests-example
# the below is not used for our own functions, but supports users’ own additional tests
def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parameterize tests that use language_code and/or message_key.

    This implements the parametrization of the language_code and message_key fixtures,
    as documented above,
    effectively replacing the fixtures themselves for all normal tests
    (after we’ve parametrized the Metafunc here,
    pytest won’t have to call the actual fixture anymore).
    """
    if _in_toolforge_i18n(metafunc.definition.session):
        return
    if 'message_key' in metafunc.fixturenames:
        translations = metafunc.definition.session.stash[translations_key]
        if 'language_code' in metafunc.fixturenames:
            metafunc.parametrize(
                ('language_code', 'message_key'),
                [
                    (language_code, message_key)
                    for language_code in translations
                    for message_key in translations[language_code]
                ],
            )
        else:
            metafunc.parametrize('message_key', translations['en'].keys())
    elif 'language_code' in metafunc.fixturenames:
        translations = metafunc.definition.session.stash[translations_key]
        metafunc.parametrize('language_code', translations.keys())
