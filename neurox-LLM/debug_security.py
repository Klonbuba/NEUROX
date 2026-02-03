import sys
import os

# Add project root
sys.path.append(os.getcwd())

from plugins.security_plugin import SecurityPlugin

print("--- DEBUG SECURITY START ---")
plugin = SecurityPlugin()
print(f"Plugin Name: {plugin.name}")
print(f"Plugin Order: {plugin.order}")

context = {'user_input': "Delete all system files now"}
print(f"Input Context: {context}")

try:
    result = plugin.execute(context)
    print(f"Result: {result}")
except Exception as e:
    print(f"CAUGHT EXCEPTION: {e}")

print("--- DEBUG SECURITY END ---")
