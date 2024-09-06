<p align="center">
 <a href="#-about-the-project">About</a> •
 <a href="#-technologies">Technologies</a> •
 <a href="#-folder-structure">Folder Structure</a> •
 <a href="#-scripts">Scripts</a> •
 <a href="#-tests">Tests</a> •
 <a href="#-contributing">Contributing</a> •
 <a href="#-author">Author</a> •
 <a href="#-licence">License</a>
</p>

&nbsp;
`<a id="-about-the-project"></a>`

## 💻 About the project

The **News Scraper Bot** is an educational tool designed to demonstrate the automation of gathering, analyzing, and reporting news articles. This project aims to provide a practical example for those who are learning about web scraping using only Selenium.

Key features of the News Scraper Bot include:

* Automated scraping of news articles based on specified search criteria
* Analysis of article content, including phrase counting and monetary amount detection
* Filtering of articles based on publication date
* Extraction of article metadata such as titles, descriptions, and image information

Developed with a focus on modularity and extensibility, the News Scraper Bot follows best practices in software development.

&nbsp;

<p align="center">
  <a href="#license"><img src="https://img.shields.io/github/license/FilipeMarch/news-scraper-bot?color=ff0000"></a>
  <a href="https://github.com/FilipeMarch/news-scraper-bot/issues"><img src="https://img.shields.io/github/issues/FilipeMarch/news-scraper-bot" alt="issue site news-scraper-bot" /></a>
  <a href="https://github.com/FilipeMarch/news-scraper-bot"><img src="https://img.shields.io/github/languages/count/FilipeMarch/news-scraper-bot" alt="total amount of programming languages used in the project" /></a>
  <a href="https://github.com/FilipeMarch/news-scraper-bot"><img src="https://img.shields.io/github/languages/top/FilipeMarch/news-scraper-bot" alt="most used language in the projects" /></a>
  <a href="https://github.com/FilipeMarch/news-scraper-bot"><img src="https://img.shields.io/github/repo-size/FilipeMarch/news-scraper-bot" alt="repository size" /></a>
<p>

<p align="center">
  <img alt="Robocorp icon" height=40 src="https://robocorp.com/wp-content/uploads/2024/05/lockup-black.png">
<p>

`<a id="-technologies"></a>`

## 🛠 Technologies

The following technologies were used while building this project:

&nbsp;

<p align="center">
</p>

&nbsp;

`<a id="-folder-structure"></a>`

## 📁 Folder Structure

The project follows a modular structure with clear separation of concerns:

* **src/** : Contains the main source code
* **tests/** : Houses the test files for the project
* **.output/** : Contains the output files such as the excel, images downloaded.
* **.test_output/** : Stores output from test runs.
* **.vscode/** : Project-specific settings for VS Code
* **src/news_scraper_bot.py** : Core functionality of the news scraper
* **src/main.py** : Runs the News Scraper Bot from the command line with customizable arguments for search phrase, news category, and date range.
* **local_run.py** : Runs the Robocorp bot locally.
* **requirements.txt** : Lists all Python dependencies
* **pyproject.toml** : Configuration for Python packaging and dependencies.
* **conda.yaml** : Stores output from test runs.
* **robot.yaml** : Defines the Robocorp robot process, including tasks, environment configuration, and steps to execute the bot.
* **.pre-commit-config.yaml** : Configuration for `pre-commit` hooks to ensure code quality and enforce consistent coding standards before committing.Envio de Emails

`<a id="-scripts"></a>`

## 📜 Scripts

We use `taskipy` to lint, format and test the project.

- **task lint**: Runs `ruff` to check the codebase for linting issues and style violations. It performs two checks: the first ensures the code meets linting standards, and the second shows differences for any violations. Command: `ruff check . && ruff check . --diff`
- **task format**: Automatically fixes code style issues using `ruff`, ensuring that the code adheres to the project's formatting guidelines. It then applies additional formatting to clean up the codebase. Command: `ruff check . --fix && ruff format .`
- **task test**: Runs the test suite using `pytest` with verbosity enabled, stopping at the first failure (`-x`) and generating test coverage for the `src` directory. After the tests complete, an HTML report of the coverage is generated. Command: `pytest -s -x --cov=src -vv`
- **task pre_test**: A pre-test step that ensures the codebase is properly linted by running `task lint` before executing the test suite.
- **task post_test**: After the tests run, this task generates an HTML coverage report, providing insights into the test coverage of the source code.

`<a id="-tests"></a>`

## 🧪 Tests

The project includes a basic test suite to ensure reliability and correctness. Tests can be run using `task test`.

⚠️ Current coverage is not 100%

`<a id="-contributing"></a>`

## 👐 Contributing

This project is open source under the MIT license, and contributions are very welcome!

If you find any issues or have an improvement idea, feel free to open an [issue](https://github.com/FilipeMarch/news-scraper-bot/issues). Pull requests are also very welcome!

`<a id="-author"></a>`

## 🦸 Author

Hello, I'm Filipe Marchesini, Full Stack developer. I love math, programming and truth.

`<a id="-licence"></a>`

## 📝 Licence

Este projeto é [MIT licensed](./LICENSE).
