import re
from collections import Counter
from io import StringIO

import pandas as pd
from js import document
from pyodide.http import pyfetch  # type: ignore

from pyscript import display


async def main_app():
    """Main app logic."""
    df = await load_csv()
    raw_tokens = count_tokens_in_df(df)
    text_block("Raw DataFrame", f"{raw_tokens} tokens", before_id="display_data")
    display(df, target="display_data")

    cleaned_df = clean_data(df)
    cleaned_tokens = count_tokens_in_df(cleaned_df)
    display(cleaned_df, target="display_cleaned_data")
    text_block("\n\nProcessed DataFrame", f"{cleaned_tokens} tokens", before_id="display_cleaned_data")


def clean_data(df):
    """Return DataFrame with cleaned 'title' and 'tags' columns."""
    df = df.copy()
    df["title"] = df["title"].apply(clean_titles)
    df["tags"] = df["tags"].apply(clean_tags)
    return df


def count_tokens_in_df(df: pd.DataFrame) -> pd.Series:
    """Count tokens from 'title' and 'tags' columns in a DataFrame."""
    all_tokens = []
    for title in df["title"]:
        if isinstance(title, str):
            all_tokens.extend(title.split())

    for tags_string in df["tags"]:
        if isinstance(tags_string, str) and tags_string:
            tags_list = [tag.strip() for tag in tags_string.split(" | ")]
            for tag_phrase in tags_list:
                all_tokens.extend(tag_phrase.split())

    token_counts = Counter(all_tokens)
    total_tokens = sum(token_counts.values())
    return total_tokens


def text_block(section_title: str, paragraph_text: str = None, before_id: str = None):
    """Create a new div with header and optional paragraph side by side."""
    block = document.createElement("div")
    block.className = "description"
    h3 = document.createElement("h3")
    h3.className = "header"
    h3.innerText = section_title
    block.appendChild(h3)
    if paragraph_text:
        p = document.createElement("p")
        p.className = "paragraph"
        p.innerText = paragraph_text
        block.appendChild(p)
    parent_block = document.querySelector(".container")
    if before_id:
        described_block = document.getElementById(before_id)
        parent_block.insertBefore(block, described_block)
    else:
        parent_block.appendChild(block)


def clean_tags(tags_string):
    """Clean tags string: lowercase, remove digits, punctuation, extra spaces."""
    if not isinstance(tags_string, str):
        return ""
    tags = [tag.strip() for tag in tags_string.split(" | ")]
    cleaned_tags = []

    digits = r"\d+"
    punctuation = r"[^\w\s]"
    whitespace = r"\s+"

    for tag in tags:
        tag = tag.lower()
        tag = re.sub(digits, "", tag)
        tag = re.sub(punctuation, "", tag)
        tag = re.sub(whitespace, " ", tag)
        tag = tag.strip()
        if tag:
            cleaned_tags.append(tag)
    unique_tags = list(dict.fromkeys(cleaned_tags))
    return " | ".join(unique_tags)


def clean_titles(title):
    """Clean title string: lowercase, remove digits, punctuation, extra spaces."""
    digits = r"\d+"
    punctuation = r"[^\w\s]"
    whitespace = r"\s+"

    title = title.lower()
    title = re.sub(digits, "", title)
    title = re.sub(punctuation, "", title)
    title = re.sub(whitespace, " ", title)
    if title.endswith("nowa"):
        title = title[:-4]
    return title.strip()


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
        container.remove()


async def load_app():
    """Ładuje aplikację zachowując strukturę kontenera"""
    clear_block("app_loader")
    await main_app()


load_app()
