Changelog
=========

0.2.1 (2025-04-18)
------------------

-   This release contains no functional changes, only changes to code style,
    documentation, unit tests, and dependency version bumps.

-   Update supported Python versions to 3.9 through 3.13.

-   Update unit tests to reflect behavioral changes in the GraceDB server.

-   Document and test support for adding a log message and a label at the same
    time.

-   Require requests-gracedb >= 0.2.

0.2.0 (2022-12-06)
------------------

-   Implement GraceDB's new pipeline preferred event API.

0.1.7 (2022-11-28)
------------------

-   Drop support for Python 2.6-3.6, which have reached end-of-life.

-   Add support for Python 3.9-3.11.

-   Modernize Python packaging to `configure Setuptools using pyproject.toml
    <https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html>`_.

0.1.6 (2020-03-18)
------------------

-   Make sure that the file-like objects returned by the
    ``client.events[event_id].files[filename].get()`` and
    ``client.superevents[superevent_id].files[filename].get()`` methods have
    been decompressed if they were sent using HTTP compression.

0.1.5 (2020-03-07)
------------------

-   Add new VOEvent type ``earlywarning``.

0.1.4 (2020-02-27)
------------------

-   Work around a bug in GraceDB where normalization of floating-point GPS
    times to fixed-precision decimal representation is applied to JSON-encoded
    requests but not form-encoded requests. This bug caused superevent API
    requests with GPS times specified with more than 6 decimal places to fail.
    See https://git.ligo.org/lscsoft/gracedb/issues/195.

0.1.2 (2020-02-20)
------------------

-   Fix an argument parsing bug: ``client.superevents.update()`` failed to
    treat the keyword argument ``preferred_event=None`` the same as omission of
    the keyword argument.

0.1.1 (2020-02-11)
------------------

-   Fix Python string formatting syntax so that the package is Python 3.5
    compatible.

0.1.0 (2020-02-04)
------------------

-   Skip unit tests if the user's X.509 certificate is not authorized for
    gracedb-test.ligo.org.

-   Track rename of ligo-requests to requests-gracedb.

-   Address all feedback from Pierre Chanial's code review:
    https://git.ligo.org/emfollow/gracedb-sdk/issues/2

0.0.2 (2019-12-12)
------------------

-   Factor out generic HTTP requests support into a separate package,
    ligo-requests.

-   Rename ``fail_noauth`` keyword argument to ``fail_if_noauth`` for
    consistency with gracedb-client.

0.0.1 (2019-12-08)
------------------

-   Initial release.
