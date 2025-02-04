def dynamic_import(module_name: str):
    components = module_name.split(".")
    module = __import__(components[0])
    for component in components[1:]:
        module = getattr(module, component)
    return module
