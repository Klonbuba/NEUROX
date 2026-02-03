import os
import importlib.util
import inspect
from core.plugin_interface import NeuroxPlugin

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def discover_plugins(self):
        """
        Scans the plugin directory for python files and loads them.
        """
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                self.load_plugin(filename)

    def load_plugin(self, filename):
        """
        Dynamically loads a plugin from a file.
        """
        plugin_path = os.path.join(self.plugin_dir, filename)
        module_name = filename[:-3] # Remove .py
        
        try:
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find the class that inherits from NeuroxPlugin
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, NeuroxPlugin) and obj is not NeuroxPlugin:
                    plugin_instance = obj()
                    plugin_instance.on_load()
                    self.plugins.append(plugin_instance)
                    print(f"Loaded plugin: {plugin_instance.name}")
                    
        except Exception as e:
            print(f"Error loading plugin {filename}: {e}")

    def execute_all(self, context):
        """
        Executes all loaded plugins sequentially (sorted by order).
        """
        # Sort plugins by order
        sorted_plugins = sorted(self.plugins, key=lambda p: p.order)
        
        print("--- Execution Order ---")
        for p in sorted_plugins:
            print(f"{p.name} (Order: {p.order})")
        print("-----------------------")
        
        for plugin in sorted_plugins:
            try:
                # In a real event system, we would filter by hook. 
                # For now, we just run execute() on everyone.
                print(f"Running: {plugin.name}")
                result = plugin.execute(context)
                if result:
                    print(f"  -> Updates: {list(result.keys())}")
                    context.update(result)
            except Exception as e:
                print(f"Error executing plugin {plugin.name}: {e}")
        return context
