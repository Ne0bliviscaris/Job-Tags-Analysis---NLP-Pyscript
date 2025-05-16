from js import document

from pyscript import display


def clear_output():
    """Clears the output container"""
    output_element = document.getElementById("output")
    output_element.innerHTML = ""


def show_content():
    """Display message on the page"""
    return "Hello from Python! PyScript working properly."


clear_output()
# message = show_content()
# display(message, target="output")
