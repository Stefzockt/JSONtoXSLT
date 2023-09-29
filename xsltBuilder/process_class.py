from lxml import etree as ET
from dataclasses import dataclass
from inspect import signature
import re



@dataclass
class Process:
    """
    Initializes a Process object where all Fields can be added to.
    """
    filepath: str
    project_namespace:str
    dialog_id: str
    xslt_template = None
    SCHEMA_NAMESPACE = "http://www.w3.org/1999/XSL/Transform"
    XSL = "{%s}" % SCHEMA_NAMESPACE
    
    def schema(self):

        self.xslt_template = ET.Element(self.XSL+"stylesheet",
                                        version="1.0")
        
        include_bis = ET.Element(self.XSL+"import",href="INCLUDE_BIS.xsl")
        include_bis_mde = ET.Element(self.XSL+"import",href="INCLUDE_BIS_MDE.xsl")
        include_bis_project = ET.Element(self.XSL+"import",href=f"INCLUDE_BIS_{self.project_namespace}.xsl")
        output = ET.Element(self.XSL+"output",method="xml")
        mde_prev = ET.Element(self.XSL+"variable",name="MDE_PREV",select="MPX01P00090")
        mde_curr = ET.Element(self.XSL+"variable",name="MDE_CURR",select=str(self.dialog_id))
        mde_next = ET.Element(self.XSL+"variable",name="MDE_NEXT",select="MPX01P00020")
        mde_list = ET.Element(self.XSL+"variable",name="MDE_LIST",select="00")
        mde_sele = ET.Element(self.XSL+"variable",name="MDE_SELE",select="00")
        mde_menu = ET.Element(self.XSL+"variable",name="MDE_MENU",select="00")
        stylesheet = ET.Element(self.XSL+"Stylesheet",name="Stylesheet",select="Process_"+str(self.dialog_id)+".xsl")
        textpackage = ET.Element(self.XSL+"variable",name="TextPackage",select="00")
        match = ET.Element(self.XSL+"template",match="/")
        match_call =  ET.Element(self.XSL+"call-template",name="DebugRecords")
        match_process = ET.Element("Process")
        match_process_inti = ET.Element(self.XSL+"call-template",name="Init")
        match_process_process = ET.Element(self.XSL+"call-template",name="Process")
        template_init = ET.Element(self.XSL+"template",name="Init")
        template_process = ET.Element(self.XSL+"template",name="Process")
        template_process_dialog = ET.Element("Dialog")

        self.xslt_template.append(include_bis)
        self.xslt_template.append(include_bis_mde)
        self.xslt_template.append(include_bis_project)
        self.xslt_template.append(output)
        self.xslt_template.append(mde_prev)      
        self.xslt_template.append(mde_curr)      
        self.xslt_template.append(mde_next)      
        self.xslt_template.append(mde_list)      
        self.xslt_template.append(mde_sele)      
        self.xslt_template.append(mde_menu)
        self.xslt_template.append(stylesheet)      
        self.xslt_template.append(textpackage)


        match_process.append(match_process_inti)
        match_process.append(match_process_process)

        match.append(match_call)
        match.append(match_process)

        self.xslt_template.append(match)

        self.xslt_template.append(template_init)
        self.xslt_template.append(template_process)
        template_process.append(template_process_dialog)

        
    @classmethod
    def from_kwargs(cls, **kwargs):
        """
        With this method its possible to add infinite Attributes to the Class
        """
        # fetch the constructor's signature
        cls_fields = {field for field in signature(cls).parameters}

        # split the kwargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                native_args[name] = val
            else:
                new_args[name] = val

        # use the native ones to create the class ...
        ret = cls(**native_args)

        # ... and add the new ones by hand
        for new_name, new_val in new_args.items():
            setattr(ret, new_name, new_val)
        return ret

    def add_all_fields(self):
        """
        This Loop will go through every attribute and adds them to the Stylesheet in their corresponding order.  
        """
        for attribute,value in vars(self).items():
            match re.sub(r'^\d+_',"",attribute):
                case "textbox":
                    self.create_text_variable(id=value.id)
                    self.create_field(value.getElement())
                case "checkbox":
                    self.create_text_variable(id=value.id)
                    self.create_field(value.getElement())

    def create_field(self,field: ET.Element):
        """
        This Function will create a new Field, beneath an existing Field.\n
        The field Attribute is an Field Element form LXML!
        """
        root = self.xslt_template
        dialog_element = root.find(".//Dialog")
        if dialog_element is not None:
            field_element = root.find(".//Field")
            if field_element is not None:
                dialog_element.addnext(field)
            else:
                dialog_element.append(field)
        else:
            print("Not a valid XSLT Template")
    

    def create_text_variable(self,id:str):
        variable = ET.Element(self.XSL+"variable",name=id)
        call_template = ET.Element(self.XSL+"call-template",name="get-text")
        param = ET.Element(self.XSL+"with-param",name="id",select=f"concat($MDE_CURR, '/{id}')")
       
        call_template.append(param)

        variable.append(call_template)

        # Find the last variable element
        last_variable = self.xslt_template.xpath('//xsl:variable[last()]', namespaces={'xsl': 'http://www.w3.org/1999/XSL/Transform'})[0]

        last_variable.addnext(variable)


    def create_Stylesheet(self):
        try:
            tree = ET.ElementTree(self.xslt_template)
            tree.write(self.filepath, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        except IOError:
            print("Error: Unable to create XSLT file.")
