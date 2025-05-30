
import json
import nodes
import os
import folder_paths


def create_node_class_mappings():
    # This function creates a dictionary of node class mappings
    # The function excludes comfy_api_nodes and comfy_extras from the mapping
    # The reason the dictionary is reversed is that the first node added 
    # using app.ui.settings.addSetting in node-disabler-settings.js will be the last one in the list
    # This feels dirty...
    reversed_dict = {key: nodes.NODE_CLASS_MAPPINGS[key] for key in reversed(nodes.NODE_CLASS_MAPPINGS)}
    all_nodes = {}
    counter = 0
    for x in reversed_dict:
        module = getattr(reversed_dict[x], "RELATIVE_PYTHON_MODULE", "nodes")
        # print(f"Module: {module}")
        # if module == "nodes" or module == "comfy_api_nodes" or module == "comfy_extras":
        if module.startswith("custom_nodes."):
            module = module.replace("custom_nodes.", "")
        elif module.startswith("comfy_api_nodes."):
            module = "Comfy API"
        elif module.startswith("comfy_extras."):
            module = "Comfy Extras"
        elif module == "nodes":
            module = "Comfy Core"

        # if module.startswith("comfy_api_nodes.") or module.startswith("comfy_extras."):
        #     continue
        
        if module in all_nodes:
            all_nodes[module].append(x)
        else:
            all_nodes[module] = [x]

        counter += 1
        
    for module in all_nodes:
        all_nodes[module] = sorted(all_nodes[module], reverse=True)

    return all_nodes, counter

def save_node_class_mappings(all_nodes):
    # This function saves the node class mappings to a JSON file
    # in the default user directory.
    default_user_path = folder_paths.get_user_directory() + '\\default'
    with open(os.path.join(default_user_path, "node_class_mappings.json"), 'w') as f:
        json.dump(all_nodes, f, default=str)
    return default_user_path
    
def disable_nodes():
    # This function disables nodes based on the settings in the comfy.settings.json file
    default_user_path = folder_paths.get_user_directory() + '\\default'
    with open(os.path.join(default_user_path, "comfy.settings.json"), 'r') as f:
        settings = json.load(f)
    
    for setting in settings:
        if setting.startswith("node-disabler"):
            # print(setting)
            # print(settings[setting])
            if settings[setting] == False:
                nodeName = setting.split(".")[2]
                nodes.NODE_CLASS_MAPPINGS.pop(nodeName)
                print(f"Removed {nodeName} from NODE_CLASS_MAPPINGS")
    
    return ""

def init():
    print("---------------------\033[33m Loading ComfyUI-Node-Disabler \033[0m---------------------")
    all_nodes, counter = create_node_class_mappings()
    print(f"Found {counter} node classes in ComfyUI.")
    path = save_node_class_mappings(all_nodes)
    print(f"Node class mappings saved to {path}\\node_class_mappings.json")
    disable_nodes()
    print("----------------------------------------------------------------------------------------")



init()
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
