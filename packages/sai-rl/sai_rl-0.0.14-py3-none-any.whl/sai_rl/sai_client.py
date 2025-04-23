from typing import Literal, Optional
from io import StringIO

import os
import gymnasium as gym
import json
import random
import string
import sys
import requests

from rich.align import Align
from rich.text import Text

from sai_rl.package_control import PackageControl
from sai_rl.sai_console import SAIConsole, SAIStatus
from sai_rl.utils import TeeIO, config
from sai_rl.error import (
    BenchmarkError,
    CompetitionError,
    MatchError,
    SubmissionError,
    SetupError,
    EnvironmentError,
)
from sai_rl.api import APIClient
from sai_rl.action_function import ActionFunctionManager
from sai_rl.model import ModelManager
from sai_rl.types import ModelType, ModelLibraryType
from sai_rl.benchmark import run_benchmark, BenchmarkResults


class SAIClient(object):
    """
    Main client for interacting with the SAI platform.

    The SAIClient provides methods for:
    - Managing competitions and submissions
    - Loading and evaluating models
    - Working with action functions
    - Managing environment packages
    - Running benchmarks and watching agents

    Args:
        env_id (Optional[str]): ID of environment to load
        api_key (Optional[str]): API key for authentication
        competition_id (Optional[str]): ID of competition to load
        action_function_id (Optional[str]): ID of action function to use
        api_base (Optional[str]): Custom API endpoint
        max_network_retries (Optional[int]): Max API retry attempts
        console (Optional[SAIConsole]): Custom console for output

    Examples:
        Basic usage:
        >>> client = SAIClient(api_key="your-api-key")
        >>> client.load_competition("comp-123456")
        >>> client.watch()  # Watch random agent

        Using a model:
        >>> model = torch.load("my_model.pt")
        >>> client.benchmark(model=model, model_type="pytorch")

        Working with action functions:
        >>> client.load_action_fn("./my_action.py")
        >>> client.submit_action_fn()
    """

    def __init__(
        self,
        env_id: Optional[str] = None,
        api_key: Optional[str] = None,
        *,
        competition_id: Optional[str] = None,
        action_function_id: Optional[str] = None,
        api_base: Optional[str] = None,
        max_network_retries: Optional[int] = None,
        console: Optional[SAIConsole] = None,
        ignore_editable: bool = False,
        is_server: bool = False,
    ):
        # Setup logging
        if is_server:
            self._log_capture = StringIO()
            self._original_stdout = sys.stdout
            sys.stdout = TeeIO(self._log_capture, sys.__stdout__)
        else:
            self._log_capture = None
            self._original_stdout = None
        self._console = console or SAIConsole()

        with self._console.status("Loading SAI CLI...") as status:
            # Setup API client
            self._api = APIClient(
                console=self._console,
                api_key=api_key,
                api_base=api_base,
                max_network_retries=max_network_retries,
            )

            # Setup package control
            self._package_control = PackageControl(
                api=self._api,
                console=self._console,
                ignore_editable=ignore_editable,
            )

            self._console.display_title(
                self._package_control._get_package_version("sai-rl") or "unknown",
                self._package_control._is_editable_install("sai-rl"),
            )

            skip_check_version = not self._package_control._is_editable_install(
                "sai-rl"
            )
            self._package_control.setup(skip_check_version, status)

            # Global variables
            self._env: Optional[gym.Env] = None

            self._match = {}
            self._competition = {}
            self._environment = {}
            self._action_function = ActionFunctionManager(
                api=self._api,
                console=self._console,
                download_path=config.temp_path,
            )

            # Load competition or environment
            if competition_id is not None:
                self._console.print()
                self._load_competition(competition_id, status)
            elif env_id is not None:
                self._console.print()
                self._load_environment(env_id, status)

            if action_function_id is not None:
                self._console.print()
                self._action_function.load(action_function_id)

            self._console.print()

    # ---- Internal Utility Methods ----
    def _check_competition_loaded(self) -> bool:
        if not self._competition or not self._match:
            raise CompetitionError("Competition not loaded")
        assert self._competition is not None
        assert self._match is not None
        return True

    def _check_setup(self) -> bool:
        if not self._package_control.setup_complete:
            raise SetupError("Setup not complete")
        assert self._package_control.setup_complete
        return True

    def _get_logs(self) -> str:
        if self._log_capture:
            return self._log_capture.getvalue()
        return ""

    def _check_environment_loaded(self) -> bool:
        if not self._environment:
            raise EnvironmentError("Environment not loaded")
        assert self._environment is not None
        return True

    def _check_environment_or_competition_loaded(self) -> bool:
        if not self._environment and not self._competition:
            raise EnvironmentError("Neither environment nor competition loaded")
        return True

    # ---- Print Methods ----
    def _print_competition(self):
        if not self._competition:
            raise CompetitionError("Competition not loaded")

        competition_name = self._competition.get("name")
        competition_id = self._competition.get("id")
        competition_slug = self._competition.get("slug")
        env_name = self._competition.get("env_name")
        env_lib = self._competition.get("env_lib")
        env_vars = self._competition.get("env_vars")
        link = self._competition.get("link")

        title = f'"{competition_name}" ({competition_slug})'

        info_group = f"""[bold cyan]
Env Name:[/bold cyan]    {env_name}
[bold cyan]Env Library:[/bold cyan] {env_lib}
[bold cyan]Env Vars:[/bold cyan]    {json.dumps(env_vars, indent=2)}"""

        link_group = f"[link={link}]View in Platform →[/link]"

        env_info = self._console.group(
            Align.left(Text.from_markup(info_group)),
            Align.right(Text.from_markup(link_group)),
        )

        panel = self._console.panel(env_info, title=title, padding=(0, 2))
        self._console.print(panel)

    def _print_submission_details(
        self,
        name: str,
        model_manager: ModelManager,
        use_onnx: bool = False,
        action_function_id: Optional[str] = None,
    ):
        if not self._competition:
            raise CompetitionError("Competition not loaded")

        title = f'"{name}" Submission Details'

        info_group = f"""[bold cyan]
Competition ID:[/bold cyan]      {self._competition.get("id")}
[bold cyan]Competition Name:[/bold cyan]    {self._competition.get("name")}
[bold cyan]Model Type:[/bold cyan]          {model_manager.model_type if not use_onnx else "onnx"}
[bold cyan]Action Function ID:[/bold cyan]   {self._action_function.id or action_function_id or "N/A"}
[bold cyan]Action Function Name:[/bold cyan] {self._action_function.name or "N/A"}"""

        submission_info = self._console.group(Align.left(Text.from_markup(info_group)))

        panel = self._console.panel(submission_info, title=title, padding=(0, 2))
        self._console.print(panel)

    def _print_environment(self):
        if not self._environment:
            raise EnvironmentError("Environment not loaded")

        environment_name = self._environment.get("name")
        env_name = self._environment.get("env_name")
        env_lib = self._environment.get("env_library")
        link = self._environment.get("link")

        title = f'"{environment_name}" ({env_lib})'

        info_group = f"""[bold cyan]
Env Name:[/bold cyan]    {env_name}
[bold cyan]Env Library:[/bold cyan] {env_lib}"""

        link_group = f"[link={link}]View in Platform →[/link]"

        env_info = self._console.group(
            Align.left(Text.from_markup(info_group)),
            Align.right(Text.from_markup(link_group)),
        )

        panel = self._console.panel(env_info, title=title, padding=(0, 2))
        self._console.print(panel)

    # ---- Load Methods ----
    def _load_competition(
        self, competition_id: str, status: Optional[SAIStatus] = None
    ):
        if status:
            status.update(f"Loading competition {competition_id}...")

        self._competition = self._api.competition.get(competition_id)
        if not self._competition:
            raise CompetitionError("Competition not found")

        self._print_competition()

        env_lib = self._competition.get("env_lib")
        if env_lib:
            self._package_control.load(env_lib, status=status)

        self._console.success("Successfully loaded competition.")

        return self._competition

    def _load_match(self, match_id: str, status: Optional[SAIStatus] = None):
        if status:
            status.update("Loading match data...")

        self._match = self._api.match.get(match_id)
        if not self._match:
            raise MatchError("Match not found")

        self._load_competition(self._match.get("competition_id"), status=status)

        if self._match.get("action_function_url"):
            self._action_function.load(self._match.get("action_function_url"))

        self._console.success("Successfully loaded match.")

        return self._match

    def _load_environment(
        self, environment_id: str, status: Optional[SAIStatus] = None
    ):
        if status:
            status.update(f"Loading environment {environment_id}...")

        self._environment = self._api.environment.get(environment_id)
        if not self._environment:
            raise EnvironmentError("Environment not found")

        self._print_environment()

        env_lib = self._environment.get("env_library")
        if env_lib:
            self._package_control.load(env_lib, status=status)

        self._console.success("Successfully loaded environment.")

        return self._environment

    # ---- Make Methods ----
    def _make_new_env(
        self,
        render_mode: Literal["human", "rgb_array", "depth_array"] = "human",
        status: Optional[SAIStatus] = None,
        **kwargs,
    ) -> gym.Env:
        if status:
            status.update("Creating new environment...")

        self._check_environment_or_competition_loaded()

        if self._env is not None:
            self._env.close()

        if self._environment:  # Use environment data if available
            env_name = self._environment.get("env_name") or ""  # type: ignore
            env_vars = {**kwargs}  # type: ignore
        else:  # Fall back to competition data
            env_name = self._competition.get("env_name") or ""  # type: ignore
            env_vars = self._competition.get("env_vars") or {}  # type: ignore

        self._env = gym.make(
            env_name,
            render_mode=render_mode,
            **env_vars,  # type: ignore
        )

        self._env.reset()

        return self._env

    def _load_model(
        self,
        model: ModelType,
        model_type: Optional[ModelLibraryType] = None,
        status: Optional[SAIStatus] = None,
    ):
        if status:
            status.update("Loading model...")

        if self._env is None:
            raise EnvironmentError("Environment not loaded")

        return ModelManager(
            console=self._console,
            env=self._env,
            action_manager=self._action_function,
            model=model,
            model_type=model_type,
            status=status,
        )

    # ---- Server Methods ----
    def _submit_match_results(
        self,
        results: BenchmarkResults,
        match_id: Optional[str] = None,
        video_path: Optional[str] = None,
        status: Optional[SAIStatus] = None,
    ):
        if status:
            status.update("Submitting match results...")

        try:
            if match_id is None:
                raise MatchError("Match ID required")

            results["logs"] = self._get_logs()
            submission = self._api.match.submit_results(match_id, results)  # type: ignore

            try:
                if results["status"] == "success" and video_path:
                    video_url = submission.get("videoUrl")  # type: ignore

                    with open(video_path, "rb") as video_file:
                        upload_response = requests.put(video_url, data=video_file)
                        upload_response.raise_for_status()
                    self._console.success("Match video uploaded successfully")
            except Exception as e:
                raise MatchError(f"Unable to upload match video: {e}")

        except Exception as e:
            self._console.error(f"Unable to upload match results: {e}")

        return results

    # ---- Private Properties ----
    @property
    def _reset_vars(self):
        seed = os.getenv("SAI_SEED")
        return {"seed": int(seed)} if seed else {}

    ############################################################
    # Public Methods
    ############################################################

    # ---- Action Function Methods ----
    def get_action_fn(self):
        """
        Gets an instance of the currently loaded action function.

        Returns:
            ActionFunction: An instantiated action function object
            None: If no action function is loaded

        Examples:
            >>> action_fn = client.get_action_fn()
            >>> if action_fn:
            ...     action = action_fn(observation)
        """
        self._check_setup()
        self._console.print()

        result = self._action_function.get()()  # type: ignore

        self._console.print()
        return result

    def load_action_fn(self, path: str):
        """
        Loads an action function from a given path.

        Args:
            path (str): Can be one of:
                - Local file path (e.g., "./my_action.py")
                - URL (e.g., "https://example.com/action.py")
                - Platform ID (12-character string)

        Returns:
            dict: Information about the loaded action function

        Raises:
            ActionFunctionError: If loading fails

        Examples:
            >>> # Load from local file
            >>> client.load_action_fn("./my_action.py")
            >>>
            >>> # Load from platform
            >>> client.load_action_fn("action-123456")
        """
        self._check_setup()
        self._console.print()

        results = self._action_function.load(path)

        self._console.print()
        return results

    def submit_action_fn(self):
        """
        Submits the currently loaded local action function to the platform.

        Returns:
            dict: Information about the submitted action function including:
                - id: The platform ID
                - name: The action function name
                - other metadata

        Raises:
            ActionFunctionError: If submission fails or no local function is loaded

        Examples:
            >>> client.load_action_fn("./my_action.py")
            >>> result = client.submit_action_fn()
            >>> print(f"Submitted as {result['id']}")
        """
        self._check_setup()
        self._console.print()

        with self._console.status("Submitting action function...") as status:
            results = self._action_function.submit(status=status)

        self._console.print()
        return results

    def reset_action_fn(self):
        """
        Clears the currently loaded action function.

        This removes all references to the current action function, allowing
        you to load a different one or start fresh.

        Examples:
            >>> client.reset_action_fn()
            >>> client.load_action_fn("./new_action.py")
        """
        self._check_setup()
        return self._action_function.reset()

    # ---- Competition Methods ----
    def get_competition(self):
        """
        Gets information about the currently loaded competition.

        Returns:
            dict: Competition information including:
                - id: Competition ID
                - name: Competition name
                - env_name: Environment name
                - env_lib: Environment library
                - env_vars: Environment variables
            None: If no competition is loaded

        Examples:
            >>> comp = client.get_competition()
            >>> if comp:
            ...     print(f"Using {comp['env_name']}")
        """
        self._check_setup()
        self._check_competition_loaded()
        return self._competition

    def load_competition(self, competition_id: str):
        """
        Loads a competition by its ID.

        Args:
            competition_id (str): Platform ID of the competition to load

        Returns:
            dict: Loaded competition information

        Raises:
            CompetitionError: If competition cannot be loaded

        Examples:
            >>> client.load_competition("comp-123456")
            >>> client.watch()  # Watch random agent
        """
        self._check_setup()

        with self._console.status(f"Loading competition {competition_id}...") as status:
            return self._load_competition(competition_id, status=status)

    def list_competitions(self, show_table: bool = True):
        """
        Lists all available competitions.

        Args:
            show_table (bool): Whether to display a formatted table of competitions

        Returns:
            list[dict]: List of competition information including:
                - id: Competition ID
                - name: Competition name
                - description: Competition description
                - environment_name: Name of the environment
                - link: URL to view in platform

        Examples:
            >>> # Show table and get data
            >>> competitions = client.list_competitions()
            >>>
            >>> # Get data only
            >>> competitions = client.list_competitions(show_table=False)
        """
        self._check_setup()
        self._console.print()

        with self._console.status("Loading competitions...") as status:
            competitions = self._api.competition.list()
            if competitions is None:
                self._console.warning("No competitions found.")
                return []

            if show_table:
                status.update("Displaying competitions...")
                table = self._console.table("Available Competitions")

                table.add_column("ID", style="yellow")
                table.add_column("Name", style="cyan", no_wrap=True)
                table.add_column("Description", style="magenta")
                table.add_column("Environment", style="green")
                table.add_column("View in Platform", style="green", justify="center")

                for comp in competitions:
                    table.add_row(
                        comp.get("slug"),
                        comp.get("name"),
                        comp.get("description"),
                        comp.get("environment_name"),
                        f"[link={comp.get('link')}]View →[/link]",
                    )

                self._console.print(table)
                self._console.print()

            return competitions

    def reset_competition(self):
        """
        Clears the currently loaded competition.

        This removes all references to the current competition, allowing
        you to load a different one or start fresh.

        Examples:
            >>> client.reset_competition()
            >>> client.load_competition("new-comp-id")
        """
        self._check_setup()
        self._check_competition_loaded()
        self._competition = {}

    # ---- Submission Methods ----
    def list_submissions(self, show_table: bool = True):
        """
        Lists all your submissions across competitions.

        Args:
            show_table (bool): Whether to display a formatted table of submissions
                If True, shows a rich table with clickable platform links
                If False, returns data only

        Returns:
            list[dict]: List of submission information including:
                - id: Submission ID
                - name: Submission name
                - status: Current status ("pending", "running", "completed", "failed")
                - last_score: Most recent evaluation score
                - competition: Name of the competition
                - link: URL to view submission in platform

        Note: Returns empty list if no submissions are found

        Examples:
            >>> # Show table and get data
            >>> submissions = client.list_submissions()
            >>>
            >>> # Get data only
            >>> submissions = client.list_submissions(show_table=False)
            >>> for sub in submissions:
            ...     print(f"{sub['name']}: {sub['last_score']}")
            >>>
            >>> # Filter completed submissions
            >>> completed = [s for s in submissions
            ...             if s['status'] == 'completed']
            >>> print(f"Found {len(completed)} completed submissions")
        """
        self._check_setup()
        self._console.print()

        with self._console.status("Loading submissions...") as status:
            submissions = self._api.submission.list()
            if submissions is None:
                self._console.warning("No submissions found.")
                return []

            if show_table:
                status.update("Displaying submissions...")
                table = self._console.table("Your Submissions")
                table.add_column("ID", style="yellow")
                table.add_column("Name", style="cyan", no_wrap=True)
                table.add_column("Model Type", style="magenta")
                table.add_column("Competition", style="cyan")
                table.add_column("Environment", style="green")
                table.add_column("Last Score", style="bright_green", justify="right")
                table.add_column("SAIStatus", style="bright_yellow")
                table.add_column(
                    "View in Platform", style="bright_blue", justify="center"
                )

                for submission in submissions:
                    table.add_row(
                        submission.get("id"),
                        submission.get("name"),
                        submission.get("model_type"),
                        submission.get("competition_name"),
                        submission.get("environment_name"),
                        submission.get("last_score"),
                        submission.get("status"),
                        f"[link={submission.get('link')}]View →[/link]"
                        if submission.get("link")
                        else "",
                    )

                self._console.print(table)
                self._console.print()

            return submissions

    # ---- Environment Methods ----
    def get_environment(self):
        """
        Gets information about the currently loaded environment.

        Returns:
            dict: Environment information including:
                - id: Environment ID
                - slug: Environment slug
                - name: Environment name
                - env_name: Environment name in the registry
                - env_library: Environment library
            None: If no environment is loaded

        Examples:
            >>> env = client.get_environment()
            >>> if env:
            ...     print(f"Using {env['env_name']}")
        """
        self._check_setup()
        if not self._environment:
            self._console.warning("No environment is loaded")
            return None
        return self._environment

    def load_environment(self, environment_id: str):
        """
        Loads an environment by its ID.

        Args:
            environment_id (str): Platform ID of the environment to load

        Returns:
            dict: Loaded environment information

        Raises:
            EnvironmentError: If environment cannot be loaded

        Examples:
            >>> client.load_environment("env-123456")
            >>> client.watch()  # Watch random agent
        """
        self._check_setup()

        with self._console.status(f"Loading environment {environment_id}...") as status:
            return self._load_environment(environment_id, status=status)

    def list_environments(self, show_table: bool = True):
        """
        Lists all available environments.

        Args:
            show_table (bool): Whether to display a formatted table of environments

        Returns:
            list[dict]: List of environment information including:
                - id: Environment ID
                - name: Environment name
                - description: Environment description
                - link: URL to view in platform

        Examples:
            >>> # Show table and get data
            >>> environments = client.list_environments()
            >>>
            >>> # Get data only
            >>> environments = client.list_environments(show_table=False)
        """
        self._check_setup()
        self._console.print()

        with self._console.status("Loading environments...") as status:
            environments = self._api.environment.list()
            if environments is None:
                self._console.warning("No environments found.")
                return []

            if show_table:
                status.update("Displaying environments...")
                table = self._console.table("Available Environments")

                table.add_column("ID", style="yellow")
                table.add_column("Name", style="cyan", no_wrap=True)
                table.add_column("Description", style="magenta")
                table.add_column("View in Platform", style="green", justify="center")

                for env in environments:
                    table.add_row(
                        env.get("env_name"),
                        env.get("name"),
                        env.get("description"),
                        f"[link={env.get('link')}]View →[/link]",
                    )

                self._console.print(table)
                self._console.print()

            return environments

    def reset_environment(self):
        """
        Clears the currently loaded environment.

        This removes all references to the current environment, allowing
        you to load a different one or start fresh.

        Examples:
            >>> client.reset_environment()
            >>> client.load_environment("new-env-id")
        """
        self._check_setup()
        if not self._environment:
            self._console.warning("No environment is loaded")
            return
        self._environment = {}

    def make_env(self, render_mode: Literal["human", "rgb_array"] = "human", **kwargs):
        """
        Creates a new instance of the competition environment.

        Args:
            render_mode (Literal["human", "rgb_array"]): How to render the environment
                - "human": Display environment in a window
                - "rgb_array": Return RGB array for video recording
            **kwargs: Additional keyword arguments to pass to the environment
                Note: These will be ignored when using a competition environment

        Returns:
            gym.Env: A Gymnasium environment instance

        Raises:
            CompetitionError: If no competition is loaded

        Examples:
            >>> env = client.make_env()
            >>> obs, _ = env.reset()
            >>> env.render()

            >>> # With custom environment args (only works for non-competition environments)
            >>> env = client.make_env(truncate_episode_steps=100)
        """
        self._check_setup()
        self._check_environment_or_competition_loaded()

        # Check if we're using a competition and have additional kwargs
        if self._competition and kwargs:
            self._console.warning(
                "Additional keyword arguments are ignored when using a competition environment "
                "to maintain compatibility with the competition settings."
            )
            return self._make_new_env(render_mode)

        # Using an environment (not competition) or no additional kwargs
        return self._make_new_env(render_mode, **kwargs)

    def watch(
        self,
        model: Optional[ModelType] = None,
        model_type: Optional[ModelLibraryType] = None,
        runs: int = 1,
    ):
        """
        Watch a model (or random agent) interact with the environment.

        Args:
            model (Optional[ModelType]): Model to watch. Can be one of:
                - PyTorch model (torch.nn.Module)
                - TensorFlow model (tf.keras.Model)
                - Stable-Baselines3 model (BaseAlgorithm)
                - ONNX model (OnnxAgentWrapper)
                - URL or file path (str)
                If None, uses random actions
            model_type (Optional[ModelLibraryType]): Framework used. One of:
                - "pytorch"
                - "tensorflow"
                - "stable_baselines3"
                - "onnx"
            runs (int): Number of episodes to run (default: 1)

        Raises:
            BenchmarkError: If watching fails
            CompetitionError: If no competition is loaded

        Examples:
            >>> # Watch random agent
            >>> client.watch()
            >>>
            >>> # Watch PyTorch model
            >>> model = torch.load("model.pt")
            >>> client.watch(model=model, model_type="pytorch", runs=3)
        """
        self._check_setup()
        self._check_environment_or_competition_loaded()

        self._console.print()
        with self._console.status("Setting up environment...") as status:
            try:
                self._make_new_env(render_mode="human")

                if self._env is None or self._env.spec is None:
                    raise EnvironmentError("Environment not loaded")

                if model is not None:
                    model_manager = self._load_model(
                        model=model,
                        model_type=model_type,
                    )
                    status.update(
                        f"Watching {model_manager.model_type} model in '{self._env.spec.id}' environment..."
                    )
                else:
                    model_manager = None
                    status.update(
                        f"Watching random agent in '{self._env.spec.id}' environment..."
                    )

                self._console.print()

                for run_index in range(runs):
                    self._console.info(f"Running watch {run_index + 1} of {runs}...")

                    results = run_benchmark(
                        console=self._console,
                        env=self._env,
                        model=model_manager,
                        reset_vars=self._reset_vars,
                        keep_env_alive=True if run_index == runs - 1 else False,
                    )

                    if results.get("status") == "error":
                        raise BenchmarkError(results.get("error"))

                self._console.success(
                    f"Watching completed for '{self._env.spec.id}' environment."
                )

                self._console.print()

            except Exception as e:
                if self._env is not None and self._env.spec is not None:
                    self._console.error(
                        f"Unable to watch model in '{self._env.spec.id}' environment: {e}"
                    )
                else:
                    self._console.error(f"Unable to watch model: {e}")
                raise BenchmarkError(e)

    def benchmark(
        self,
        model: Optional[ModelType] = None,
        model_type: Optional[ModelLibraryType] = None,
        video_path: Optional[str] = None,
        show_progress: bool = True,
        throw_errors: bool = True,
        timeout: int = 120
    ) -> BenchmarkResults:
        """
        Run benchmark evaluation of a model.

        Args:
            model (Optional[ModelType]): Model to evaluate. Can be one of:
                - PyTorch model (torch.nn.Module)
                - TensorFlow model (tf.keras.Model)
                - Stable-Baselines3 model (BaseAlgorithm)
                - ONNX model (OnnxAgentWrapper)
                - URL or file path (str)
                If None, uses random actions
            model_type (Optional[ModelLibraryType]): Framework used. One of:
                - "pytorch"
                - "tensorflow"
                - "stable_baselines3"
                - "onnx"
            video_path (Optional[str]): Path to save video recording
                If None, no video is recorded
            show_progress (bool): Whether to show progress bar during benchmark
                Defaults to True
            throw_errors (bool): Whether to raise exceptions on errors
                If False, returns error in results instead
                Defaults to True

        Returns:
            BenchmarkResults: Results containing:
                - status: "success", "error", or "timeout"
                - score: Total reward achieved
                - duration: Time taken in seconds
                - error: Error message if failed

        Raises:
            BenchmarkError: If benchmark fails and throw_errors is True
            CompetitionError: If no competition is loaded

        Examples:
            >>> # Benchmark random agent
            >>> results = client.benchmark()
            >>> print(f"Score: {results['score']}")
            >>>
            >>> # Benchmark PyTorch model with video
            >>> model = torch.load("model.pt")
            >>> results = client.benchmark(
            ...     model=model,
            ...     model_type="pytorch",
            ...     video_path="benchmark.mp4"
            ... )
        """
        self._console.print()

        results: BenchmarkResults = {
            "status": "error",
            "score": 0.0,
            "duration": 0,
            "logs": None,
            "error": None,
        }

        with self._console.status("Setting up benchmark...") as status:
            try:
                self._check_setup()
                self._check_environment_or_competition_loaded()
            except Exception as e:
                results["error"] = str(e)
                return results

            try:
                status.update("Setting up environment...")
                self._make_new_env(
                    render_mode="human" if video_path is None else "rgb_array"
                )

                model_manager = self._load_model(
                    model=model, model_type=model_type, status=status
                )

                self._console.print()

                if not self._env:
                    raise EnvironmentError("Environment not loaded")

                results = run_benchmark(
                    console=self._console,
                    env=self._env,
                    model=model_manager,
                    reset_vars=self._reset_vars,
                    video_path=video_path,
                    status=status,
                    show_progress=show_progress,
                    timeout=timeout
                )

                self._console.print()
                self._console.info(
                    f"\n[bold]Results:[/bold]\n{json.dumps(results, indent=2)}"
                )

                if results["status"] == "success":
                    self._console.success("Benchmark completed successfully")

            except Exception as e:
                results["status"] = "error"
                results["error"] = str(e)

            finally:
                if self._env is not None:
                    try:
                        self._env.close()
                    except Exception as e:
                        self._console.error(f"Unable to close environment: {e}")

            if throw_errors and results.get("status") == "error":
                raise BenchmarkError(results.get("error"))

            self._console.print()
            return results

    def server_benchmark(self, match_id: Optional[str] = None) -> BenchmarkResults:
        """
        Run benchmark in server mode and upload results.

        This method is primarily used by the SAI platform for evaluating
        submitted models. It:
        1. Downloads the model from the provided match
        2. Runs the benchmark
        3. Uploads results and video back to the platform

        Args:
            match_id (Optional[str]): ID of match to evaluate
                If None, tries to get ID from SAI_MATCH_ID environment variable

        Returns:
            BenchmarkResults: Results containing:
                - status: "success", "error", or "timeout"
                - score: Total reward achieved
                - duration: Time taken in seconds
                - error: Error message if failed

        Raises:
            MatchError: If match ID is not provided or invalid
            BenchmarkError: If benchmark fails

        Examples:
            >>> # Using environment variable
            >>> os.environ["SAI_MATCH_ID"] = "match-123456"
            >>> results = client.server_benchmark()
            >>>
            >>> # Using explicit match ID
            >>> results = client.server_benchmark("match-123456")
        """
        results: BenchmarkResults = {
            "status": "error",
            "score": 0.0,
            "duration": 0,
            "logs": None,
            "error": None,
        }

        try:
            self._check_setup()
        except Exception as e:
            results["error"] = str(e)
            return self._submit_match_results(results, match_id=match_id)

        match_id = match_id or os.getenv("SAI_MATCH_ID")
        if match_id is None:
            results["error"] = "Match ID required"
            return self._submit_match_results(results, match_id=match_id)

        video_path = "./benchmark.mp4"

        try:
            self._load_match(match_id)

            self._console.print()

            results = self.benchmark(
                model=self._match.get("model_url"),  # type: ignore
                model_type=self._match.get("model_type"),  # type: ignore
                video_path=video_path,
                show_progress=False,
                throw_errors=False,
                timeout=os.getenv("SAI_TIMEOUT", 120)
            )
        except Exception as e:
            results = {
                "status": "error",
                "score": None,
                "duration": None,
                "logs": None,
                "error": str(e),
            }

        return self._submit_match_results(
            results, match_id=match_id, video_path=video_path
        )

    # ---- Model Methods ----
    def submit_model(
        self,
        name: str,
        model: ModelType,
        model_type: Optional[ModelLibraryType] = None,
        action_function_id: Optional[str] = None,
        use_onnx: bool = False,
        skip_warning: bool = False,
    ):
        """
        Submits a model to the current competition.

        Args:
            name (str): Name for the submission
            model (ModelType): Model to submit. Can be one of:
                - PyTorch model (torch.nn.Module)
                - TensorFlow model (tf.keras.Model)
                - Stable-Baselines3 model (BaseAlgorithm)
                - ONNX model (OnnxAgentWrapper)
                - URL or file path (str)
            model_type (Optional[ModelLibraryType]): Framework used. One of:
                - "pytorch" - For PyTorch models
                - "tensorflow" - For TensorFlow/Keras models
                - "stable_baselines3" - For Stable-Baselines3 models
                - "onnx" - For ONNX models
            action_function_id (Optional[str]): ID of a previously submitted action function to use with this model
            use_onnx (bool): Whether to convert the model to ONNX format before submission
            skip_warning (bool): Skip validation warnings related to action function configuration

        Returns:
            dict: Submission information including:
                - id: Unique submission ID
                - name: Submission name
                - type: Model framework type
                - status: Current submission status
                - created_at: Timestamp of submission
                - updated_at: Timestamp of last update

        Raises:
            SubmissionError: If submission fails validation checks or upload fails
            CompetitionError: If no competition is currently loaded
            ValueError: If model type is invalid or incompatible with provided model

        Examples:
            >>> # Submit PyTorch model
            >>> model = torch.load("model.pt")
            >>> result = client.submit_model(
            ...     name="My Model v1",
            ...     model=model,
            ...     model_type="pytorch"
            ... )
            >>>
            >>> # Submit with action function and ONNX conversion
            >>> client.load_action_fn("./action.py")
            >>> action_fn = client.submit_action_fn()
            >>> result = client.submit_model(
            ...     name="My Model v2",
            ...     model=model,
            ...     model_type="pytorch",
            ...     action_function_id=action_fn["id"],
            ...     use_onnx=True
            ... )
        """
        self._check_setup()
        self._check_environment_or_competition_loaded()

        if not self._competition:
            raise CompetitionError(
                "No competition is loaded, please load a competition first using SAIClient(competition_id='')"
            )

        with self._console.status("Submitting model to the competition...") as status:
            if action_function_id is not None:
                if self._action_function.id is not None:
                    if action_function_id != self._action_function.id:
                        raise SubmissionError(
                            f"Provided action_function_id '{action_function_id}' does not match loaded action function id '{self._action_function.id}'"
                        )

                if self._action_function.is_local:
                    self._console.warning(
                        "Warning: action_function_id is provided but local action function hasn't been uploaded.\n"
                        "This may cause a mismatch between the action function already uploaded and the one used locally."
                    )

                    if not skip_warning:
                        raise SubmissionError(
                            "Action function must be uploaded before model submission. Set skip_warning=True to bypass this check."
                        )

            elif self._action_function.is_loaded:
                self._console.warning(
                    "Warning: Action function is loaded but not used in submission.\n"
                    "You must either:\n"
                    "1. Upload the action function and provide its ID via action_function_id parameter\n"
                    "2. Remove the action function using remove_action_function()"
                )

                if not skip_warning:
                    raise SubmissionError(
                        "Action function configuration must be resolved before submission. Set skip_warning=True to bypass this check."
                    )

            self._make_new_env(render_mode="rgb_array")

            model_manager = self._load_model(
                model=model,
                model_type=model_type,
                status=status,
            )

            self._console.print()

            self._print_submission_details(
                name, model_manager, use_onnx, action_function_id
            )
            if self._env:
                self._env.close()

            file_extension = {
                "stable_baselines3": ".zip",
                "pytorch": ".pt",
                "tensorflow": ".keras",
                "onnx": ".onnx",
            }.get("onnx" if use_onnx else model_manager.model_type, "")

            random_id = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=6)
            )
            os.makedirs(config.temp_path, exist_ok=True)
            temp_model_path = f"{config.temp_path}/{random_id}{file_extension}"
            model_manager.save_model(temp_model_path, use_onnx=use_onnx)

            status.update("Creating submission...")
            response = self._api.submission.create(
                {
                    "name": name,
                    "type": "onnx" if use_onnx else model_manager.model_type,
                    "competitionId": self._competition.get("id"),  # type: ignore
                    "actionFunctionId": action_function_id,
                }
            )

            submission = response.get("submission")  # type: ignore
            upload_url = response.get("upload_url")  # type: ignore

            if not submission or not upload_url:
                raise SubmissionError("Failed to create submission")

            status.update("Uploading model...")
            status.stop()

            with open(temp_model_path, "rb") as model_file:
                file_size = os.path.getsize(temp_model_path)
                with self._console.progress("Uploading model...") as p:
                    task = p.add_task("Uploading", total=file_size)
                    upload_response = requests.put(upload_url, data=model_file)
                    upload_response.raise_for_status()
                    p.update(task, completed=file_size)

            status.start()
            status.update("Running submission...")

            self._api.submission.run(submission.get("id"))

            if os.path.exists(temp_model_path):
                os.remove(temp_model_path)
            else:
                self._console.warning("Temporary model file not found.")

            self._console.success("Model submitted successfully.")

            return {
                "id": submission.get("id"),
                "name": submission.get("name"),
                "type": submission.get("type"),
                "status": submission.get("status"),
            }

    def save_model(
        self,
        name: str,
        model: ModelType,
        model_type: Optional[ModelLibraryType] = None,
        use_onnx: bool = False,
        output_path: str = "./",
    ):
        """
        Saves a model to disk in the appropriate format.

        Args:
            name (str): Name for the saved model file (without extension)
            model (ModelType): Model to save. Can be one of:
                - PyTorch model (torch.nn.Module)
                - TensorFlow model (tf.keras.Model)
                - Stable-Baselines3 model (BaseAlgorithm)
                - ONNX model (OnnxAgentWrapper)
                - URL or file path (str)
            model_type (Optional[ModelLibraryType]): Framework used. One of:
                - "pytorch" (.pt)
                - "tensorflow" (.keras)
                - "stable_baselines3" (.zip)
                - "onnx" (.onnx)
            use_onnx (bool): Whether to convert and save model in ONNX format (default: False)
            output_path (str): Directory to save the model file (default: "./")

        Returns:
            str: Full path to the saved model file

        Raises:
            ModelError: If model cannot be saved or converted to ONNX
            CompetitionError: If no competition is loaded

        Note:
            - File extension is automatically added based on model_type
            - If use_onnx=True, model will be converted and saved in ONNX format regardless of original type

        Examples:
            >>> # Save PyTorch model
            >>> model = torch.load("model.pt")
            >>> path = client.save_model(
            ...     name="my_model",
            ...     model=model,
            ...     model_type="pytorch",
            ...     output_path="./models"
            ... )  # Saves to ./models/my_model.pt
            >>> print(path)
            './models/my_model.pt'

            >>> # Save model in ONNX format
            >>> path = client.save_model(
            ...     name="my_model",
            ...     model=model,
            ...     model_type="pytorch",
            ...     use_onnx=True,
            ...     output_path="./models"
            ... )  # Saves to ./models/my_model.onnx
        """
        self._check_setup()
        self._check_environment_or_competition_loaded()

        self._console.print()

        with self._console.status("Setting up model...") as status:
            self._make_new_env(render_mode="rgb_array")

            model_manager = self._load_model(
                model=model,
                model_type=model_type,
                status=status,
            )

            file_extension = {
                "stable_baselines3": ".zip",
                "pytorch": ".pt",
                "tensorflow": ".keras",
                "onnx": ".onnx",
            }.get("onnx" if use_onnx else model_manager.model_type, "")

            save_path = f"{output_path}/{name}{file_extension}"
            os.makedirs(output_path, exist_ok=True)

            status.update("Saving model...")
            model_manager.save_model(save_path, use_onnx=use_onnx)

            self._console.success(f"Model saved to {save_path}")

        return save_path

    # ---- Package Methods ----
    def get_package(self, package: str) -> str:
        """
        Gets information about a specific package.

        Args:
            package (str): Name of the package to get information about

        Returns:
            PackageType: Package information including:
                - id: Package ID
                - name: Package name
                - description: Package description
                - version: Package version
            None: If package is not found

        Examples:
            >>> info = client.get_package("sai-pygame")
            >>> if info:
            ...     print(f"Latest version: {info['version']}")
        """
        self._check_setup()

        return self._api.package.get(package)  # type: ignore

    def update_package(self, package: str) -> None:
        """
        Updates a package to its latest version.

        Args:
            package (str): Name of the package to update

        Raises:
            PackageError: If the package cannot be updated

        Note: If package is an editable install, update will be skipped

        Examples:
            >>> client.update_package("sai-pygame")
        """
        self._check_setup()

        with self._console.status("Updating package...") as status:
            self._package_control.update(package, status)

    def install_package(self, package: str) -> None:
        """
        Installs a package if not already installed.

        Args:
            package (str): Name of the package to install

        Raises:
            PackageError: If the package cannot be installed

        Examples:
            >>> client.install_package("sai-pygame")
        """
        self._check_setup()

        with self._console.status("Installing package...") as status:
            self._package_control.update(package, status)

    def uninstall_package(self, package: str) -> None:
        """
        Uninstalls a package.

        Args:
            package (str): Name of the package to uninstall

        Raises:
            PackageError: If the package cannot be uninstalled

        Examples:
            >>> client.uninstall_package("sai-pygame")
        """
        self._check_setup()

        with self._console.status("Uninstalling package...") as status:
            self._package_control.uninstall(package, status)

    def list_packages(self, show_table: bool = True):
        """
        Lists all available packages and their installation status.

        Args:
            show_table (bool): Whether to display a formatted table of packages

        Returns:
            list[PackageType]: List of package information including:
                - id: Package ID
                - name: Package name
                - description: Package description
                - version: Latest version available

                Note: When show_table=True, displays additional information:
                    - Installed Version: Currently installed version
                    - Latest Version: Latest available version
                    - SAIStatus: Up to date/Update available/Not installed
                    - Install Type: Editable/Regular/Not installed

        Examples:
            >>> # Show table and get data
            >>> packages = client.list_packages()
            >>>
            >>> # Get data only
            >>> packages = client.list_packages(show_table=False)
            >>> for pkg in packages:
            ...     print(f"{pkg['name']}: {pkg['version']}")
        """
        self._check_setup()
        self._console.print()

        with self._console.status("Loading packages...") as status:
            packages = self._api.package.list()
            if not packages:
                self._console.warning("No packages found.")
                return []

            if show_table:
                status.update("Displaying packages...")
                table = self._console.table("Available Packages")

                table.add_column("Name", style="cyan")
                table.add_column("Installed Version", style="yellow")
                table.add_column("Latest Version", style="green")
                table.add_column("Status", style="magenta")
                table.add_column("Install Type", style="blue")

                for package in packages:
                    latest_version = package.get("version")
                    installed_version = self._package_control._get_package_version(
                        package["name"]
                    )

                    is_latest = latest_version == installed_version
                    is_installed = installed_version is not None
                    is_editable = self._package_control._is_editable_install(
                        package["name"]
                    )

                    status = (
                        "Up to date"
                        if is_latest
                        else "Update available"
                        if is_installed
                        else "Not installed"
                    )

                    install_type = (
                        "Editable"
                        if is_editable
                        else "Regular"
                        if is_installed
                        else "—"
                    )

                    table.add_row(
                        package.get("name"),
                        installed_version or "Not installed",
                        latest_version or "Unknown",
                        status,
                        install_type,
                    )

                self._console.print(table)
                self._console.print()

            return packages
