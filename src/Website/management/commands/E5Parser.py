from datetime import datetime

import django.apps
from django.core.management.base import BaseCommand

from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver


# E5
class Command(BaseCommand):
    help = "Parser"

    def add_arguments(self, parser):
        parser.add_argument('--str-endpoint', nargs='+', type=str)
        parser.add_argument('--str-error_context', nargs='+', type=str, required=True)
        parser.add_argument('--int-iframe_length', nargs='+', type=int)
        parser.add_argument('--str-save_message', nargs='+', type=str)
        parser.add_argument('--str-class', nargs='+', type=str)

    # E5
    @staticmethod
    def get_class(class_str: str) -> object:
        models_class_list: list = django.apps.apps.get_models()
        for models_class in models_class_list:
            if models_class.__name__ == class_str:
                return models_class

    def handle(self, *args, **options):
        # Get options
        error_context: str = ' '.join(options['str_error_context'])
        iframe_length: int = 0
        endpoint: str = ''
        save_message: str = ''
        class_: object = None

        if options.get('str_endpoint') is not None:
            endpoint = options['str_endpoint'][0]
        if options.get('int_iframe_length') is not None:
            iframe_length = options['int_iframe_length'][0]
        if options.get('str_save_message') is not None:
            save_message = ' '.join(options['str_save_message'])
        if options.get('str_class') is not None:
            class_str: str = options['str_class'][0]
            class_: object = self.get_class(class_str=class_str)

        # Instantiate Scraper
        scraper: E5SeleniumWebDriver = E5SeleniumWebDriver()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {error_context} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{error_context} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Get Iframes
        if scraper.status.success:
            if iframe_length == 0:
                if error_context.lower() == "get leagues":
                    scraper.get_leagues(error_context=error_context)
                elif error_context.lower() == "get seasons":
                    scraper.get_seasons(error_context=error_context)
                elif error_context.lower() == "get teams":
                    scraper.get_teams(error_context=error_context)
                elif error_context.lower() == "get upcoming matches":
                    scraper.get_upcoming_matches(error_context=error_context)
            elif iframe_length == 1:
                scraper.get_iframe(endpoint=endpoint, error_context=error_context, save_message=save_message,
                                   class_=class_)
            else:
                scraper.get_iframes(endpoint=endpoint, error_context=error_context, iframe_length=iframe_length,
                                    save_message=save_message, class_=class_)
            if not scraper.status.success:
                scraper.log_warning(f"{error_context} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                    f"{scraper.status.exception}")

        # Close driver
        scraper.quit()
        if not scraper.status.success:
            scraper.log_warning(f"{error_context} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {error_context} end -----")

        self.stdout.write(f"{save_message} Updated Successfully")
