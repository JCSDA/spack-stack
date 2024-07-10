from collections import OrderedDict
import copy
import io
import logging
import os
import re
import shutil
import subprocess

import spack
import spack.config
import spack.environment as ev
import spack.util.spack_yaml as syaml
from spack.extensions.stack.stack_paths import common_path, site_path_tier1, site_path_tier2, stack_path, template_path

default_manifest_yaml = """\
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
# Includes are in order of highest precedence first.
# Site configs take precedence over the base packages.yaml.
spack:

  view: false

"""

# Hidden file in top-level spack-stack dir so this module can
# find relative config files. Assuming Spack is a submodule of
# spack-stack.
check_file = ".spackstack"


def get_git_revision_short_hash(path) -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=path)
        .decode("ascii")
        .strip()
    )


def stack_hash():
    return get_git_revision_short_hash(stack_path())


def spack_hash():
    return get_git_revision_short_hash(spack.paths.spack_root)


class StackEnv(object):
    """Represents a spack.yaml environment based on different
    configurations of sites and specs. Uses the Spack library
    to maintain an internal state that represents the yaml and
    can be written out with write(). The output is a pure
    Spack environment.
    """

    def __init__(self, **kwargs):
        """
        Construct properties directly from kwargs so they can
        be passed in through a dictionary (input file), or named
        args for command-line usage.
        """

        self.dir = kwargs.get("dir")
        self.template = kwargs.get("template", None)
        self.name = kwargs.get("name")

        self.includes = []

        # Config can be either name in apps dir or an absolute path to
        # to a spack.yaml to be used as a template. If None then empty
        # template is used.
        if not self.template:
            self.env_yaml = syaml.load_config(default_manifest_yaml)
            self.template_path = None
        else:
            if os.path.isabs(self.template):
                self.template_path = self.template
                template = self.template
            elif os.path.exists(os.path.join(template_path, self.template)):
                self.template_path = os.path.join(template_path, self.template)
                template = os.path.join(self.template_path, "spack.yaml")
            else:
                raise Exception('Template: "{}" does not exist'.format(self.template))

            with open(template, "r") as f:
                self.env_yaml = syaml.load_config(f)

        self.site = kwargs.get("site", None)
        if self.site == "none":
            self.site = None
        self.desc = kwargs.get("desc", None)
        self.compiler = kwargs.get("compiler", None)
        self.install_prefix = kwargs.get("install_prefix", None)
        self.upstreams = kwargs.get("upstreams", None)
        self.modifypkg = kwargs.get("modifypkg", None)

        if not self.name:
            # site = self.site if self.site else 'default'
            self.name = "{}.{}.{}".format(self.template, self.site, self.compiler)

    def env_dir(self):
        """env_dir is <dir>/<name>"""
        return os.path.join(self.dir, self.name)

    def get_lmod_or_tcl(self, site_configs_dir):
        site_modules_yaml_path = os.path.join(site_configs_dir, "modules.yaml")
        with open(site_modules_yaml_path, "r") as f:
            site_modules_yaml = syaml.load_config(f)
        lmod_or_tcl_list = site_modules_yaml["modules"]["default"]["enable"]
        assert lmod_or_tcl_list and (
            set(lmod_or_tcl_list) in ({"tcl"}, {"lmod"})
        ), """Set one and only one value ('lmod' or 'tcl') under 'modules:default:enable'
           in site modules.yaml, or use '--modulesys {tcl,lmod}'"""
        return lmod_or_tcl_list[0]

    def _copy_or_merge_includes(self, section, default_in_path, update_in_path, result_out_path):
        """Given two potential config files, merge the two (update the former with the latter)
        into an output config file. If only one of them exists, copy that file to the output.
        Do nothing if neither of them exists."""
        if os.path.exists(default_in_path) and \
                os.path.exists(update_in_path):
            logging.info(f"  Merging {default_in_path} and ...\n  ... {update_in_path} (the latter overwrites the former) ...\n  ... into {result_out_path}")
            with open(default_in_path, "r") as f:
                default_in_yaml = syaml.load_config(f)
            with open(update_in_path, "r") as f:
                update_in_yaml = syaml.load_config(f)
            #
            default_in_data = default_in_yaml[section]
            update_in_data = update_in_yaml[section]
            result_data = spack.config.merge_yaml(default_in_data, update_in_data)
            result_out_yaml = OrderedDict()
            result_out_yaml[section] = result_data
            # Write file, but sanitize the output.
            stream = io.StringIO()
            syaml.dump_config(result_out_yaml, stream)
            # - replace "- packages:" with "packages:" (similar for modules)
            sanitized_output = re.sub(r"- {}:".format(section), "{}:".format(section), stream.getvalue())
            # - get rid of annoying single quotes and !!omap
            sanitized_output = re.sub(r"!!omap", "", re.sub(r"'(\S+):':", "\g<1>::", sanitized_output))
            with open(result_out_path, "w") as f:
                f.write(sanitized_output)
        else:
            destination = result_out_path
            if os.path.exists(update_in_path):
                source = update_in_path
            elif os.path.exists(default_in_path):
                source = default_in_path
            logging.info(f"  Copying {source} ...\n  ... to {destination}")
            shutil.copy(source, destination)

    def _copy_common_includes(self):
        """Copy common directory into environment"""
        self.includes.append("common")
        env_common_dir = os.path.join(self.env_dir(), "common")
        logging.info(f"Copying common includes from {common_path} ...\n  ... to {env_common_dir}")
        shutil.copytree(
            common_path, env_common_dir, ignore=shutil.ignore_patterns("modules*.yaml", "packages*.yaml")
        )
        # Merge or copy common module config(s)
        lmod_or_tcl = self.get_lmod_or_tcl(self.site_configs_dir())
        modules_yaml_path = os.path.join(common_path, "modules.yaml")
        modules_yaml_modulesys_path = os.path.join(common_path, f"modules_{lmod_or_tcl}.yaml")
        destination = os.path.join(env_common_dir, "modules.yaml")
        self._copy_or_merge_includes("modules", modules_yaml_path, modules_yaml_modulesys_path, destination)
        # Merge or copy common package config(s)
        packages_yaml_path = os.path.join(common_path, "packages.yaml")
        packages_compiler_yaml_path = os.path.join(common_path, f"packages_{self.compiler}.yaml")
        destination = os.path.join(env_common_dir, "packages.yaml")
        self._copy_or_merge_includes("packages", packages_yaml_path, packages_compiler_yaml_path, destination)

    def site_configs_dir(self):
        site_configs_dir = None
        for site_path in [site_path_tier1, site_path_tier2]:
            site_configs_dir = os.path.join(site_path, self.site)
            if os.path.isdir(site_configs_dir):
                return site_configs_dir
        raise Exception(f"Site {self.site} not found in {[site_path_tier1, site_path_tier2]}")

    def _copy_site_includes(self):
        """Copy site directory into environment"""
        if not self.site:
            raise Exception("Site is not set")

        site_name = "site"
        self.includes.append(site_name)
        env_path = self.site_configs_dir()
        env_site_dir = os.path.join(self.env_dir(), site_name)
        logging.info(f"Copying site includes from {self.site_configs_dir()} ...\n  ... to {env_site_dir}")
        shutil.copytree(
            self.site_configs_dir(), env_site_dir, ignore=shutil.ignore_patterns("modules*.yaml", "packages*.yaml")
        )
        # Merge or copy site module config(s)
        lmod_or_tcl = self.get_lmod_or_tcl(self.site_configs_dir())
        modules_yaml_path = os.path.join(env_path, "modules.yaml")
        modules_yaml_modulesys_path = os.path.join(env_path, f"modules_{lmod_or_tcl}.yaml")
        destination = os.path.join(env_site_dir, "modules.yaml")
        self._copy_or_merge_includes("modules", modules_yaml_path, modules_yaml_modulesys_path, destination)
        # Merge or copy site package config(s)
        packages_yaml_path = os.path.join(env_path, "packages.yaml")
        packages_compiler_yaml_path = os.path.join(env_path, f"packages_{self.compiler}.yaml")
        destination = os.path.join(env_site_dir, "packages.yaml")
        self._copy_or_merge_includes("packages", packages_yaml_path, packages_compiler_yaml_path, destination)


    def write(self):
        """Write environment out to a spack.yaml in <env_dir>/<name>.
        Will create env_dir if it does not exist.
        """
        env_dir = self.env_dir()
        env_yaml = self.env_yaml

        if os.path.exists(env_dir):
            raise Exception("Environment '{}' already exists.".format(env_dir))

        os.makedirs(env_dir, exist_ok=True)

        # Copy site config first so that it takes precedence in env
        if self.site != "none":
            self._copy_site_includes()

        # Copy common include files
        self._copy_common_includes()

        # No way to add to env includes using pure Spack.
        env_yaml["spack"]["include"] = self.includes

        # Write out file with includes filled in.
        env_file = os.path.join(env_dir, "spack.yaml")
        with open(env_file, "w") as f:
            # Write header with hashes.
            header = "spack-stack hash: {}\nspack hash: {}"
            env_yaml.yaml_set_start_comment(header.format(stack_hash(), spack_hash()))
            syaml.dump_config(env_yaml, stream=f)

        # Activate environment
        env = ev.Environment(manifest_dir=env_dir)
        ev.activate(env)
        env_scope = env.scope_name

        # Save original data in spack.yaml because it has higest precedence.
        # spack.config.add will overwrite as it goes.
        # Precedence order (high to low) is original spack.yaml,
        # then common configs, then site configs.
        original_sections = {}
        for key in spack.config.SECTION_SCHEMAS.keys():
            section = spack.config.get(key, scope=env_scope)
            if section:
                original_sections[key] = copy.deepcopy(section)

        # Commonly used config settings
        compiler = f"packages:all:require:['%{self.compiler}']"
        spack.config.add(compiler, scope=env_scope)
        # Also update compiler definitions if matrices are used
        # DH I am too stupid to do this the "spack way" ...
        definitions = spack.config.get("definitions", scope=env_scope)
        if definitions:
            target_compiler = f"%{self.compiler}"
            for i in range(len(definitions)):
                if "compilers" in definitions[i]:
                    j = len(definitions[i]["compilers"])-1
                    while j>=0:
                        if not definitions[i]["compilers"][j] == target_compiler:
                            definitions[i]["compilers"].pop(j)
                        j -= 1
            spack.config.set("definitions", definitions, scope=env_scope)

        if self.install_prefix:
            # Modules can go in <prefix>/modulefiles by default
            prefix = "config:install_tree:root:{}".format(self.install_prefix)
            spack.config.add(prefix, scope=env_scope)
            module_prefix = os.path.join(self.install_prefix, "modulefiles")
            lmod_prefix = "modules:default:roots:lmod:{}".format(module_prefix)
            tcl_prefix = "modules:default:roots:tcl:{}".format(module_prefix)
            spack.config.add(lmod_prefix, scope=env_scope)
            spack.config.add(tcl_prefix, scope=env_scope)
        if self.upstreams:
            for upstream_path in self.upstreams:
                upstream_path = upstream_path[0]
                # spack doesn't handle "~/" correctly, this fixes it:
                upstream_path = os.path.expanduser(upstream_path)
                if not os.path.basename(os.path.normpath(upstream_path)) == "install":
                    logging.warning(
                        "WARNING: Upstream path '%s' is not an 'install' directory!"
                        % upstream_path
                    )
                if not os.path.isdir(upstream_path):
                    logging.warning(
                        "WARNING: Upstream path '%s' does not appear to exist!" % upstream_path
                    )
                re_pattern = ".+/(?P<spack_stack_ver>spack-stack-[^/]+)/envs/(?P<env_name>[^/]+)"
                path_parts = re.match(re_pattern, upstream_path)
                if path_parts:
                    name = path_parts["spack_stack_ver"] + "-" + path_parts["env_name"]
                else:
                    name = os.path.basename(upstream_path)
                upstream = "upstreams:%s:install_tree:'%s'" % (name, upstream_path)
                logging.info("Adding upstream path '%s'" % upstream_path)
                spack.config.add(upstream, scope=env_scope)
        if self.modifypkg:
            logging.info("Creating custom repo with packages %s" % ", ".join(self.modifypkg))
            env_repo_path = os.path.join(env_dir, "envrepo")
            env_pkgs_path = os.path.join(env_repo_path, "packages")
            os.makedirs(env_pkgs_path, exist_ok=False)
            with open(os.path.join(env_repo_path, "repo.yaml"), "w") as f:
                f.write("repo:\n  namespace: envrepo")
            repo_paths = spack.config.get("repos")
            repo_paths = [p.replace("$spack/", spack.paths.spack_root + "/") for p in repo_paths]
            for pkg_name in self.modifypkg:
                pkg_found = False
                for repo_path in repo_paths:
                    pkg_path = os.path.join(repo_path, "packages", pkg_name)
                    if os.path.exists(pkg_path):
                        shutil.copytree(
                            pkg_path,
                            os.path.join(env_pkgs_path, pkg_name),
                            ignore=shutil.ignore_patterns("__pycache__"),
                        )
                        pkg_found = True
                        # Use the first repo where the package exists:
                        break
                if not pkg_found:
                    logging.warning(f"WARNING: package '{pkg_name}' could not be found")
            logging.info("Adding custom repo 'envrepo' to env config")
            repo_cfg = "repos:[$env/envrepo]"
            spack.config.add(repo_cfg, scope=env_scope)

        # Merge the original spack.yaml template back in
        # so it has the highest precedence
        for section in spack.config.SECTION_SCHEMAS.keys():
            original = original_sections.get(section, {})
            existing = spack.config.get(section, scope=env_scope)
            new = spack.config.merge_yaml(existing, original)
            if existing and section in existing:
                spack.config.set(section, new[section], env_scope)

        with env.write_transaction():
            env.write()

        ev.deactivate()

        logging.info("Successfully wrote environment at {}".format(env_file))

    def check_umask(self):
        """Check if the user's umask will create environments that are not readable
        by group or others and if so, issue a warning.
        """

        # os.mask requires a new value for the mask and returns the old mask.
        # The new value doesn't matter, since it is forgotten when the Python
        # script terminates. See https://www.geeksforgeeks.org/python-os-umask-method/
        newmask = 18  # decimal, same as 0o022 in octal
        oldmask = os.umask(newmask)
        if oldmask == 18:
            # 18 = 0o022
            logging.info("\nChecked user umask and found no issues (0022)\n")
        elif oldmask == 23:
            # 23 = 0o027
            logging.warning(
                "\nWARNING! User umask only allows owner and group to read the env (0027)\n"
            )
        else:
            logging.warning(
                "\nWARNING! User umask is neither 0022 nor 0027, check before proceeding\n"
            )
