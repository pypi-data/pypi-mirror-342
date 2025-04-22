import requests
from ._dividentifiers import extract_elements


def div_identifier(header,content):
    try:
        element = extract_elements(Main_header = header, webcontent=content).json()['webpage_elements']
        return element
    except Exception as e:
        print(f"Error: {e}")
        return None

##################### Old packages ############################
def Romulus(header, html):
    if html is None:
        element_name = extract_elements(Main_header = header, webcontent=html).json()['webpage_elements']
        return element_name['div5']
    else:
        raise ValueError("Invalid HTML content")

def Marcius(header, webelements):
    if webelement is None:
        element_name = extract_elements(Main_header = header, webcontent=webelements).json()['webpage_elements']
        return element_name['div6']
    else:
        raise ValueError("Invalid HTML content")
    
def navigator(header, elements):
    if html is None:
        element_name = extract_elements(Main_header = header, webcontent=elements).json()['webpage_elements']
        return element_name['div7']
    else:
        raise ValueError("Invalid HTML content")