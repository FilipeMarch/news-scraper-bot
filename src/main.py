import argparse
import logging

from news_scraper_bot import NewsScraperBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description='News Scraper Bot')
    parser.add_argument(
        '--search_phrase',
        default='default search',
        help='Search phrase for news articles',
    )
    parser.add_argument(
        '--news_category',
        default='general',
        help='News category/section/topic',
    )
    parser.add_argument(
        '--num_months',
        type=int,
        default=1,
        help='Number of months of news to scrape',
    )
    return parser.parse_args()


def main():
    try:
        args = parse_arguments()
        bot = NewsScraperBot(
            args.search_phrase,
            args.news_category,
            args.num_months,
        )
        bot.run()
    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')


if __name__ == '__main__':
    main()
