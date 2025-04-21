Getting Started
===============

Choose from multiple ways to start testing your API with Schemathesis.

.. note:: Your API schema can be either a URL or a local path to a JSON/YAML file.

Command-Line Interface
----------------------

Quick and easy for those who prefer the command line.

Python
^^^^^^

1. Install via pip: ``python -m pip install schemathesis``
2. Run tests:

.. code-block:: bash

   st run --checks all https://example.schemathesis.io/openapi.json

Docker
^^^^^^

1. Pull Docker image: ``docker pull schemathesis/schemathesis:stable``
2. Run tests:

.. code-block:: bash

   docker run schemathesis/schemathesis:stable
      run --checks all https://example.schemathesis.io/openapi.json

Python Library
--------------

For more control and customization, integrate Schemathesis into your Python codebase.

1. Install via pip: ``python -m pip install schemathesis``
2. Add to your tests:

.. code-block:: python

   import schemathesis

   schema = schemathesis.from_uri("https://example.schemathesis.io/openapi.json")


   @schema.parametrize()
   def test_api(case):
       case.call_and_validate()

.. note:: See a complete working example project in the `/example <https://github.com/schemathesis/schemathesis/tree/master/example>`_ directory.

GitHub Integration
------------------

GitHub Actions
^^^^^^^^^^^^^^

Run Schemathesis tests as a part of your CI/CD pipeline. Add this YAML configuration to your GitHub Actions:

.. code-block:: yaml

   api-tests:
     runs-on: ubuntu-22.04
     steps:
       - uses: schemathesis/action@v1
         with:
           schema: "https://example.schemathesis.io/openapi.json"

For more details, check out our `GitHub Action <https://github.com/schemathesis/action>`_ repository.
