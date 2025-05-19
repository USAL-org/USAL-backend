import os
import re
from typing import Any

from yaml import ScalarNode, UnsafeLoader, load

from usal.core.container import container

is_prod = os.getenv("ENV", "dev") == "prod"


def load_config() -> None:
    yaml_paths: list[str] = [
        "configs/common.yaml",
        f"configs/{os.getenv('ENV') or 'local'}.yaml",
    ]
    for yaml_path in yaml_paths:
        config = parse_config(yaml_path)
        container.params.update(config)


def parse_config(
    path: str,
    tag: str = "!ENV",
    raise_if_na: bool = False,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    default_sep = ":"
    default_value = "N/A"
    default_sep_pattern = r"(" + default_sep + "[^}]+)?" if default_sep else ""
    pattern = re.compile(
        r".*?\$\{([^}{" + default_sep + r"]+)" + default_sep_pattern + r"\}.*?"
    )
    loader = UnsafeLoader

    loader.add_implicit_resolver(tag, pattern, first=[tag])  # type: ignore

    type_tag = "tag:yaml.org,2002:"
    type_tag_pattern = re.compile(rf"({type_tag}\w+\s)")

    def constructor_env_variables(loader: UnsafeLoader, node: ScalarNode) -> str:
        value = str(loader.construct_scalar(node))
        match = pattern.findall(value)
        dt = "".join(type_tag_pattern.findall(value)) or ""
        value = value.replace(dt, "")
        if match:
            full_value = value
            for g in match:
                curr_default_value = default_value
                env_var_name: Any = g
                env_var_name_with_default = g
                if default_sep and isinstance(g, tuple) and len(g) > 1:  # type: ignore
                    env_var_name = g[0]
                    env_var_name_with_default = "".join(g)  # type: ignore
                    found = False
                    for each in g:  # type: ignore
                        if default_sep in each:
                            _, curr_default_value = each.split(default_sep, 1)  # type: ignore
                            found = True
                            break
                    if not found and raise_if_na:
                        raise ValueError(
                            f"Could not find default value for {env_var_name}"
                        )
                full_value = full_value.replace(
                    f"${{{env_var_name_with_default}}}",
                    os.environ.get(env_var_name, curr_default_value),  # type: ignore
                )
                if dt:
                    node.value = full_value
                    node.tag = dt.strip()
                    return loader.yaml_constructors[node.tag](loader, node)
            return full_value

        return value

    loader.add_constructor(tag, constructor_env_variables)

    with open(path, encoding=encoding) as conf_data:
        return load(conf_data, Loader=loader)
