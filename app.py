import streamlit as st
import random
import csv
from typing import List


def format_book(book_info: List[str]) -> str:
    """Formats a book from the CSV file into a human-readable string."""
    desired_len = 7
    format_str = ""
    (title, authors, shelf, genres, owner, short_desc, long_desc) = book_info + [""] * (desired_len - len(book_info))
    if authors:
        # when there are multiple authors, add an "and" before the last one
        author_list = authors.split(", ")
        if len(author_list) > 2:
            author_list[-1] = "and " + author_list[-1]
            format_str += f"I recommend **{title}** by {', '.join(author_list)}.\n\n"
        elif len(author_list) == 2:
            format_str += f"I recommend **{title}** by {author_list[0]} and {author_list[1]}.\n\n"
        else:
            format_str += f"I recommend **{title}** by {author_list[0]}.\n\n"
    else:
        format_str += f"I recommend **{title}**.\n\n"

    if shelf:
        format_str += f"Shelf: {shelf}\n\n"
    else:
        format_str += f"Shelf: Not assigned (maybe you could update it? 😉)\n\n"

    if genres:
        format_str += f"Genres: {genres}\n\n"

    if owner:
        if owner == "House":
            format_str += f"Owner: This book came with the house when we got it, so there is no owner.\n\n"
        else:
            format_str += f"Owner: {owner}\n\n"

    if short_desc:
        format_str += f"Short description: {short_desc}\n\n"

    return format_str


st.title("Cavendish Labs Library AI Assistant")
if st.button("Recommend a random book"):
    with open('books.csv', 'r', encoding="cp1252") as f:
        print(f)
        reader = csv.reader(f)
        books = list(reader)[1:]  # ignore header
        random_book = random.choice(books)
        st.write(format_book(random_book))
