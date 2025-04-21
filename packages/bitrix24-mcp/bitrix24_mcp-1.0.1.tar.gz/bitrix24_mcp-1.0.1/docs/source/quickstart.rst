Quick Start
===========

Configuration
============

The server requires your Bitrix24 webhook URL. You can set it in one of two ways:

1. Environment variable:

.. code-block:: bash

   export BITRIX_WEBHOOK_URL="https://your-domain.bitrix24.ru/rest/1/yoursecretcode/"

2. `.env` file:

.. code-block:: ini

   # .env
   BITRIX_WEBHOOK_URL="https://your-domain.bitrix24.ru/rest/1/yoursecretcode/"
   # Optional log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   # LOG_LEVEL=INFO

Running the Server
================

After installation and configuration, start the MCP server:

.. code-block:: bash

   python main.py
   # or if installed globally
   mcp-server-b24

Testing the Installation
=====================

To verify basic Bitrix24 API integration, run the test script:

.. code-block:: bash

   python test_services.py