"""
Runs the robot locally.
"""

import logging
import os

from robocorp import workitems
from robocorp.tasks import task

from src.news_scraper_bot import NewsScraperBot

os.environ['RC_WORKITEM_INPUT_PATH'] = os.path.join(
    os.getcwd(), 'devdata', 'work-items-in', 'first-input', 'work-items.json'
)  # TODO fix this, it's not working

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


@task
def run_news_scraper():
    """
    Run the news scraper bot.
    """
    # TODO should be getting from 'work-items.json'
    # but it's not working, so hardcoding for now
    workitems.inputs.current.search_phrase = 'climate change'
    workitems.inputs.current.news_category = ''
    workitems.inputs.current.num_months = 8
    bot = NewsScraperBot()
    bot.run()


if __name__ == '__main__':
    run_news_scraper()
