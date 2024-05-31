# tag::def_build_book_query[]
def build_book_query(entry: dict) -> str:
    query_parts = ["insert"]

    query_parts += [
        f"""$book isa {entry["Format"]};""",
        f"""$book has isbn-13 "{entry["ISBN-13"]}";""",
        f"""$book has title "{entry["Title"]}";""",
        f"""$book has page-count {entry["Page count"]};""",
        f"""$book has price {entry["Price"]};""",
    ]

    if "ISBN-10" in entry:
        query_parts += [f"""$book has isbn-10 "{entry["ISBN-10"]}";"""]

    query_parts += [f"""$book has genre "{genre}";""" for genre in entry["Genres"]]

    contributors: dict[str, int] = dict()

    for contributor in entry["Authors"] + entry["Editors"] + entry["Illustrators"] + entry["Other contributors"]:
        if contributor not in contributors:
            contributors[contributor] = len(contributors) + 1

    query_parts += [f"""$contributor_{index} isa contributor;""" for contributor, index in contributors.items()]
    query_parts += [f"""$contributor_{index} has name "{contributor}";""" for contributor, index in contributors.items()]
    query_parts += [f"""(work: $book, author: $contributor_{contributors[author]}) isa authoring;""" for author in entry["Authors"]]
    query_parts += [f"""(work: $book, editor: $contributor_{contributors[editor]}) isa authoring;""" for editor in entry["Editors"]]
    query_parts += [f"""(work: $book, illustrator: $contributor_{contributors[illustrator]}) isa illustrating;""" for illustrator in entry["Illustrators"]]
    query_parts += [f"""(work: $book, contributor: $contributor_{contributors[contributor]}) isa contribution;""" for contributor in entry["Other contributors"]]

    query_parts += [
        f"""$publisher isa publisher;""",
        f"""$publisher has name "{entry["Publisher"]}";""",
        f"""(published: $book, publisher: $publisher) isa publishing;""",
    ]

    return "\n".join(query_parts)
# end::def_build_book_query[]


entry = {
    "ISBN-13": "9780008627843",
    "ISBN-10": "0008627843",
    "Title": "The Hobbit",
    "Format": "ebook",
    "Authors": ["J.R.R. Tolkien"],
    "Editors": [],
    "Illustrators": ["J.R.R. Tolkien"],
    "Other contributors": [],
    "Publisher": "Harper Collins",
    "Page count": 310,
    "Genres": ["fiction", "fantasy"],
    "Price": 16.99
}

query = build_book_query(entry)
print(query)
