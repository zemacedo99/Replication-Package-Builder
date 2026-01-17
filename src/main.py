"""Main application."""
import logging
import os
import sys

from dotenv import load_dotenv
from pydantic import ValidationError

import utils
from data import process
from models import application
from search import ieee

load_dotenv()
logging.basicConfig(
    filename="./output/replication_package_builder.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    filemode="a",
    level=logging.INFO
)


APPLICATION_FINISHED_MESSAGE = "main() - Application finished"

if __name__ == "__main__":
    logging.info("main() - Application started")

    arguments = utils.process_command_line_arguments()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("main() - Debug mode is enabled")

    try:
        app_settings = application.Settings()
    except ValidationError as e:
        logging.error("main() - %s", e)
        logging.info(APPLICATION_FINISHED_MESSAGE)
        print("%s", e)
        print("\nCheck the application log for details.")
        sys.exit(0)

    if arguments.ieee:
        # TODO: Originally this is performed in a while loop
        try:
            logging.info("main() - Search IEEE")

            final_results = []

            results = ieee.search(
                query=os.getenv("IEEE_QUERY"),
                api_key=os.getenv("IEEE_API_KEY"),
                start_record=1,
                max_records=os.getenv("IEEE_PAGE_SIZE"),
                debug=arguments.debug
            )  # IEEE uses 1-indexing

            results_information = ieee.extract_results_information(
                results=results, debug=arguments.debug
            )

            process.process_and_save_results(
                ieee_results=results_information, folder_name="output",
                debug=arguments.debug
            )
        except (FileNotFoundError, ValidationError) as e:
            logging.error("main() - %s", e)
            logging.info(APPLICATION_FINISHED_MESSAGE)
            sys.exit(0)

    logging.info(APPLICATION_FINISHED_MESSAGE)
