from typing import Optional
import imageio
import numpy as np
import gymnasium as gym
import subprocess
import atexit
import os
import time
from imageio_ffmpeg import get_ffmpeg_exe

from sai_rl.sai_console import SAIConsole, SAIStatus
from sai_rl.error import RecordingError


class RecordingManager:
    def __init__(
        self,
        console: SAIConsole,
        env: gym.Env,
        video_path: Optional[str] = None,
        status: Optional[SAIStatus] = None,
    ):
        if status is not None:
            status.update("Setting up recording...")

        self._console = console

        self.width = env.metadata.get("width", 1280)
        self.height = env.metadata.get("height", 720)
        self.engine = env.metadata.get("engine", "pygame")
        self.fps = env.metadata.get("render_fps", 60)

        self.use_virtual_display = (
            os.environ.get("DISPLAY") == ":99" and self.engine == "unity"
        )

        self.ffmpeg_process = None
        self.writer = None

        self.filename = video_path if video_path is not None else "output.mp4"

        self.enabled = video_path is not None
        if not self.enabled:
            self._console.debug("No video path provided, recording disabled.")
        else:
            self._console.debug(f"Recording to {self.filename}")

    def setup_ffmpeg(self, status: Optional[SAIStatus] = None):
        """Setup FFmpeg for virtual display recording"""
        if status is not None:
            status.update("Setting up FFmpeg...")

        try:
            if "DISPLAY" not in os.environ:
                raise RecordingError("No DISPLAY environment variable set")

            ffmpeg_exe = get_ffmpeg_exe()
            self._console.debug(f"Using ffmpeg from: {ffmpeg_exe}")

            ffmpeg_cmd = [
                ffmpeg_exe,
                "-f",
                "x11grab",
                "-s",
                "1280x720",
                "-r",
                str(self.fps),
                "-i",
                os.environ["DISPLAY"],
                "-c:v",
                "libx264",
                "-preset",
                "ultrafast",
                "-pix_fmt",
                "yuv420p",
                "-y",
                self.filename,
            ]

            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            time.sleep(0.5)
            if self.ffmpeg_process.poll() is not None:
                _, stderr = self.ffmpeg_process.communicate()
                raise RecordingError(f"FFmpeg failed to start: {stderr}")

            atexit.register(self.cleanup)
            self._console.success("FFmpeg setup complete.")
        except Exception as e:
            raise RecordingError(f"Failed to setup FFmpeg: {e}")

    def store_frame(self, frame):
        if not self.enabled:
            return

        if self.use_virtual_display:
            return

        if frame is not None:
            if isinstance(frame, np.ndarray):
                if self.writer is not None:
                    self.writer.append_data(frame)
            else:
                raise RecordingError(
                    f"Rendered frame is not a numpy array, got {type(frame)}"
                )

    def start_recording(self, status: Optional[SAIStatus] = None):
        if not self.enabled:
            return

        if status is not None:
            status.update("Starting recording...")

        try:
            if self.use_virtual_display:
                self.setup_ffmpeg(status=status)
            else:
                self.writer = imageio.get_writer(self.filename, fps=self.fps)
        except Exception as e:
            raise RecordingError(f"Failed to start recording: {e}")

    def stop_recording(self, status: Optional[SAIStatus] = None):
        if status is not None:
            status.update("Stopping recording...")

        try:
            if self.writer is not None:
                self.writer.close()
                self.writer = None
            self.cleanup()
        except Exception as e:
            raise RecordingError(f"Error stopping recording: {e}")

    def cleanup(self):
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
