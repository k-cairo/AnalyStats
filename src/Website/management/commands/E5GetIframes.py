from datetime import datetime

import django.apps
from django.core.management.base import BaseCommand

from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver


# E5
class Command(BaseCommand):
    help = "Get Iframes"

    def add_arguments(self, parser):
        parser.add_argument('--str-endpoint', nargs='+', type=str, help='Endpoint to get iframes from', required=True,
                            default='')
        parser.add_argument('--str-error_context', nargs='+', type=str, help='Error context', required=True)
        parser.add_argument('--int-iframe_length', nargs='+', type=int, help='Iframe length', required=True)
        parser.add_argument('--str-save_message', nargs='+', type=str, help='Save message', required=True)
        parser.add_argument('--str-class', nargs='+', type=str, help='Class', required=True)

    # E5
    @staticmethod
    def get_class(class_str: str) -> object:
        models_class_list: list = django.apps.apps.get_models()
        for models_class in models_class_list:
            if models_class.__name__ == class_str:
                return models_class

    def handle(self, *args, **options):
        endpoint: str = options['str_endpoint'][0]
        error_context: str = ' '.join(options['str_error_context'])
        iframe_length: int = options['int_iframe_length'][0]
        save_message: str = ' '.join(options['str_save_message'])
        class_str: str = options['str_class'][0]
        class_: object = self.get_class(class_str=class_str)
        print()

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
            if iframe_length == 1:
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
