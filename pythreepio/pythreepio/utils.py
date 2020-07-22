# importlib.resources is imported  to provide access to resources within packages

try:
    import importlib.resources as pkg_resources
    # for easier accessibility  importlib_resources can be refered to as pkg_resources

except ImportError:
    import importlib_resources as pkg_resources
    # except statement here represents importlib.resources in python3.6 and lower.   

import json
import static
# static is imported to Serve static or templated content via WSGI 



def get_mapped_commands() -> dict:
  """
     this function is used to read data from "mapped_commands_full.json" file and returns an  dictionary  based on JSON file
     '->' this represents data type of returning value of the function
  """
  json_txt = pkg_resources.read_text(static, "mapped_commands_full.json")
  return json.loads(json_txt)
