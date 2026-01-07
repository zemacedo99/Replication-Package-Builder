#!/usr/bin/env python3
"""Main application."""
import logging
import sys

import utils
from models import application
from pydantic import ValidationError

from search import ieee

logging.basicConfig(
    filename="./replication_package_builder.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    filemode="a",
    level=logging.INFO
)


# FIXME
APPLICATION_FINISHED_MESSAGE = "main() - Application finished"
IEEE_QUERY = '("Agile" OR "Agility" OR "Scrum" OR "Kanban" OR "Scrumban" OR "SafeScrum" OR "AgileSafe" OR "Agile Safe" OR "XP" OR "Extreme Programming" OR "Large-Scale Scrum" OR "LeSS" OR "Scrum@Scale" OR "SaS" OR "Disciplined Agile Delivery" OR "DAD") AND ("aerospace" OR "avionic" OR "avionics" OR "aviation" OR "aeronautic" OR "aeronautics" OR "aeronautical") AND ("Safety" OR "Safety-Critical" OR "Safety Critical" OR "Safety-Critical Systems" OR "Safety Critical Systems" OR "High Integrity" OR "High Integrity Systems" OR "HIS" OR "Safety Integrity" OR "Safety-Systems" OR "Safety Systems") AND ("ARP4761" OR "ARP 4761" OR "ARP4754" OR "ARP 4754" OR "ARP4754A" OR "ARP 4754A" OR "DO-178" OR "DO 178" OR "DO178" OR "DO-178C" OR "DO 178C" OR "DO178C" OR "DO-178B" OR "DO 178B" OR "DO178B" OR "DO 331" OR "DO331" OR "DO-331" OR "DO-297" OR "DO 297" OR "DO297") AND NOT "Manufactoring" AND NOT "manufactoring" AND NOT "Formal Methods" AND NOT "Formal methods" AND NOT "Batery" AND NOT "Bateries" AND NOT "Cells" AND NOT "Hydrogen" AND NOT "Computer Model" AND NOT "Simulation" AND NOT "Computer Simulation" AND NOT "Network" AND NOT "Neural" AND NOT "Graphical" AND NOT "Computer Graphics" AND NOT "Machine Learning" AND NOT "Electric" AND NOT "Automated Driving" AND NOT "Security" AND NOT "Health" AND NOT "MC/DC" AND NOT "Flight" AND NOT "Flight Control" AND NOT "Crew" AND NOT "Processor" AND NOT "Satellite" AND NOT "Power Converters" AND NOT "Engine" AND NOT "Turbine" AND NOT "Braking System" AND NOT "Carbon Emissions" AND NOT "Ambulance" AND NOT "Paramedics"'
IEEE_API_KEY = ""
PAGE_SIZE = 25
START_INDEX = 0

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
        try:
            logging.info("main() - Search IEEE")
            results = ieee.search(
                query=IEEE_QUERY, api_key=IEEE_API_KEY,
                start_record=START_INDEX + 1, max_records=PAGE_SIZE
            )  # IEEE uses 1-indexing
            logging.info("main() - Results: %s", results)
        except (FileNotFoundError, ValidationError) as e:
            logging.error("main() - %s", e)
            logging.info(APPLICATION_FINISHED_MESSAGE)
            sys.exit(0)

    logging.info(APPLICATION_FINISHED_MESSAGE)
