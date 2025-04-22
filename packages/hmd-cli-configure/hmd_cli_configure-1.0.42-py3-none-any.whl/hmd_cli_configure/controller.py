import os
import socket
from pathlib import Path

from cement import Controller, ex, minimal_logger
from importlib.metadata import version
from hmd_cli_tools.hmd_cli_tools import load_hmd_env, set_hmd_env
from hmd_cli_tools.prompt_tools import prompt_for_values
from dotenv import dotenv_values

logger = minimal_logger("hmd-cli-configure")

VERSION_BANNER = """
hmd configure version: {}
"""

hostname = socket.gethostname()

hmd_home_vars = {
    "HMD_HOME": {
        "prompt": "Select a folder to store NeuronSphere data and configuration:",
        "default": str(Path(os.path.expanduser("~")) / "hmd"),
    },
    "HMD_REPO_HOME": {
        "prompt": "Enter folder that will contain NeuronSphere repositories:",
        "default": "$HMD_HOME/projects",
    },
    "HMD_GH_ORG_NAME": {
        "prompt": "Enter your GitHub Org Name, GitHub username, or see docs:",
        "required": True,
    },
}
default_env_vars = {
    "HMD_AUTHOR_NAME": {"prompt": "Enter your name:"},
    "HMD_AUTHOR_EMAIL": {"prompt": "Enter your email:"},
    "HMD_BUILD_STRICT_MODE": {"hidden": True, "default": "false"},
    "HMD_HOSTNAME": {
        "hidden": True,
        "default": hostname if hostname is not None else "local-ns",
    },
}


class LocalController(Controller):
    class Meta:
        label = "configure"
        alias = "config"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Configures a local environment to use HMD CLI tools. Run 'hmd configure' to setup local environment."

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the configure command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd_cli_configure")),
                },
            ),
        )

    def _default(self):
        hmd_home = os.environ.get("HMD_HOME")
        questions = default_env_vars
        if hmd_home is None:
            logger.warning("Could not find environment variable HMD_HOME.")
            questions = {**hmd_home_vars, **default_env_vars}
        else:
            load_hmd_env()

        results = prompt_for_values(questions)
        for key, value in results.items():
            if key == "HMD_HOME":
                if value is not None:
                    hmd_home = os.path.expandvars(os.path.expanduser(value))
                    os.environ["HMD_HOME"] = hmd_home
                    set_hmd_env("HMD_HOME", hmd_home)
                    load_hmd_env(override=False)
                    continue
            if key == "HMD_REPO_HOME":
                if value is not None:
                    hmd_repo_home = os.path.expandvars(os.path.expanduser(value))
                    os.environ["HMD_REPO_HOME"] = hmd_repo_home
                    set_hmd_env("HMD_REPO_HOME", hmd_repo_home)
                    if not os.path.exists(hmd_repo_home):
                        os.makedirs(hmd_repo_home)
                    continue

            if key == "HMD_GH_ORG_NAME":
                if not value:
                    raise Exception(
                        "Must provide GitHub Org name, or username. See docs for more info."
                    )

                set_hmd_env("HMD_NPM_SCOPE", value)

            if value is not None:
                set_hmd_env(key, value)

        for h in self.app._meta.handlers:
            if h.Meta.label == self.Meta.label:
                continue
            setattr(h, "app", self.app)
            configure_cmd = getattr(h, "configure", None)
            if configure_cmd:
                configure_cmd(h)

        print(
            f"""
Remember to set HMD_HOME in this terminal session:

export HMD_HOME={os.environ['HMD_HOME']}
"""
        )

    @ex(
        help="Set environment variable in $HMD_HOME/.config/hmd.env",
        arguments=[
            (["key"], {"action": "store"}),
            (["value"], {"action": "store"}),
        ],
    )
    def set_env(self):
        key = self.app.pargs.key
        value = self.app.pargs.value

        set_hmd_env(key, value)

    @ex(
        help="Get environment variable in $HMD_HOME/.config/hmd.env",
        arguments=[
            (["key"], {"action": "store"}),
        ],
    )
    def get_env(self):
        key = self.app.pargs.key

        load_hmd_env(override=False)

        print(f"{key}={os.environ.get(key)}")

    @ex(
        help="list current environment settings from $HMD_HOME/.config/hmd.env and current session",
    )
    def list_env(self):
        env_path = Path(os.environ["HMD_HOME"]) / ".config" / "hmd.env"
        hmd_env = dotenv_values(env_path)

        output = f"""
Loaded configuration from:
{env_path}

Values found in hmd.env file:
        """

        for key, value in hmd_env.items():
            output += f"""
{key}={value}"""

        overrides = {
            key: os.environ.get(key)
            for key, value in hmd_env.items()
            if os.environ.get(key) is not None and os.environ.get(key) != value
        }

        output += """

Variables overridden in current session:
        """
        for key, value in overrides.items():
            output += f"""
{key}={value}"""

        print(output)
