import os
from pathlib import Path
import shutil
from typing import Any, Callable, Optional, Union

from pydantic import validate_call
import yaml


from mlflow_ibmcos.core.exceptions import (
    MLMODEL_FILE_NOT_FOUND,
    ArtifactNotFoundError,
    MLModelNotFoundError,
)
from mlflow_ibmcos.logger import Logger
from mlflow_ibmcos.schemas import NonEmptyDict
from mlflow_ibmcos.utils import Color, print_colored_message


logger = Logger(__name__)


def move_artifacts_hook(func: Callable) -> Callable:
    """
    Decorator to move artifacts to a final location after
    the method has completed.
    This decorator is only applied to `download_artifacts` method, which is called
    using a keyword argument `move_artifacts`.
    """

    @validate_call(validate_return=True)
    def wrapper(
        self: Any,
        artifact_path: Optional[str] = None,
        dst_path: Optional[Union[str, Path]] = None,
        delete_other_versions: bool = False,
        move_artifacts: Optional[NonEmptyDict] = None,
    ) -> str:
        result = func(
            self,
            artifact_path=artifact_path,
            dst_path=dst_path,
            delete_other_versions=delete_other_versions,
        )
        if move_artifacts is not None:
            logger.info(f"Moving artifacts {move_artifacts} to final location.")
            mlmodel_path = os.path.join(result, "MLmodel")
            if not os.path.exists(mlmodel_path):
                raise MLModelNotFoundError(MLMODEL_FILE_NOT_FOUND.format(result))
            with open(mlmodel_path) as f:
                mlmodel = yaml.safe_load(f)
            artifacts = mlmodel["flavors"]["python_function"]["artifacts"]
            if not set(move_artifacts).issubset(set(artifacts)):
                not_included = set(move_artifacts) - set(artifacts)

                raise ArtifactNotFoundError(
                    f"Artifacts {not_included} not found in MLmodel file."
                )
            for artifact_to_move, new_dest in move_artifacts.items():
                old_dest: str = artifacts[artifact_to_move]["path"]
                if not os.path.isabs(old_dest):
                    old_dest = os.path.join(result, old_dest)
                artifacts[artifact_to_move]["path"] = new_dest
                if Path(new_dest).exists():
                    msg = f"Destination {new_dest} already exists. Skipping physical move for {artifact_to_move}."
                    logger.warning(msg)
                    print_colored_message(msg, color=Color.YELLOW)
                    if old_dest != new_dest:
                        # Remove old destination if it is not the same as new destination
                        # We remove either it's a directory or a file
                        logger.info(
                            f"Removing old destination {old_dest} for artifact {artifact_to_move}."
                        )
                        if os.path.isdir(old_dest):
                            shutil.rmtree(old_dest, ignore_errors=True)
                        else:
                            os.remove(old_dest)
                    continue
                shutil.move(old_dest, new_dest)
                logger.info(
                    f"Moved artifact {artifact_to_move} from {old_dest} to {new_dest}"
                )
            with open(mlmodel_path, "w") as f:
                yaml.safe_dump(mlmodel, f)
            logger.info("Updated MLmodel file with new artifact paths")

        return result

    return wrapper
