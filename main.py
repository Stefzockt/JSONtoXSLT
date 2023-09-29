import os
import shutil
import json
from mdBuilder.mdBuilder import buildData
from xsltBuilder.process_class import Process
from xsltBuilder.textbox_class import TextBox
import re
from xsltBuilder.checkbox_class import CheckBox

def main(input:str):
    #Read the input file
    with open(input,"r") as f:     
        data = f.read()
    jsondata = json.loads(data)

    #Delete the project directory if it exists
    shutil.rmtree("output/"+jsondata["project_details"]["project_namespace"],ignore_errors=True)

    try:
        os.mkdir("./output")
    except:
        pass

    #Create the project directory
    os.mkdir("./output/"+jsondata["project_details"]["project_namespace"])
    dir = "./output/"+jsondata["project_details"]["project_namespace"]

    #Create the project Readme file
    buildData(jsondata["project_details"])

    for dialog in jsondata["dialogs"]:
        #Iterate through each dialog
        params = {}
        params["filepath"] = dir + "/Process_"+dialog["dialog_id"]+".xsl"
        params["project_namespace"] = jsondata["project_details"]["project_namespace"]
        params["dialog_id"] = dialog["dialog_id"]
        for element, value in dialog["fields"].items():
            #Iterate through each field to be added
            match re.sub(r'^\d+_', '', element):
                case "textbox":
                    textbox = TextBox(id=str(value["position"]),edit=value["edit"],lines=value["lines"],orientation=value["orientation"])
                    params[element] = textbox
                case "checkbox":
                    checkbox = CheckBox(id=str(value["position"]),edit=value["edit"],lines=value["lines"],orientation=value["orientation"],value=value["default"])
                    params[element] = checkbox
        #Generate the XSLT file for the dialog
        P = Process.from_kwargs(**params)
        P.schema()
        P.add_all_fields()
        P.create_Stylesheet()

if __name__ == '__main__':
    main(input="./Construction.json")