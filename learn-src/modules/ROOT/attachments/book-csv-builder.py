from typedb.api.connection.options import TypeDBOptions
from typedb.driver import TypeDB, SessionType, TransactionType

ADDRESS = "localhost:1729"
DATABASE = "bookstore"
OUTPUT = "learn-src/modules/ROOT/attachments/books.csv"

query = """
    match
    $book isa book, has isbn-13 $isbn;
    $publisher isa publisher;
    $publication isa publication;
    ($book, $publisher, $publication) isa publishing;
    fetch
    $book: isbn-13, isbn-10, title, page-count, genre, price;
    $publisher: name;
    $publication: year;
    "contributors": {
        match
        $contributor isa contributor, has name $name;
        ($book, $contribution-role: $contributor) isa! $contribution-type;
        $contribution-type relates $contribution-role;
        fetch
        $name;
        $contribution-role;
    };
    "places": {
        match
        $place isa! $place-type, has name $name;
        $place-type sub place;
        ($publication, $place) isa locating;
        fetch
        $name;
        $place-type;
    };
    "stocks": {
        match
        $book has stock $stock;
        fetch
        $stock;
    };
    sort $isbn;
"""

options = TypeDBOptions(infer=True)

with open(OUTPUT, "w") as output:
    output.write(",".join([
        "ISBN-13",
        "ISBN-10",
        "Title",
        "Format",
        "Authors",
        "Editors",
        "Illustrators",
        "Other contributors",
        "Publisher",
        "Year",
        "City",
        "State",
        "Country",
        "Page count",
        "Genres",
        "Price",
        "Stock",
    ]) + "\n")

    with TypeDB.core_driver(ADDRESS) as driver:
        with driver.session(DATABASE, SessionType.DATA) as session:
            with session.transaction(TransactionType.READ, options=options) as transaction:
                results = transaction.query.fetch(query)

                for result in results:
                    format_ = result["book"]["type"]["label"]
                    isbn_13s = [attribute["value"] for attribute in result["book"]["isbn-13"]]
                    isbn_10s = [attribute["value"] for attribute in result["book"]["isbn-10"]]
                    titles = [attribute["value"] for attribute in result["book"]["title"]]
                    page_counts = [attribute["value"] for attribute in result["book"]["page-count"]]
                    genres = [attribute["value"] for attribute in result["book"]["genre"]]
                    prices = [attribute["value"] for attribute in result["book"]["price"]]
                    publisher_names = [attribute["value"] for attribute in result["publisher"]["name"]]
                    publication_years = [attribute["value"] for attribute in result["publication"]["year"]]
                    contributors = [(contributor["contribution-role"]["label"].split(":")[1], contributor["name"]["value"]) for contributor in result["contributors"]]
                    publication_places = [(place["place-type"]["label"], place["name"]["value"]) for place in result["places"]]
                    stocks = [stock["stock"]["value"] for stock in result["stocks"]]

                    author_names = [contributor[1] for contributor in contributors if contributor[0] == "author"]
                    editor_names = [contributor[1] for contributor in contributors if contributor[0] == "editor"]
                    illustrator_names = [contributor[1] for contributor in contributors if contributor[0] == "illustrator"]
                    contributor_names = [contributor[1] for contributor in contributors if contributor[0] == "contributor"]
                    city_names = [place[1] for place in publication_places if place[0] == "city"]
                    state_names = [place[1] for place in publication_places if place[0] == "state"]
                    country_names = [place[1] for place in publication_places if place[0] == "country"]

                    output.write(",".join([
                        ";".join(isbn_13s),
                        ";".join(isbn_10s),
                        ";".join(f"\"{title}\"" for title in titles),
                        format_,
                        ";".join(f"\"{name}\"" for name in author_names),
                        ";".join(f"\"{name}\"" for name in editor_names),
                        ";".join(f"\"{name}\"" for name in illustrator_names),
                        ";".join(f"\"{name}\"" for name in contributor_names),
                        ";".join(f"\"{name}\"" for name in publisher_names),
                        ";".join(f"{year}" for year in publication_years),
                        ";".join(f"\"{name}\"" for name in city_names),
                        ";".join(f"\"{name}\"" for name in state_names),
                        ";".join(f"\"{name}\"" for name in country_names),
                        ";".join(f"{page_count}" for page_count in page_counts),
                        ";".join(f"\"{genre}\"" for genre in genres),
                        ";".join(f"{price}" for price in prices),
                        ";".join(f"{stock}" for stock in stocks),
                    ]).replace("\";\"", ";") + "\n")
