#importlib.resources is imported  to provide access to resources within packages
try:
    import importlib.resources as pkg_resources
#for easier accessibility  importlib_resources can be refered to as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources
import json
import static
#static is imported to Serve static or templated content via WSGI 

#this function is used to read data from "mapped_commands_full.json" file and returns an  dictionary  based on JSON file
#'->' this represents data type of returning value of the function
def get_mapped_commands() -> dict:
    json_txt = pkg_resources.read_text(static, "mapped_commands_full.json")
    return json.loads(json_txt)
