from io import StringIO

import pandas as pd
from js import document
from pyodide.http import pyfetch

import pyscript
from pyscript import display


async def main_app():
    """Main app logic."""
    df = await load_csv()
    display(df, target="display_data")


async def load_csv():
    """Load CSV from URL and return DataFrame."""
    processing()
    response = await pyfetch(
        "https://raw.githubusercontent.com/Ne0bliviscaris/Job-Tags-Analysis---NLP-Pyscript/main/data/job%20offers%20tags.csv"
    )
    text = await response.string()
    clear_block()
    return pd.read_csv(StringIO(text))


def processing():
    """Show processing info with spinner."""
    container = document.getElementById("processing_block")
    if not container:
        container = document.createElement("div")
    container.innerHTML = (
        '<div style="display:flex;align-items:center;gap:8px;">'
        '<span class="spinner" style="width:18px;height:18px;border:3px solid #ccc;border-top:3px solid #333;border-radius:50%;display:inline-block;animation:spin 1s linear infinite;"></span>'
        "<span>Processing...</span></div>"
        "<style>@keyframes spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}</style>"
    )


def clear_block(block_id="#processing_block"):
    """Clear the loading indicator in the given block.
    Default = #processing_block"""
    container = document.getElementById(block_id)
    if container:
        container.innerHTML = ""


async def load_app():
    """Ładuje aplikację zachowując strukturę kontenera"""
    clear_block("app_loader")
    await main_app()


load_app()
