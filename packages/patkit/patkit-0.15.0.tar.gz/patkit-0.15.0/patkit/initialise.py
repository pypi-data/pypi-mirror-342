#!/usr/bin/env python3
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
Initialisation routines for PATKIT.
"""

import shutil
from importlib.resources import path as resource_path
from logging import Logger
from pathlib import Path

from patkit.annotations import add_peaks
from patkit.configuration import (
    Configuration,
    apply_exclusion_list,
    load_exclusion_list,
)
from patkit.constants import PATKIT_CONFIG_DIR
from patkit.data_loader import load_data
from patkit.data_processor import (
    process_modalities, process_statistics_in_recordings)
from patkit.data_structures import Session
from patkit.metrics import (
    add_aggregate_images,
    add_distance_matrices,
    add_pd,
    add_spline_metric,
    downsample_metrics_in_session,
)
from patkit.modalities import RawUltrasound, Splines
from patkit.utility_functions import (
    log_elapsed_time, path_from_name, set_logging_level)


def initialise_patkit(
    path: Path | str | None = None,
    config_file: Path | str | None = None,
    exclusion_file: Path | str | None = None,
    logging_level: int | None = None,
) -> tuple[Configuration, Logger, Session]:
    """
    Initialise the basic structures for running patkit.

    This sets up the argument parser, reads the basic configuration, sets up the
    logger, and loads the recorded and saved data into a Session. To initialise
    derived data run `add_derived_data`.

    Returns
    -------
    tuple[config, logger, session] where
        config is an instance of Configuration,
        logger is an instance of logging.Logger, and
        session is an instance of Session.
    """
    path = path_from_name(path)
    # TODO 0.16: Move this call to cli_commands like with simulate.
    config, exclusion_file, logger = initialise_logger_and_config(
        config_file=config_file,
        exclusion_file=exclusion_file,
        logging_level=logging_level,
    )

    exclusion_list = None
    if exclusion_file is not None:
        exclusion_list = load_exclusion_list(exclusion_file)
    session = load_data(path, config)
    apply_exclusion_list(session, exclusion_list=exclusion_list)
    log_elapsed_time(logger)

    add_derived_data(session=session, config=config, logger=logger)
    log_elapsed_time(logger)

    return config, logger, session


def initialise_logger_and_config(
    config_file: Path | str | None = None,
    exclusion_file: Path | str | None = None,
    logging_level: int | None = None,
) -> tuple[Configuration, Path, Logger]:
    """
    Initialise logger and configuration.

    Parameters
    ----------
    config_file : Path | str | None
        Main configuration file, by default None. This leads to loading
        `~/.patkit/`.
    exclusion_file : Path | str | None
        Main exclusion file, by default None.
    logging_level : int | None
        Logging level, by default None. Which sets the logging level to DEBUG.

    Returns
    -------
    tuple[Configuration, Path, Logger]
        These are the main Configuration, exclusion file as Path, and the
        logger.
    """
    if config_file is None:
        default_config_dir = Path(PATKIT_CONFIG_DIR).expanduser()
        config_file = default_config_dir/"configuration.yaml"
        if not config_file.exists():
            if not default_config_dir.exists():
                default_config_dir.mkdir()
            with resource_path(
                    "patkit", "default_configuration"
            ) as fspath:
                shutil.copytree(
                    fspath, default_config_dir, dirs_exist_ok=True)

    else:
        config_file = path_from_name(config_file)

    config = Configuration(config_file)

    exclusion_file = path_from_name(exclusion_file)
    logger = set_logging_level(logging_level)

    return config, exclusion_file, logger


def add_derived_data(
    session: Session,
    config: Configuration,
    logger: Logger,
) -> None:
    """
    Add derived data to the Session according to the Configuration.

    NOTE: This function will not delete existing data unless it is being
    replaced (and the corresponding `replace` parameter is `True`). This means
    that already existing derived data is retained.

    Added data types include Modalities, Statistics and Annotations.

    Parameters
    ----------
    session : Session
        The Session to add derived data to.
    config : Configuration
        The configuration parameters to use in deriving the new derived data.
    logger : Logger
        The logger is passed as an argument since the initialise module is the
        one responsible for setting it up.

    Returns
    -------
    None
    """
    data_run_config = config.data_run_config

    modality_operation_dict = {}
    if data_run_config.pd_arguments:
        pd_arguments = data_run_config.pd_arguments
        modality_operation_dict["PD"] = (
            add_pd,
            [RawUltrasound],
            pd_arguments.model_dump(),
        )

    if data_run_config.aggregate_image_arguments:
        aggregate_image_arguments = data_run_config.aggregate_image_arguments
        modality_operation_dict["AggregateImage"] = (
            add_aggregate_images,
            [RawUltrasound],
            aggregate_image_arguments.model_dump(),
        )

    if data_run_config.spline_metric_arguments:
        spline_metric_args = data_run_config.spline_metric_arguments
        modality_operation_dict["SplineMetric"] = (
            add_spline_metric,
            [Splines],
            spline_metric_args.model_dump(),
        )

    process_modalities(recordings=session, processing_functions=modality_operation_dict)

    statistic_operation_dict = {}
    if data_run_config.distance_matrix_arguments:
        distance_matrix_arguments = data_run_config.distance_matrix_arguments
        statistic_operation_dict["DistanceMatrix"] = (
            add_distance_matrices,
            ["AggregateImage mean on RawUltrasound"],
            distance_matrix_arguments.model_dump(),
        )

    process_statistics_in_recordings(
        session=session, processing_functions=statistic_operation_dict
    )

    if data_run_config.downsample:
        downsample_metrics_in_session(
            recording_session=session, data_run_config=data_run_config
        )

    if data_run_config.peaks:
        modality_pattern = data_run_config.peaks.modality_pattern
        for recording in session:
            if recording.excluded:
                logger.info("Recording excluded from peak finding: %s", recording.name)
                continue
            for modality_name in recording:
                if modality_pattern.search(modality_name):
                    add_peaks(
                        recording[modality_name],
                        config.data_run_config.peaks,
                    )
