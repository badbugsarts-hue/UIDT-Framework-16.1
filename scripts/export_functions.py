import inspect
import importlib
import pkgutil

def export_functions_to_json_list(package_name):
    package = importlib.import_module(package_name)
    functions_list = []

    for _, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if not ispkg:
            mod = importlib.import_module(modname)
            for name, func in inspect.getmembers(mod, inspect.isfunction):
                functions_list.append({
                    "name": name,
                    "module": modname,
                    "description": func.__doc__ or "",
                    "parameters": list(inspect.signature(func).parameters.keys()),
                    "returns": str(inspect.signature(func).return_annotation),
                    "codeSnippet": inspect.getsource(func)
                })
    return functions_list
