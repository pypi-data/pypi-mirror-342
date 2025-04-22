from dataclasses import dataclass
from enum import Enum

from zeta.db import BaseData, NestedZetaBase
from zeta.utils.logging import zetaLogger


try:
    # TODO(CZ-921): Add proper dependencies to Comfy worker.
    from zeta.db.project import ZetaProject
except ImportError:
    zetaLogger.warning("ImportError: ZetaProject not found")


"""
The type of generation that was performed.

Must match the enum in the `GenerationType` class in the `engine/db/generation.ts` file.
"""
class GenerationType(Enum):
    TEXT_TO_IMAGE = "TEXT_TO_IMAGE"
    TEXT_TO_3D = "TEXT_TO_3D"
    TEXT_TO_SCENE = "TEXT_TO_SCENE"
    IMAGE_TO_3D = "IMAGE_TO_3D"
    SCENE_TO_IMAGE = "SCENE_TO_IMAGE"
    SCENE_TO_BOARD = "SCENE_TO_BOARD"
    SCENE_TO_VIDEO = "SCENE_TO_VIDEO"


"""
The state of the generation.

Must match the enum in the `GenerationState` class in the `engine/db/generation.ts` file.
"""
class GenerationState(Enum):
    IDLE = "Idle"

    PENDING = "Pending"
    GENERATING = "Generating"
    PROCESSING = "Processing"

    DONE = "Done"
    ERROR = "Error"
    CANCELLED = "Cancelled"

"""
The backend that was used to generate the generation.

Must match the enum in the `GenerationBackend` class in the `src/web/core/db/generation.ts` file.
"""
class GenerationBackend(Enum):
    RUNPOD_COMFYUI = "RUNPOD_COMFYUI"
    GPU_WORKER_COMFYUI = "GPU_WORKER_COMFYUI"

    MESHY_V4_PREVIEW = "MESHY_V4_PREVIEW"
    TRIPO = "TRIPO"
    MCP = "MCP"


@dataclass
class GenerationData(BaseData):
    # The type of generation that was performed.
    type: GenerationType

    # The backend that was used to generate the generation.
    backend: GenerationBackend

    # The state of the generation.
    state: GenerationState

    # The progress of the generation.
    progress: int

    # The error message that was generated if the generation failed.
    error: str

    # The user that requested the generation.
    userUid: str

    # The session that this generation is associated with.
    sessionUid: str

    # The project that this generation is associated with.
    projectUid: str

    # The prim path of the object that was generated.
    primPath: str

    # The prompt that was used for this generation.
    prompt: dict

    # The camera metadata that was used for this generation.
    cameraMetadata: dict

    # The outputs (e.g. images, videos, etc.) that were generated.
    outputs: list[dict]


class ZetaGeneration(NestedZetaBase):
    @classmethod
    def get_by_uid(cls, uid: str) -> 'ZetaGeneration':
        # This may not work in Firebase.
        thiz = super().get_by_uid(uid)
        thiz._parent = ZetaProject.get_by_uid(thiz.data.projectUid)
        return thiz

    @property
    def collection_name(cls) -> str:
        return "generations"

    @property
    def parent_uid_field(cls) -> str:
        return "project_uid"

    @property
    def data_class(self):
        return GenerationData

    @property
    def session_uid(self) -> str:
        return self.data.sessionUid

    @property
    def project_uid(self) -> str:
        return self.data.projectUid

    @property
    def is_running(self) -> bool:
        return (
            self.data.state == GenerationState.IDLE or
            self.data.state == GenerationState.PENDING or
            self.data.state == GenerationState.GENERATING
        )

    def get_scene_snapshot_uids(self) -> list['str']:
        if self.data is None:
            zetaLogger.error("Generation data is empty")
            return []
        try:
            snapshot_uids = self.data.cameraMetadata.get('snapshotUids', [])
            return snapshot_uids
        except Exception as e:
            zetaLogger.error(f"Failed to get camera snapshots: {e}")

        return []

    def calculate_credits_cost(self) -> int:
        if not self.valid:
            raise ValueError("This ZetaGeneration object is not valid")

        if self.data.type == GenerationType.TEXT_TO_IMAGE:
            return 20
        elif self.data.type == GenerationType.TEXT_TO_3D:
            return 200
        elif self.data.type == GenerationType.TEXT_TO_SCENE:
            if self.data.prompt["model"] == "gpt-4o":
                return 200
            elif self.data.prompt["model"] == "claude-3-7-sonnet":
                return 500
            elif self.data.prompt["model"] == "gemini-2.5-pro":
                return 500
            else:
                raise ValueError(f"Unknown model: {self.data.prompt['model']}")
        elif self.data.type == GenerationType.IMAGE_TO_3D:
            return 500
        elif self.data.type == GenerationType.SCENE_TO_IMAGE:
            return 20
        elif self.data.type == GenerationType.SCENE_TO_BOARD:
            return 100
        elif self.data.type == GenerationType.SCENE_TO_VIDEO:
            return 500
        else:
            raise ValueError(f"Unknown generation type: {self.data.type}")

    def _data_from_dict(self, data: dict):
        super()._data_from_dict(data)

        if self.data and type(self.data.type) == str:
            self.data.type = GenerationType(self.data.type)
        if self.data and type(self.data.backend) == str:
            self.data.backend = GenerationBackend(self.data.backend)
        if self.data and type(self.data.state) == str:
            self.data.state = GenerationState(self.data.state)
