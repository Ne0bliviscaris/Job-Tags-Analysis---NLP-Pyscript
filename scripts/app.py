from io import StringIO

import pandas as pd
from js import document
from pyodide.http import pyfetch

import pyscript
from pyscript import display

block_id = "app_loader"


async def main_app():
    """Main app logic."""
    data = await load_csv()
    display(data, target="display_data")


async def load_csv():
    """Load CSV from URL and return DataFrame."""
    response = await pyfetch(
        "https://raw.githubusercontent.com/Ne0bliviscaris/Job-Tags-Analysis---NLP-Pyscript/main/data/job%20offers%20tags.csv"
    )
    text = await response.string()
    return pd.read_csv(StringIO(text))


def clear_loader():
    """Clear the loading indicator."""
    loading_animation = document.querySelector(f"#{block_id} .loading-animation")
    loading_animation.innerHTML = ""
    return loading_animation


async def load_app():
    """Ładuje aplikację zachowując strukturę kontenera"""
    clear_loader()
    await main_app()


load_app()
