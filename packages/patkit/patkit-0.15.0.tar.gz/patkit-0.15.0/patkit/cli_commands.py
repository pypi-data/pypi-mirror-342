#
# Copyright (c) 2019-2025
# Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
#
# This file is part of the Phonetic Analysis ToolKIT
# (see https://github.com/giuthas/patkit/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.md. They can also be found in
# citations.bib in BibTeX format.
#
"""
patkit command line commands.
"""

from pathlib import Path

import click

from patkit.initialise import initialise_logger_and_config, initialise_patkit
from patkit.qt_annotator import run_annotator
from patkit.interpreter import run_interpreter
from patkit.simulation import run_simulations
from patkit.simulation.simulate import setup_contours_comparisons_soundpairs


@click.command(name="open")
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, file_okay=True), )
@click.option(
    "-config_file", "-c",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, path_type=Path,
        readable=True
    ),
    required=False,
)
@click.option(
    "-exclusion_file", "-e",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, path_type=Path,
        readable=True
    ),
    required=False,
)
def open_in_annotator(
        path: Path, config_file: Path | None, exclusion_file: Path | None
) -> None:
    """
    Open the PATH in the annotator GUI.

    \b
    PATH to the data - maybe be a file or a directory.
    CONFIG_FILE configuration .yaml file.
    """
    if exclusion_file:
        if exclusion_file.suffix not in {".csv", ".yaml"}:
            raise click.ClickException(
                f"Unexpected exclusion file extension: {exclusion_file.suffix}."
            )
    configuration, logger, session = initialise_patkit(
        path=path, config_file=config_file, exclusion_file=exclusion_file)
    run_annotator(session, configuration)


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, file_okay=True), )
@click.option(
    "-config_file", "-c",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, path_type=Path,
        readable=True
    ),
    required=False,
)
@click.option(
    "-exclusion_file", "-e",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, path_type=Path,
        readable=True
    ),
    required=False,
)
def interact(
        path: Path, config_file: Path | None, exclusion_file: Path | None
):
    """
    Open the PATH in interactive commandline mode.

    \b
    PATH to the data - maybe be a file or a directory.
    CONFIG_FILE configuration .yaml file.
    """
    if exclusion_file:
        if exclusion_file.suffix not in {".csv", ".yaml"}:
            raise click.ClickException(
                f"Unexpected exclusion file extension: {exclusion_file.suffix}."
            )
    configuration, logger, session = initialise_patkit(
        path=path, config_file=config_file, exclusion_file=exclusion_file
    )
    run_interpreter(session=session, configuration=configuration)


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, file_okay=True), )
@click.argument(
    "config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=False,
)
@click.argument(
    "output_dir",
    type=click.Path(dir_okay=True, file_okay=False),
    required=False,
)
def publish(path: Path, config_file: Path | None, output_dir: Path | None):
    """
    Publish plots from the data in PATH.

    \b
    PATH to the data - maybe be a file or a directory.
    CONFIG_FILE configuration .yaml file.

    NOT IMPLEMENTED YET.
    """
    configuration, logger, session = initialise_patkit(
        path=path, config_file=config_file
    )


@click.command()
@click.argument(
    "path",
    type=click.Path(dir_okay=False, file_okay=True, path_type=Path),
)
def simulate(path: Path):
    """
    Run a simulation experiment.

    \b
    PATH to a ỳaml file which contains the parameters for running the
    simulation.
    """
    config, exclusion_file, logger = initialise_logger_and_config(
        config_file=path,
    )
    contours, comparisons, sound_pairs = setup_contours_comparisons_soundpairs(
        sim_configuration=config.simulation_config)
    run_simulations(
        sim_configuration=config.simulation_config,
        contours=contours,
        comparisons=comparisons,
        sound_pairs=sound_pairs
    )
