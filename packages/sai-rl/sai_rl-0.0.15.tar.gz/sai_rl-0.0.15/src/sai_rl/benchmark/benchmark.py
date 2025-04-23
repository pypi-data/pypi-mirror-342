import time
from typing import Optional, TypedDict

import gymnasium as gym

from rich.live import Live
from rich.table import Table

from sai_rl.sai_console import SAIConsole, SAIStatus
from sai_rl.benchmark.recording_manager import RecordingManager
from sai_rl.model import ModelManager


class BenchmarkResults(TypedDict):
    status: Optional[str]
    score: Optional[float]
    duration: Optional[int]
    logs: Optional[str]
    error: Optional[str]


def generate_table(
    console: SAIConsole,
    timestep: int,
    current_score: float,
    time_elapsed: float,
    timeout: int,
) -> Table:
    table = console.table(
        title="Benchmark Progress", show_header=True, show_lines=False
    )

    # Add all columns with their values in the header
    table.add_column("Steps", justify="center", style="cyan")
    table.add_column("Score", justify="center", style="green")
    table.add_column("Time", justify="center", style="yellow")
    table.add_column("Remaining", justify="center", style="red")

    # Add a single row with all values
    table.add_row(
        str(timestep),
        f"{current_score:.2f}",
        f"{time_elapsed:.1f}s",
        f"{timeout - time_elapsed:.1f}s",
    )

    return table


def run_benchmark(
    console: SAIConsole,
    env: gym.Env,
    model: Optional[ModelManager] = None,
    reset_vars: Optional[dict] = None,
    video_path: Optional[str] = None,
    timeout: int = 600,
    keep_env_alive: bool = False,
    status: Optional[SAIStatus] = None,
    show_progress: bool = False,
) -> BenchmarkResults:
    if status is not None:
        status.update("Starting benchmark...")

    console.debug("\nRunning Benchmark:")
    console.debug(f"Environment: {env.__class__.__name__}")
    console.debug(f"Model: {'Provided' if model else 'Random Actions'}")
    console.debug(f"Video Recording: {'Enabled' if video_path else 'Disabled'}")
    console.debug(f"Timeout: {timeout} seconds")
    console.debug(f"Keep Environment: {'Yes' if keep_env_alive else 'No'}\n")

    results: BenchmarkResults = {
        "status": None,
        "score": None,
        "duration": None,
        "logs": None,
        "error": None,
    }
    recorder = None

    try:
        recorder = RecordingManager(
            console=console, env=env, video_path=video_path, status=status
        )
        recorder.start_recording(status=status)

        done = False
        truncated = False
        obs, _ = env.reset(**(reset_vars or {}))
        score = 0.0
        timestep = 0
        start_time = time.time()

        if status is not None:
            status.update("Running benchmark...")
            status.stop()

        live = None
        if show_progress:
            live = Live(
                generate_table(console, 0, 0.0, 0.0, timeout),
                console=console.console,
                refresh_per_second=15,
            )
            live.start()

        try:
            while not done and not truncated and (time.time() - start_time) < timeout:
                if model is not None:
                    action = model.get_action(obs)
                else:
                    action = env.action_space.sample()

                obs, reward, done, truncated, _ = env.step(action)
                score += float(reward)

                frame = env.render()
                recorder.store_frame(frame)

                if live:
                    time_elapsed = time.time() - start_time
                    timestep += 1
                    live.update(
                        generate_table(console, timestep, score, time_elapsed, timeout)
                    )
        finally:
            if live:
                live.stop()

        if status is not None:
            console.print()
            status.start()
            status.update("Benchmark complete!")

        end_time = time.time()
        recorder.stop_recording(status=status)

        results: BenchmarkResults = {
            "status": "success" if (end_time - start_time) < timeout else "timeout",
            "score": score,
            "duration": int(end_time - start_time),
            "logs": None,
            "error": None,
        }

    except Exception as e:
        results: BenchmarkResults = {
            "status": "error",
            "score": 0.0,
            "duration": 0,
            "logs": None,
            "error": str(e),
        }
    finally:
        if status is not None:
            status.update("Cleaning up...")

        if not keep_env_alive:
            try:
                env.close()
            except:  # noqa: E722
                pass

        if recorder is not None:
            try:
                recorder.cleanup()
            except:  # noqa: E722
                pass

    return results
