"""
Business Source License 1.1

Copyright (C) 2025 Raman Marozau, raman@worktif.com
Use of this software is governed by the Business Source License included in the LICENSE.TXT file and at www.mariadb.com/bsl11.

Change Date: Never
On the date above, in accordance with the Business Source License, use of this software will be governed by the open source license specified in the LICENSE file.
Additional Use Grant: Free for personal and non-commercial research use only.

SPDX-License-Identifier: BUSL-1.1
"""

import base64
import ctypes
import json
import os
import shutil
import ssl
import urllib.request
import zipfile
from typing import List, Optional, Dict

import certifi as certifi
import numpy as np
from numpy import ndarray

from purem.env_config import load_env_config
from purem.file_structure import FileStructure
from purem.loader import Loader
from purem.logger import Logger
from purem.utils import _compute_shifted_jit


class Purem:
    """
    Summary of what the class does.

    The Purem class is used to manage and handle the initialization, configuration, and
    operation of the Purem environment and its associated runtime, including license management,
    binary handling, and API configuration. It centralizes the setup of the Purem runtime,
    ensuring that all necessary binaries, license checks, and configurations are in place.

    The class supports downloading and extracting binaries, setting up runtime libraries, and providing utility
    methods such as softmax computation, license validation, and URL construction to interact with remote
    and local systems.

    :ivar _license_key: The license key used for Purem initialization and validation.
    :type _license_key: Optional[str]
    :ivar _lib: The dynamically loaded library object for the Purem binary.
    :type _lib: ctypes.CDLL
    :ivar _download_binary_url: The URL for downloading the Purem binary.
    :type _download_binary_url: Optional[str]
    :ivar _ctx: SSL context used for secure connections, initialized using the system's certificates.
    :type _ctx: ssl.SSLContext
    :ivar _file_structure: Manages file paths and structures related to Purem binary and runtime.
    :type _file_structure: FileStructure
    :ivar _binary_path: The path to the main Purem binary.
    :type _binary_path: pathlib.Path
    :ivar _binary_project_root_path: The path to the project root Purem binary.
    :type _binary_project_root_path: pathlib.Path
    :ivar _binary_archive_path: The path where the binary archive is stored.
    :type _binary_archive_path: pathlib.Path
    :ivar _binary_archive_path_tmp: The temporary path for binary archive operations.
    :type _binary_archive_path_tmp: pathlib.Path
    :ivar _env: Environment configuration used in Purem operations, including URLs.
    :type _env: Any
    :ivar _config_url: URL for retrieving Purem configuration, either from an environment variable or a default.
    :type _config_url: str
    :ivar _loader: Loader utility for displaying loading messages during lengthy operations.
    :type _loader: Loader
    :ivar _log: Logger utility for tracking and managing logging in the Purem operations.
    :type _log: Logger
    """

    def __init__(self, licenced_key: Optional[str] = None):
        self._license_key = licenced_key or None
        self._lib = None
        self._download_binary_url = None
        self._ctx = ssl.create_default_context(cafile=certifi.where())
        self._file_structure = FileStructure()
        self._binary_path = self._file_structure.get_binary_path()
        self._binary_project_root_path = (
            self._file_structure.get_binary_project_root_path()
        )
        self._binary_archive_path = self._file_structure.get_binary_archive_path()
        self._binary_archive_path_tmp = (
            self._file_structure.get_binary_archive_path_tmp()
        )
        self._env = load_env_config()
        self._config_url = (
                self._env.PUREM_CONFIG_URL
                or "https://api.worktif.com/v2/portal/products/purem/config"
        )
        self._loader = Loader()
        self._log = Logger()

    def configure(self, license_key: Optional[str] = None) -> None:
        if self._license_key is None and license_key is not None:
            self._license_key = license_key
        if self._license_key is None:
            raise ValueError(
                self._log.info(
                    "Purem requires a valid license key to initialize.\n"
                    "You can obtain your key at https://worktif.com or through your enterprise deployment."
                )
            )

        self._set_binary()

    def softmax(self, array: ndarray) -> ndarray:
        array_size = len(array)
        array = array.astype(np.float32, copy=False)
        shifted_arr = np.empty(array_size, dtype=np.float32)
        _compute_shifted_jit(array, shifted_arr)
        ptr = shifted_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        self._lib.purem(ptr, array_size)
        return shifted_arr

    def clean_softmax(self, arr: [np.float32], size) -> List[any]:
        return self._lib.purem(arr, size)

    def _build_url(self, config: dict) -> Optional[str]:
        if config is None:
            return None
        base = config.get("base_url", "").rstrip("/")
        protocol = config.get("protocol", "https")
        path = config.get("pathname", "").lstrip("/")
        binary_url = f"{protocol}://{base}/{path}{self._license_key}"
        return binary_url

    def _tune_binary(self):
        self._lib = ctypes.CDLL(str(self._binary_path))
        self._lib.purem.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_size_t]
        self._lib.purem.restype = None

    def _tune_project_root_binary(self):
        self._lib = ctypes.CDLL(str(self._binary_project_root_path))
        self._lib.purem.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_size_t]
        self._lib.purem.restype = None

    def _load_from_latest_cdn_index(self) -> Optional[Dict]:
        try:
            if self._config_url is not None:
                req = urllib.request.Request(
                    self._config_url,
                )

                with urllib.request.urlopen(req, context=self._ctx) as response:
                    return json.load(response)
            else:
                return None

        except Exception:
            return None

    def _set_binary(self):
        if os.path.exists(self._binary_path):
            self._tune_binary()
        elif os.path.exists(self._binary_project_root_path):
            self._tune_project_root_binary()
        elif not self._license_key:
            raise ValueError(
                self._log.info(
                    "Purem requires a valid license key to initialize.\n"
                    "You can obtain your key at https://worktif.com or through your enterprise deployment."
                )
            )
        else:
            try:
                self._loader.set_message(
                    "Initializing Purem licensed runtime locally..."
                )
                self._loader.start()
                self._download_binary_url = (
                        self._build_url(self._load_from_latest_cdn_index())
                        or f"{self._env.PUREM_DOWNLOAD_BINARY_URL}{self._license_key}"
                )
                self._download_and_extract_binary()
                self._loader.stop()

            except Exception as e:
                raise RuntimeError(
                    self._log.info(
                        "We couldn't load your Purem binary at this time.\n"
                        "This may be a local issue or license mismatch.\n"
                        "Please try again – or contact us at support@worktif.com.\n"
                        "We're here to help you run at full power."
                    )
                )

            try:
                self._tune_project_root_binary()
            except Exception as e:
                raise RuntimeError(
                    self._log.info(
                        "It appears your Purem licensed binary can not be loaded. Please try again. If the problem "
                        "persists, please contact us at support@worktif.com. Thank you for your patience."
                    )
                )

    def _download_and_extract_binary(self):
        req = urllib.request.Request(
            self._download_binary_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        try:
            with urllib.request.urlopen(req, context=self._ctx) as response:
                with open(self._binary_archive_path_tmp, "wb") as out_file:
                    shutil.copyfileobj(response, out_file)

            shutil.move(self._binary_archive_path_tmp, self._binary_archive_path)
        except Exception as e:
            raise RuntimeError(
                self._log.info(
                    f"The Purem archive appears to be corrupted or incomplete.\nDetails: {e}"
                    "Please ensure the package downloaded fully and is unmodified.\n"
                    "Need help? Contact support@worktif.com – we'll assist right away.\n"
                )
            )

        try:
            with zipfile.ZipFile(self._binary_archive_path, "r") as zip_ref:
                zip_ref.extractall(
                    self._file_structure.dirs.project_root_binary_dir_path
                )
            self._log.info_new_line(
                f"Purem binary extracted to: {self._file_structure.dirs.binary_dir_path}"
            )
        except zipfile.BadZipFile as e:
            raise RuntimeError(
                self._log.info(
                    f"The Purem archive appears to be corrupted or incomplete.\nDetails: {e}"
                    "Please ensure the package downloaded fully and is unmodified.\n"
                    "Need help? Contact support@worktif.com – we'll assist right away.\n"
                )
            )

        self._binary_archive_path.unlink()
