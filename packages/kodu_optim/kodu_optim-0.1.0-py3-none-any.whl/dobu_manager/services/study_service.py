from __future__ import annotations

import asyncio
import datetime
import random
import shutil
from functools import cache
from pathlib import Path

import optuna
from fastapi import UploadFile
from loguru import logger

from dobu_manager.config import OrchestratorConfig
from dobu_manager.repositories.study_repository import (
    create_study,
    find_all_studies,
    find_study_by_name,
    get_optuna_storage,
    update_study,
)
from shared.models.optuna import inverse_direction_mapper
from shared.models.study import CodeBaseStudy, CreateStudy


@cache
def _get_studies_dir() -> Path:
    return OrchestratorConfig.get().data_dir / "studies"


def insert_study(data: CreateStudy) -> CodeBaseStudy:
    study = CodeBaseStudy(
        name=data.name,
        direction=data.direction,
        created_at=datetime.datetime.now(),
        objective_file=data.objective_file,
        objective_function=data.objective_function,
    )
    optuna.create_study(
        storage=OrchestratorConfig.get().db_url,
        direction=study.direction,
        study_name=study.name,
    )

    create_study(study)
    return study


def get_study_by_name(name: str) -> CodeBaseStudy | None:
    return find_study_by_name(name)


def get_all_studies() -> list[CodeBaseStudy]:
    return find_all_studies()


def does_study_exists(name: str) -> bool:
    return find_study_by_name(name) is not None


def is_codebase_present(name: str) -> bool:
    study_dir = _get_studies_dir() / "test" / name
    return study_dir.exists() and len(list(study_dir.iterdir())) > 0


def select_single_study() -> CodeBaseStudy | None:
    all_studies = find_all_studies()
    eligible = [study for study in all_studies if study.state == "running"]
    if len(eligible) == 0:
        return None
    return random.choice(eligible)


def activate_study(name: str) -> CodeBaseStudy:
    study = find_study_by_name(name)
    study.state = "running"
    update_study(study)
    return study


def pause_study(name: str) -> CodeBaseStudy:
    study = find_study_by_name(name)
    study.state = "paused"
    update_study(study)
    return study


def get_study_codebase_zip(name: str, confirmed=True) -> Path:
    studies_dir = _get_studies_dir()
    return (
        studies_dir / "test" / name / "data.zip"
        if not confirmed
        else studies_dir / "confirmed" / name / "data.zip"
    )


def store_codebase_zip(
    name: str,
    data: UploadFile,
) -> Path:
    study_dir = _get_studies_dir() / "test" / name

    # Clear directory if exists
    if study_dir.exists():
        shutil.rmtree(study_dir)
    study_dir.mkdir(parents=True)

    # Save the uploaded zip file to the study directory as data.zip
    zip_path = study_dir / "data.zip"
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(data.file, buffer)

    return zip_path


def move_codebase_zip(name: str) -> Path:
    study_dir = get_study_codebase_zip(name, confirmed=False)
    if not study_dir.exists():
        raise Exception("Codebase Not found")
    target = get_study_codebase_zip(name, confirmed=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(study_dir, target)
    return target


scheduled_removals: dict[str, int] = {}


async def clear_test_after_timeout(name: str, directory: Path):
    """Clear the test after 30 minutes"""
    logger.info(f"Scheduling removal of test codebase: {name}")
    if name not in scheduled_removals:
        scheduled_removals[name] = 0
    else:
        scheduled_removals[name] += 1
    removal_id = scheduled_removals[name]
    await asyncio.sleep(60 * 30)
    logger.info(f"Woke up for removal of codebase {name}")
    if removal_id != scheduled_removals[name]:
        logger.info("Codebase was updated since removal scheduling, skipping it now")
        return
    logger.info(f"Removing code of test codebase: {directory}")
    if directory.exists():
        shutil.rmtree(directory)


def sync_unknown_optuna_studies(study: optuna.study.Study):
    # These are user created in the optuna dashboard most likely
    # but there might a case where that it not saved correctly in our db
    # In either case we remove it from optuna
    logger.info(
        f"Found a conflicting study [present in optuna but not in our db]: {study.study_name}"
    )
    zip_path = get_study_codebase_zip(study.study_name, confirmed=True)
    if zip_path.exists():
        logger.info("Found the codebase zip for the conflicting study, removing it now")
        # The data.zip file is present but I don't want to bother parsing the objective function
        # deleting is easier:
        shutil.rmtree(zip_path.parent)
    logger.info(f"Deleting conflicting study from optuna: {study.study_name}")
    storage = get_optuna_storage()
    storage.delete_study(study_id=study._study_id)


def sync_unknown_native_studies(study: CodeBaseStudy):
    # These are studies that are created by the user but seem to not be synced to the db file.
    logger.info(
        f"Found a conflicting study [preset in our db but not in optuna]: {study.name}"
    )
    storage = get_optuna_storage()
    logger.info("Creating the conflicting study in optuna")
    storage.create_new_study(
        study_name=study.name, directions=[inverse_direction_mapper[study.direction]]
    )


async def sync_optuna():
    logger.info("Running optuna synchronization")
    storage = get_optuna_storage()
    optuna_studies = set([study.study_name for study in storage.get_all_studies()])
    our_studies = set([study.name for study in find_all_studies()])
    # Studies that are present in optuna but not in ours
    unknown_optuna_studies = optuna_studies.difference(our_studies)

    # studies that are present in our db but not in optuna [ILLEGAL STATE]
    unknown_our_studies = our_studies.difference(optuna_studies)

    if len(unknown_optuna_studies) == 0 and len(unknown_our_studies) == 0:
        logger.info("No synchronization needed")
        return

    if len(unknown_optuna_studies) != 0:
        for study in storage.get_all_studies():
            if study.study_name not in unknown_optuna_studies:
                continue
            sync_unknown_optuna_studies(study)

    if len(unknown_our_studies) != 0:
        for study in find_all_studies():
            if study.name not in unknown_our_studies:
                continue
            sync_unknown_native_studies(study)


async def start_optuna_synchronizer(period_seconds: float):
    async def schedule():
        while True:
            asyncio.create_task(sync_optuna())
            await asyncio.sleep(period_seconds)

    asyncio.create_task(schedule())
