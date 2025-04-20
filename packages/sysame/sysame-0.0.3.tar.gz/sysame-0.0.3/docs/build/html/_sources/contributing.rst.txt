Contributing
===========

Thank you for considering contributing to SysAME! This guide will help you get started with the development process.

Development Setup
---------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

       git clone https://github.com/your-username/sysame.git
       cd sysame

3. Set up the development environment:

   .. code-block:: bash

       # Create a virtual environment
       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate
       
       # Install development dependencies
       pip install -e ".[dev]"

Coding Standards
--------------

- Follow PEP 8 style guidelines
- Write docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Add unit tests for new functionality

Pull Request Process
-----------------

1. Ensure your code passes all tests:

   .. code-block:: bash

       pytest

2. Update documentation if needed
3. Add your changes to the CHANGELOG
4. Submit a pull request with a clear description of your changes

Documentation
------------

When contributing documentation:

1. Write clear and concise descriptions
2. Include examples where appropriate
3. Use proper reStructuredText formatting
4. Build and test documentation locally:

   .. code-block:: bash

       cd docs
       make html
       # On Windows: make.bat html

Testing
------

We use pytest for testing. To run tests:

.. code-block:: bash

    pytest

To measure code coverage:

.. code-block:: bash

    pytest --cov=sysame
