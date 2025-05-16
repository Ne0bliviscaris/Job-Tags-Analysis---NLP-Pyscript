from io import StringIO

import pandas as pd
from js import document
from pyodide.http import pyfetch

import pyscript
from pyscript import display

block_id = "app_loader"


def clear_loader():
    """Czyści kontener animacji bez usuwania jego struktury"""
    loading_animation = document.querySelector(f"#{block_id} .loading-animation")
    loading_animation.innerHTML = ""
    return loading_animation


async def load_csv():
    """Load CSV from URL and return DataFrame."""
    response = await pyfetch(
        "https://raw.githubusercontent.com/Ne0bliviscaris/Job-Tags-Analysis---NLP-Pyscript/main/data/job%20offers%20tags.csv"
    )
    text = await response.string()
    return pd.read_csv(StringIO(text))


async def main_app():
    """Main app logic."""
    data = await load_csv()
    display(data)


async def load_app():
    """Ładuje aplikację zachowując strukturę kontenera"""
    clear_loader()
    await main_app()


load_app()
