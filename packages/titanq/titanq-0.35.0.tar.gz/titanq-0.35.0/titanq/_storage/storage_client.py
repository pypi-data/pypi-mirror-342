# Copyright (c) 2024, InfinityQ Technology, Inc.
from enum import Enum
import io
import numpy as np

from abc import ABC, abstractmethod
from typing import Optional, Union

from .._client.model import S3Input, S3Output, UrlInput, UrlOutput

class Ftype(Enum):
    WEIGHTS= "weights"
    BIAS = "bias"
    VARIABLE_BOUNDS= "variable_bounds"
    CONSTRAINT_BOUNDS = "constraint_bounds"
    CONSTRAINT_WEIGHTS = "constraints_weights"
    QUAD_CONSTRAINT_WEIGHTS = "quad_constraint_weights"
    QUAD_CONSTRAINT_BOUNDS = "quad_constraint_bounds"
    QUAD_CONSTRAINT_LINEAR_WEIGHTS = "quad_constraint_linear_weights"
    RESULT = "result"


class StorageClient(ABC):
    """
    Interface to define a storage client.
    Storage is required to upload input files and then download
    response files to/from TitanQ.
    Different storage methods exist; this interface hides the details
    of each option.

    Instances of this class must be used as a context manager.
    No download/upload operation should occur outside of the context.

    Example
    -------

    >>> with storage_client as storage:
    >>>     storage.upload(...)
    """

    def __init__(self):
        pass

    def __enter__(self):
        """
        Initialize the storage, which means the storage may be unusable
        prior to entering the context.
        No download/upload operation should occur outside of the context.
        """
        self._initialize()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Cleanup the storage, which may make the storage unusable.
        No download/upload operation should occur outside of the context.
        """
        self._cleanup()

    @abstractmethod
    def input(self) -> Union[S3Input, UrlInput]:
        """
        Returns the api model for the input of the solve request

        :return: either the s3 or the url input
        """

    @abstractmethod
    def output(self) -> Union[S3Output, UrlOutput]:
        """
        Returns the api model for the output of the solve request

        :return: either the s3 or the url output
        """

    @abstractmethod
    def upload(self, file_type: Ftype, data: bytes):
        """Uploads .npy arrays to the storage client"""

    @abstractmethod
    def wait_for_result_to_be_uploaded_and_download(self) -> bytes:
        """
        Wait until a file is uploaded on the storage client and download it

        :return: content of the result file in bytes
        """

    @abstractmethod
    def _initialize(self) -> None:
        """
        Will be called when entering the runtime context to initialize
        the storage method.

        The child class should avoid initializing the storage in its
        ctor (for example, authenticating to the cloud),
        as client code may be running in Notebook cells, sometimes
        splitting ctor execution and file transfer operations days
        apart.
        """

    @abstractmethod
    def _cleanup(self) -> None:
        """
        Will be called when exiting the runtime context to do whatever
        cleanup the storage method needs to do.
        This may make the storage unusable.
        """

def to_bytes(array: Optional[np.ndarray]) -> Optional[bytes]:
        """
        :return: numpy array as bytes
        """
        if array is None:
            return None

        buffer = io.BytesIO()
        np.save(buffer, array)
        return buffer.getvalue()