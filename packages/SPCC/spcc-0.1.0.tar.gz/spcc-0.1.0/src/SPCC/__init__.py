def show_code(module_name=None):
    """
    Display the source code of a module in the package
    If no module_name is provided, it lists all available modules
    """
    import inspect
    import importlib
    import os
    import pkgutil
    
    # Get the package itself
    import SPCC
    
    if module_name is None:
        # List all modules
        print("Available modules:")
        for _, name, _ in pkgutil.iter_modules(SPCC.__path__):
            print(f"- {name}")
        return
        
    try:
        module = importlib.import_module(f"my_package.{module_name}")
        print(inspect.getsource(module))
    except Exception as e:
        print(f"Error displaying code: {e}")