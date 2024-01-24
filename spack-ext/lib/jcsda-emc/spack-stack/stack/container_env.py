import shutil
import os

import spack
import spack.util.spack_yaml as syaml
from spack.extensions.stack.stack_paths import common_path, container_path, container_specs_path


class StackContainer:
    """Represents an abstract container. It takes in a
    container template (spack.yaml), the specs from an app, and
    its packages.yaml versions then writes out a merged file.
    """

    def __init__(self, container, dir, specs) -> None:
        self.container = container
        self.specs = specs

        test_path = os.path.join(container_path, self.container + ".yaml")
        if os.path.exists(test_path):
            self.container_path = test_path
        elif os.path.isabs(container):
            self.container_path = self.container
        else:
            raise Exception("Invalid container {}".format(self.container))

        test_path = os.path.join(container_specs_path, self.specs + ".yaml")
        if os.path.exists(test_path):
            self.specs_path = test_path
        elif os.path.isabs(specs):
            self.specs_path = self.specs
        else:
            raise Exception("Invalid specs list {}".format(self.specs))

        self.name = self.container
        self.dir = dir
        self.env_dir = os.path.join(self.dir, self.name)
        self.base_packages = os.path.join(common_path, "packages.yaml")

    def write(self):
        """Merge base packages and app's spack.yaml into
        output container file.
        """

        with open(self.container_path, "r") as f:
            filedata = f.read()
            filedata = filedata.replace("::", ":")
            container_yaml = syaml.load_config(filedata)

        with open(self.specs_path, "r") as f:
            specs_yaml = syaml.load_config(f)

        with open(self.base_packages, "r") as f:
            filedata = f.read()
            filedata = filedata.replace("::", ":")
            packages_yaml = syaml.load_config(filedata)

        if "packages" not in container_yaml["spack"]:
            container_yaml["spack"]["packages"] = {}

        container_yaml["spack"]["packages"] = spack.config.merge_yaml(
            container_yaml["spack"]["packages"], packages_yaml["packages"]
        )

        if "specs" not in container_yaml["spack"]:
            container_yaml["spack"]["specs"] = {}

        container_yaml["spack"]["specs"] = spack.config.merge_yaml(
            container_yaml["spack"]["specs"], specs_yaml["specs"]
        )

        container_yaml["spack"]["container"]["labels"]["app"] = self.specs

        os.makedirs(self.env_dir, exist_ok=True)

        # Replace the placeholder SPACK_STACK_HASH with the hash stored in the env variable
        if "spack_extension" in \
                container_yaml["spack"]["container"]["extra_instructions"].keys():
            old = container_yaml["spack"]["container"]["extra_instructions"]["spack_extension"]
            try:
                new = old.replace("SPACK_STACK_HASH", os.environ['SPACK_STACK_HASH'])
            except KeyError:
                raise Exception("Environment variable 'SPACK_STACK_HASH' not defined")
            container_yaml["spack"]["container"]["extra_instructions"]["spack_extension"] = new

        with open(os.path.join(self.env_dir, "spack.yaml"), "w") as f:
            syaml.dump_config(container_yaml, stream=f)

        # Copy the spack-stack extension into the spack/docker env directory
        os.chdir(self.env_dir)
        shutil.copytree(os.path.join(os.environ['SPACK_STACK_DIR'], "spack-ext"), \
            "spack-ext-" + os.environ['SPACK_STACK_HASH'])
