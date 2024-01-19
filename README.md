# Platform autotests

## Initial installation

1. Install python 3.11
2. [Install poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

   ```shell
      # Linux/Mac os
      curl -sSL https://install.python-poetry.org | python3 -
   ```
   ```shell
      # Windows powershell
      (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```
3. Install dependencies
   ```shell
      poetry install
   ```
4. Install [pre-commit](https://pre-commit.com) hooks:
   ```shell
      pre-commit install --install-hooks
   ```

### Local settings:
To change local settings and provide some secure data such as passwords use the `.env.local` file.
Copy [.env.local.example](.env.local.example) as `.env.local` and configure the settings.
This file also contains more information.

### Webdriver:
webdriver-manager should automatically install the required webdriver version.
However, sometimes Google changes something and webdriver-manager stops working. In this case, you can manually
download the required version of a webdriver and provide a path of the webdriver in the `.env.local` file.

## More guides

* <u>[Running tests on CI](docs/RunTests.md)</u>
* <u>[UI docs](docs/UI.md)</u>

### Useful plugins:

You can install these useful plugins for PyCharm:
* Pydantic - improves autocompletion
* Tabnine AI Code Completion/GitHub Copilot - AI autocompletion tools
