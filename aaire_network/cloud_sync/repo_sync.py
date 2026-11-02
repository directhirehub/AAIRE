#!/usr/bin/env python3
"""Cloud and GitHub repository synchronization helper."""
from __future__ import annotations
import subprocess

class RepoSync:
    @staticmethod
    def commit_and_push(folder_path: str, message: str) -> bool:
        try:
            subprocess.run(["git", "add", folder_path], check=True)
            res = subprocess.run(["git", "diff", "--staged", "--quiet"])
            if res.returncode == 0:
                return True  # No changes
            subprocess.run(["git", "commit", "-m", message], check=True)
            subprocess.run(["git", "push"], check=True)
            return True
        except Exception:
            return False
          
