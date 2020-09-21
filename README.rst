ResumeCollection
================

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Project
^^^^^^^^^^^^^^^^^^^^^^^^

run following command to set up project.

    $ make upnew

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ make superuser


Postman API docs
^^^^^^^^^^^^^^^^

You can find Postman API docs for using the APIs at the following path

    /resumecollection/docs/api_docs/Resume Collection.postman_collection.json

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy resumecollection

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest
