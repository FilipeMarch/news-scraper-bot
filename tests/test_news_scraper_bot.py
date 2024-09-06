import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.news_scraper_bot import (
    DataProcessor,
    FileOperations,
    NewsScraperBot,
    WebScraper,
)


@pytest.fixture
def web_scraper():
    return WebScraper('https://www.pudim.com.br/')


@pytest.fixture
def file_operations():
    return FileOperations('test_output')


@patch('src.news_scraper_bot.Selenium')
def test_web_scraper_init(mock_selenium):
    """
    Test the initialization of the WebScraper class.
    """
    scraper = WebScraper('https://www.pudim.com.br/')
    assert scraper.base_url == 'https://www.pudim.com.br/'
    assert scraper.browser == mock_selenium.return_value
    mock_selenium.assert_called_once()


@patch('src.news_scraper_bot.Selenium')
def test_open_website(mock_selenium):
    """
    Test the opening of the website.
    """
    web_scraper = WebScraper('https://www.pudim.com.br/')
    web_scraper.open_website()

    mock_selenium.return_value.open_available_browser.assert_called_once_with(
        web_scraper.base_url
    )
    mock_selenium.return_value.wait_until_element_is_visible.assert_called_once_with(
        'css:body', timeout=3
    )


def test_is_article_within_date_range():
    """
    Test if an article is within the specified date range.
    """
    FAIL_DAYS, SUCCESS_DAYS = 32, 1
    fail_date, success_date = (
        datetime.date.today() - datetime.timedelta(days=FAIL_DAYS),
        datetime.date.today() - datetime.timedelta(days=SUCCESS_DAYS),
    )
    fail_date_str, success_date_str = (
        fail_date.strftime('%Y-%m-%d'),
        success_date.strftime('%Y-%m-%d'),
    )
    assert (
        DataProcessor.is_article_within_date_range(fail_date_str, 1) is False
    )
    assert (
        DataProcessor.is_article_within_date_range(success_date_str, 1) is True
    )


def test_count_phrases():
    """
    Test counting phrases in article content.
    """
    assert (
        DataProcessor.count_phrases('Test title', 'Test description', 'test')
        == 2  # noqa: PLR2004
    )
    assert (
        DataProcessor.count_phrases('No match', 'Still no match', 'test') == 0
    )


def test_check_monetary_amount():
    """
    Test checking for monetary amounts in article content.
    """
    assert (
        DataProcessor.check_monetary_amount(
            '$100 in the title', 'No money here'
        )
        is True
    )
    assert (
        DataProcessor.check_monetary_amount('No money', 'Still no money')
        is False
    )


@patch('src.news_scraper_bot.Files')
def test_save_to_excel(mock_files_class):
    """
    Test saving data to an Excel file.
    """
    mock_files_instance = mock_files_class.return_value
    file_operations = FileOperations('test_output')
    file_operations.excel = mock_files_instance

    data = [
        {
            'title': 'Test',
            'date': '2023-01-01',
            'description': 'Test desc',
            'image_filename': 'test.jpg',
            'count_phrases': 1,
            'contains_money': False,
        }
    ]
    file_operations.save_to_excel(data)

    mock_files_instance.create_workbook.assert_called_once()


@pytest.mark.trio
async def test_download_images(file_operations):
    """
    Test downloading images.
    """
    with patch('src.news_scraper_bot.httpx.AsyncClient') as mock_client:
        mock_response = mock_client.return_value.__aenter__.return_value.get
        mock_response.return_value.status_code = 200
        mock_response.return_value.content = b'fake image content'

        await file_operations.download_images([
            {'image_url': 'https://www.pudim.com.br/pudim.jpg'}
        ])


def test_news_scraper_bot_init():
    """
    Test the initialization of the NewsScraperBot class.
    """
    bot = NewsScraperBot('test', 'news', 1)
    assert bot.search_phrase == 'test'
    assert bot.news_category == 'news'
    assert bot.num_months == 1
    assert isinstance(bot.web_scraper, WebScraper)
    assert isinstance(bot.file_operations, FileOperations)


@patch('src.news_scraper_bot.WebScraper')
def test_news_scraper_bot_run(mock_web_scraper):
    """
    Test the run method of the NewsScraperBot class.
    """
    mock_file_ops = MagicMock()
    mock_file_ops.download_images = AsyncMock()

    bot = NewsScraperBot('test', 'news', 1)
    bot.web_scraper = mock_web_scraper.return_value
    bot.file_operations = mock_file_ops

    bot.run()

    mock_web_scraper.return_value.open_website.assert_called_once()
    mock_web_scraper.return_value.search_news.assert_called_once_with('test')
    mock_web_scraper.return_value.extract_articles_info.assert_called_once()
    mock_file_ops.download_images.assert_called_once()
    mock_file_ops.save_to_excel.assert_called_once()
