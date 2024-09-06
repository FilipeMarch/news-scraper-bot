import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

import httpx
import trio
from dateutil.relativedelta import relativedelta
from robocorp import log, workitems
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files

log_dir = 'output'

os.makedirs(log_dir, exist_ok=True)

# log_file = os.path.join(log_dir, 'scraper_log.txt')
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
# )

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


class WebScraper:
    """
    A class for web scraping operations on news websites.

    This class handles opening the website, searching for news articles,
    and extracting article information.
    """

    def __init__(self, base_url: str):
        """
        Initialize the WebScraper with a base URL.

        Args:
            base_url (str): The base URL of the news website.
        """
        self.base_url = base_url
        self.browser = Selenium()

    def open_website(self) -> None:
        """
        Open the news website in a browser.

        This method navigates to the base URL and waits for the page to load.
        """
        log.info(f'Opening website: {self.base_url}')
        self.browser.open_available_browser(self.base_url)
        self.browser.wait_until_element_is_visible('css:body', timeout=3)
        log.info('Website opened successfully')

    def search_news(self, search_phrase: str) -> None:
        """
        Perform a search on the news website.

        This method enters the search phrase and initiates the search.

        Args:
            search_phrase (str): The phrase to search for in news articles.
        """
        log.info('Waiting for search button to be visible')
        search_button_locator = 'css:.header-toggle.search-toggle'
        self.browser.wait_until_element_is_visible(
            search_button_locator, timeout=7
        )

        log.info('Clicking on the search button')
        self.browser.click_element(search_button_locator)

        log.info('Waiting for search input to be visible')
        self.browser.wait_until_element_is_visible('name:q', timeout=7)

        log.info('Clicking on the search input field')
        search_input = self.browser.find_element('name:q')
        search_input.click()

        log.info('Entering the search phrase')
        search_input.send_keys(search_phrase)

        log.info('Clicking on the search button to start the search')
        search_submit_button_locator = 'css:.btn-search'
        self.browser.click_element(search_submit_button_locator)

        log.info('Waiting for search results to be visible')
        articles_list_locator = 'css:.list-articles'
        self.browser.wait_until_element_is_visible(
            articles_list_locator, timeout=7
        )

    def extract_articles_info(
        self, search_phrase: str, num_months: int
    ) -> Optional[List[Dict]]:
        """
        Extract information from news articles based on search criteria.

        This method scrapes article data including title, description, date,
        and image information. It filters articles based on the date range.

        Args:
            search_phrase (str): The phrase used to search for articles.
            num_months (int): The number of months to look back for articles.

        Returns:
            Optional[List[Dict]]: A list of dictionaries containing article
            information, or None if no articles are found.
        """
        log.info('Extracting article information')
        titles = self.browser.find_elements(
            'xpath:.//h3[@class="hed-article-title"]'
        )
        descriptions = self.browser.find_elements(
            'xpath:.//div[@class="summary"]/p'
        )
        dates = self.browser.find_elements('xpath:.//time')
        images = self.browser.find_elements('xpath:.//li//img')

        if len(titles) == 0:
            log.info('No articles found for the given search phrase')
            return None

        articles_data = []
        for title, description, date, image in zip(
            titles, descriptions, dates, images
        ):
            article_date = date.get_attribute('datetime')
            image_url = image.get_attribute('src')
            image_filename = os.path.basename(image_url)
            count_phrases = DataProcessor.count_phrases(
                title.text, description.text, search_phrase
            )
            contains_money = DataProcessor.check_monetary_amount(
                title.text, description.text
            )

            if DataProcessor.is_article_within_date_range(
                article_date, num_months
            ):
                articles_data.append({
                    'title': title.text,
                    'description': description.text,
                    'date': article_date,
                    'image_filename': image_filename,
                    'image_url': image_url,
                    'count_phrases': count_phrases,
                    'contains_money': contains_money,
                })
            else:
                break

        log.info(
            f'Found {len(articles_data)} articles '
            'containing search phrase in the date range'
        )
        return articles_data


class DataProcessor:
    """
    A class for processing and analyzing article data.

    This class provides static methods for date range checking,
    phrase counting, and monetary amount detection in article content.
    """

    @staticmethod
    def is_article_within_date_range(
        article_date: str, num_months: int
    ) -> bool:
        """
        Check if an article's date falls within the specified date range.

        Args:
            article_date (str): The date of the article in 'YYYY-MM-DD' format.
            num_months (int): The number of months to look back.

        Returns:
            bool: True if article is within the date range, False otherwise.
        """
        date_format = '%Y-%m-%d'
        article_datetime = datetime.strptime(article_date, date_format)
        current_datetime = datetime.now()

        if num_months <= 1:
            start_of_current_month = current_datetime.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            return article_datetime >= start_of_current_month
        else:
            months_ago = num_months - 1
            start_date = current_datetime.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            ) - relativedelta(months=months_ago)
            return article_datetime >= start_date

    @staticmethod
    def count_phrases(title: str, description: str, search_phrase: str) -> int:
        """
        Count occurrences of a search phrase in the title and description.

        Args:
            title (str): The article title.
            description (str): The article description.
            search_phrase (str): The phrase to search for.

        Returns:
            int: The total count of the search phrase in title and description.
        """
        return title.lower().count(
            search_phrase.lower()
        ) + description.lower().count(search_phrase.lower())

    @staticmethod
    def check_monetary_amount(title: str, description: str) -> bool:
        """
        Check if the title or description contains any monetary amount.

        Args:
            title (str): The article title.
            description (str): The article description.

        Returns:
            bool: True if a monetary amount is found, False otherwise.
        """
        pattern = r'\$\d+(?:\.\d{1,2})?|\d+\s?(?:dollars|USD)'
        return bool(
            re.search(pattern, title + ' ' + description, re.IGNORECASE)
        )


class FileOperations:
    """
    A class for handling file operations related to scraped news data.

    This class manages saving data to Excel files and downloading images.
    """

    def __init__(self, output_dir: str):
        """
        Initialize FileOperations with an output directory.

        Args:
            output_dir (str): The directory path for saving output files.
        """
        self.output_dir = output_dir
        self.excel = Files()

    def save_to_excel(self, data: List[Dict]) -> None:
        """
        Save the scraped article data to an Excel file (.xlsx).

        Args:
            data (List[Dict]): A list of dictionaries containing article info.
        """
        file_path = os.path.join(self.output_dir, 'news_articles.xlsx')
        log.info(f'Saving results to {file_path}')

        self.excel.create_workbook(file_path)
        self.excel.append_rows_to_worksheet([
            [
                'Title',
                'Date',
                'Description',
                'Image Filename',
                'Count Phrases',
                'Contains Money',
            ]
        ])

        for article in data:
            self.excel.append_rows_to_worksheet(
                [
                    [
                        article['title'],
                        article['date'],
                        article['description'],
                        article['image_filename'],
                        article['count_phrases'],
                        article['contains_money'],
                    ]
                ],
                header=False,
            )
        self.excel.save_workbook()
        log.info('Results saved successfully')

    async def download_images(self, article_data: List[Dict]) -> None:
        """
        Download images for all articles asynchronously.

        Args:
            article_data (List[Dict]): A list of dictionaries
            containing article info.
        """
        async with httpx.AsyncClient() as client:
            async with trio.open_nursery() as nursery:
                for article in article_data:
                    nursery.start_soon(
                        self._download_image, client, article['image_url']
                    )

    async def _download_image(
        self, client: httpx.AsyncClient, image_url: str
    ) -> None:
        """
        Download a single image asynchronously.

        Args:
            client (httpx.AsyncClient): An async HTTP client.
            image_url (str): The URL of the image to download.
        """
        HTTP_OK = 200
        try:
            response = await client.get(image_url)
            if response.status_code == HTTP_OK:
                filename = os.path.basename(image_url)
                filepath = os.path.join(self.output_dir, filename)
                await trio.to_thread.run_sync(
                    self._save_image, filepath, response.content
                )
                log.info(f'Image downloaded: {filename}')
            else:
                logger.warning(f'Failed to download image: {image_url}')
        except Exception as e:
            logger.error(f'Error downloading image {image_url}: {str(e)}')

    @staticmethod
    def _save_image(filepath: str, content: bytes) -> None:
        """
        Save image content to a file.

        Args:
            filepath (str): The path where the image will be saved.
            content (bytes): The image content to save.
        """
        with open(filepath, 'wb') as f:
            f.write(content)


class NewsScraperBot:
    """
    Main class for orchestrating the news scraping process.

    Coordinates the web scraping, data processing, and file operations.
    """

    def __init__(
        self,
        search_phrase: Optional[str] = None,
        news_category: Optional[str] = None,
        num_months: Optional[int] = None,
    ):
        """
        Initialize the NewsScraperBot with search parameters.

        Args:
            search_phrase (str): The phrase to search for in news articles.
            news_category (str): The category of news to focus on.
            num_months (int): The number of months to look back for articles.
        """
        if search_phrase is None:
            # Robot Framework Work Item
            work_item = workitems.inputs.current
            self.search_phrase = getattr(work_item, 'search_phrase', '')
            self.news_category = getattr(work_item, 'news_category', '')
            self.num_months = getattr(work_item, 'num_months', 1)
        else:
            # CLI Arguments
            self.search_phrase = search_phrase
            self.news_category = news_category
            self.num_months = num_months

        log.info(
            f'Search phrase: {self.search_phrase}, '
            f'Category: {self.news_category}, '
            f'Months: {self.num_months}'
        )
        self.base_url = 'https://source.opennews.org/'
        self.output_dir = os.path.join(os.getcwd(), 'output')

        self.web_scraper = WebScraper(self.base_url)
        self.file_operations = FileOperations(self.output_dir)

    def run(self) -> None:
        """
        Execute the main scraping process.

        Orchestrates the opening of the website, searching for news,
        and scraping the results.
        """
        try:
            self.web_scraper.open_website()
            self.web_scraper.search_news(self.search_phrase)
            self.scrape_news()
        finally:
            self.web_scraper.browser.close_all_browsers()

    def scrape_news(self) -> None:
        """
        Scrape news articles and process the results.

        This method extracts article information, downloads images,
        and saves the data to an Excel file.
        """
        log.info('Scraping news...')
        article_data = self.web_scraper.extract_articles_info(
            self.search_phrase, self.num_months
        )
        if article_data:
            trio.run(self.file_operations.download_images, article_data)
            self.file_operations.save_to_excel(article_data)
        else:
            log.info('No articles found within the date range')


def main():
    bot = NewsScraperBot()
    bot.run()


if __name__ == '__main__':
    main()
