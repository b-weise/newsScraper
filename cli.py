import argparse
import asyncio
from argparse import Namespace
from datetime import datetime
from pathlib import Path

from source.classes.db_manager import DBManager
from source.classes.p12_scraper import P12Scraper
from source.interfaces.db_tables import MatchingArticles


async def main(args: Namespace):
    """
    Entry point for CLI execution.
    """
    search_keyword = args.keyword[0]

    p12scraper = P12Scraper(throttling_chunk_size=args.chunk_size)
    await p12scraper.initialize_website_handler(headless=not args.headfull, default_timeout_sec=args.timeout,
                                                default_navigation_timeout_sec=args.nav_timeout)
    results = await p12scraper.search(keyword=search_keyword, case_sensitive=args.case_sensitive,
                                      do_throttle=not args.disable_throttling)
    await p12scraper.destroy()

    def map_results(results: list[dict[str, str]]) -> list[MatchingArticles]:
        """
        Maps dictionaries to table objects.
        """
        table_objects = []
        for article in results:
            table_objects.append(
                MatchingArticles(
                    Keyword=search_keyword,
                    URL=article['article_url'],
                    Title=article['title'],
                    Date=datetime.fromisoformat(article['date']),
                    Author=article['author'],
                    ImageURL=article['image_url'],
                    Body=article['body'],
                )
            )
        return table_objects

    db_filepath = Path(args.output)
    dbmanager = DBManager(filepath=db_filepath)
    dbmanager.store(map_results(results))
    dbmanager.destroy()


# Set up argument parser
parser = argparse.ArgumentParser(description='P12 articles scraper.')
parser.add_argument('keyword', nargs=1, help='Keyword to be searched for.')
parser.add_argument('-o', '--output', nargs='?', default='p12_scraper.db',
                    help='Path to the SQLite database where the output is stored.')
parser.add_argument('-I', '--case_sensitive', action='store_true',
                    help='Perform a case-sensitive search.')
parser.add_argument('-R', '--disable_throttling', action='store_true',
                    help='Disable requests throttling.')
parser.add_argument('-H', '--headfull', action='store_true', help='Launch headfull browser.')
parser.add_argument('-t', '--timeout', nargs='?', type=int, default=5,
                    help='Default timeout in seconds.')
parser.add_argument('-n', '--nav_timeout', nargs='?', type=int, default=25,
                    help='Default navigation timeout in seconds.')
parser.add_argument('-c', '--chunk_size', nargs='?', type=int, default=5,
                    help='Default throttling chunk size.')

args = parser.parse_args()

asyncio.run(main(args))
