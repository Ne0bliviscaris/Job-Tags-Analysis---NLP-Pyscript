from js import document

from pyscript import display

block_id = "app_loader"


def clear_loader():
    """Czyści kontener animacji bez usuwania jego struktury"""
    loading_animation = document.querySelector(f"#{block_id} .loading-animation")
    loading_animation.innerHTML = ""
    return loading_animation


def load_app():
    """Ładuje aplikację zachowując strukturę kontenera"""
    container = clear_loader()
    welcome_message = "Hello from Python! PyScript working properly."
    container.innerHTML = welcome_message


load_app()
