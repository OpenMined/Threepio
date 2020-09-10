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
        Fetches data from a "mapped_commands_full.json" file 
        you can have a look at "mapped_commands_full.json" file by going through following link
        https://raw.githubusercontent.com/OpenMined/Threepio/dev/pythreepio/static/mapped_commands_full.json
        Returns:
            A dict mapping keys to the corresponding data fetched from json file.  
          If a key from the keys argument is missing from the dictionary,
          then that key represing dat didn't existed.
    """
    json_txt = pkg_resources.read_text(static, "mapped_commands_full.json")
    return json.loads(json_txt)
