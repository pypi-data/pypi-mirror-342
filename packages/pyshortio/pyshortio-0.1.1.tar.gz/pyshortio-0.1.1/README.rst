
.. image:: https://readthedocs.org/projects/pyshortio/badge/?version=latest
    :target: https://pyshortio.readthedocs.io/en/latest/
    :alt: Documentation Status

.. .. image:: https://github.com/MacHu-GWU/pyshortio-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/pyshortio-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/pyshortio-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/pyshortio-project

.. image:: https://img.shields.io/pypi/v/pyshortio.svg
    :target: https://pypi.python.org/pypi/pyshortio

.. image:: https://img.shields.io/pypi/l/pyshortio.svg
    :target: https://pypi.python.org/pypi/pyshortio

.. image:: https://img.shields.io/pypi/pyversions/pyshortio.svg
    :target: https://pypi.python.org/pypi/pyshortio

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/pyshortio-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/pyshortio-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://pyshortio.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/pyshortio-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/pyshortio-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/pyshortio-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/pyshortio#files


Welcome to ``pyshortio`` Documentation
==============================================================================
.. image:: https://pyshortio.readthedocs.io/en/latest/_static/pyshortio-logo.png
    :target: https://pyshortio.readthedocs.io/en/latest/

PyShortIO provides a clean, well-documented API client for the `Short.io <https://short.io/>`_ URL shortening service with comprehensive error handling and pagination support. It follows Pythonic design principles to make URL shortening operations intuitive and efficient.


Quick Start
------------------------------------------------------------------------------
.. code-block:: python

    from pyshortio.api import Client

    # Initialize client with your API token
    client = Client(token="your_api_token")

    # Get your domain
    response, domain = client.get_domain_by_hostname("your-domain.short.gy")
    domain_id = domain.id

    # Create a shortened link
    response, link = client.create_link(
        hostname="your-domain.short.gy",
        original_url="https://example.com/very-long-url-path",
        title="Example Link"
    )
    print(f"Shortened URL: {link.short_url}")

    # List all your links
    response, links = client.list_links(domain_id=domain_id)
    for link in links:
        print(f"{link.title}: {link.short_url} -> {link.original_url}")

📖 `Complete Documentation <https://pyshortio.readthedocs.io/en/latest/>`_


.. _install:

Install
------------------------------------------------------------------------------

``pyshortio`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install pyshortio

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade pyshortio
