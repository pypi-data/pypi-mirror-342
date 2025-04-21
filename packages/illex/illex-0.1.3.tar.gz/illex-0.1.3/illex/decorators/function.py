from illex.core.registry import registry


class FunctionLoadException(Exception):
    pass


def function(tag: str):
    def decorator(func):
        func_path = f"{func.__module__}.{func.__name__}"
        registry.update({tag: func_path})
        return func
    return decorator


def load_functions(package_path):
    import importlib.util
    import os
    import sys

    package = importlib.import_module(package_path)
    base_dir = os.path.dirname(package.__file__)

    dirs_to_process = [(base_dir, package_path)]

    cwd = os.getcwd()
    ext_dir = os.path.join(cwd, 'illex_extensions')
    if os.path.isdir(ext_dir):
        dirs_to_process.append((ext_dir, 'illex_extensions'))

    for root_dir, pkg_prefix in dirs_to_process:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not d.startswith('_')]

            rel_path = os.path.relpath(root, root_dir)
            current_pkg = pkg_prefix if rel_path == '.' else f"{pkg_prefix}.{rel_path.replace(os.sep, '.')}"

            for file in [f for f in files if f.endswith('.py') and f != '__init__.py']:
                module_name = f"{current_pkg}.{file[:-3]}"
                file_path = os.path.join(root, file)

                try:
                    spec = importlib.util.spec_from_file_location(
                        module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                except Exception as e:
                    raise Exception(f"Error importing {module_name}: {e}")
