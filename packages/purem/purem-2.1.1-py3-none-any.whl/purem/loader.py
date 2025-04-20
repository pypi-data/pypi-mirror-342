"""
Business Source License 1.1

Copyright (C) 2025 Raman Marozau, raman@worktif.com
Use of this software is governed by the Business Source License included in the LICENSE.TXT file and at www.mariadb.com/bsl11.

Change Date: Never
On the date above, in accordance with the Business Source License, use of this software will be governed by the open source license specified in the LICENSE file.
Additional Use Grant: Free for personal and non-commercial research use only.

SPDX-License-Identifier: BUSL-1.1
"""

import sys
import threading
import time


class Loader:
    def __init__(self, message="Downloading"):
        self._message = message
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self.done = False

    def set_message(self, message: str):
        self._message = message

    def start(self):
        self._thread.start()

    def stop(self):
        self.done = True
        self._thread.join()

    def _animate(self):
        symbols = ["|", "/", "-", "\\"]
        i = 0
        while not self.done:
            sys.stdout.write(f"\r{self._message}... {symbols[i % len(symbols)]}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.1)
        sys.stdout.write(f"\r{self._message}... done.\n")
