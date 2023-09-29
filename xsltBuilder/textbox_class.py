from dataclasses import dataclass
from lxml import etree as ET


@dataclass
class TextBox():
    """
    Initializes a TextBox object
    """
    id: str
    edit: bool = True
    lines: int = 1
    orientation: str = "horizontal"

    #Field Attributes these are currently not supported
    
    field_alignment: str = "{$Style/PDFAH}"
    field_color: str = "{$Style/PDFFC}"
    field_bgColor: str = "{$Style/PDFBC}"
    field_italic: str = "{$Style/PDFSI}"
    field_bold: str = "{$Style/PDFSB}"
    field_fontSize: str = "{$Style/PDFSZ}"

    label_alignment: str = "{$Style/PDNAH}"
    label_color: str = "{$Style/PDNFC}"
    label_bgColor: str = "{$Style/PDNBC}"
    label_italic: str = "{$Style/PDNSI}"
    label_bold: str = "{$Style/PDNSB}"
    label_fontSize: str = "{$Style/PDNSZ}"

    swingComponent: str = "Text"

    def getElement(self) -> ET.Element:
        """
        Returns the XML Element for the TextBox 
        """

        field_attributes = {
            "Alignment": self.field_alignment,
            "Color": self.field_color,
            "BgColor": self.field_bgColor,
            "Italic": self.field_italic,
            "Bold": self.field_bold,
            "FontSize": self.field_fontSize,
            "Layout": self.orientation
        }

        label_attributes = {
            "Alignment": self.label_alignment,
            "Color": self.label_color,
            "BgColor": self.label_bgColor,
            "Italic": self.label_italic,
            "Bold": self.label_bold,
            "FontSize": self.label_fontSize,
        }

        field = ET.Element("Feld", attrib=field_attributes)
        label = ET.SubElement(field,"Name", attrib=label_attributes)
        id = ET.SubElement(field,"Id")
        tooltip = ET.SubElement(field,"Tooltip")
        edit = ET.SubElement(field,"Edit")
        value = ET.SubElement(field,"Wert")
        component = ET.SubElement(field,"SwingComponent")
        lines = ET.SubElement(field,"Lines")

        label.text = self.id+"_label"
        id.text = self.id
        tooltip.text = self.id+"_tooltip"
        edit.text = str(self.edit)
        value.text = self.id+"_value"
        component.text = self.swingComponent
        lines.text = str(self.lines)

        return field

    def getString(self):
        """
        Get the XML string for the TextBox
        """
        return ET.tostring(self.getElement())
