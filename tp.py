import logging
from os import getenv
from sqlite3 import connect, Connection
from typing import Optional
from pandas import read_csv, DataFrame
from numpy import nan

EMPTY_BOOK_TITLE = ""
ANONYMOUS_AUTHOR = "Anonymous"
MIN_RATING = 1
MAX_RATING = 5
MIN_PAGE_COUNT = 1
MIN_PRICE = 0
MIN_RATING_COUNT = 0


file = getenv("DB_TP_FILE_NAME", "Amazon_BooksDataset.csv")
database_name = getenv("DB_TP_DATABASE_NAME", "amazon_books.db")
log_level = getenv("DB_TP_LOG_LEVEL", logging.INFO)

if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
    log_level = "INFO"
logging.basicConfig(
    level=logging.getLevelName(log_level),
    format="%(levelname)s: %(message)s"
)


def get_sanitized_int(number: str) -> int:
    """Clean an integer. Remove 'thousands delimiter' (,)."""
    if type(number) == str:
        return int(number.replace(',', ''))
    return int(number)


def get_sanitized_float(number: str) -> float:
    """Clean an float. Remove 'thousands delimiter' (,)."""
    if type(number) == str:
        return float(number.replace(',', ''))
    return float(number)


def get_name(book: hash) -> str:
    """Clean the book name. Defaults to empty book name"""
    return str(book.Book_Name) if book.Book_Name else EMPTY_BOOK_TITLE


def get_author(book: hash) -> str:
    """Clean the book author. Defaults to anonymous author"""
    author = ANONYMOUS_AUTHOR
    if book.Author:
        author = str(book.Author)
    else:
        logging.warning("Value for author: %s is empty", book.Author)
    return author


def get_page_count(book: hash) -> Optional[int]:
    """Clean the page count. Must be greater than or equal to zero."""
    page_count: int
    try:
        page_count = get_sanitized_int(book.Pages)
        if page_count < MIN_PAGE_COUNT:
            logging.warning(
                "Page count %s is lower than minimum a number %s",
                page_count,
                MIN_PAGE_COUNT
            )
            page_count = None
    except ValueError:
        logging.warning("Page count %s is not a number", book.Pages)
        page_count = None
    return page_count


def get_language(book: hash) -> Optional[str]:
    """Clean the language. Can be empty"""
    if not book.Language:
        logging.warning("Language is empty")
    return book.Language or None


def get_rating(book: hash) -> Optional[float]:
    """Clean the book rating. Must be between one and five."""
    rating: float
    try:
        rating = get_sanitized_float(book.Ratings)
        if rating < MIN_RATING:
            logging.warning(
                "Rating %s is less than minimum %s", rating, MIN_RATING
            )
            rating = None
        elif rating > MAX_RATING:
            logging.warning(
                "Rating %s is greater than maximum %s", rating, MAX_RATING
            )
            rating = None
    except ValueError:
        logging.warning("Rating %s is not a number", book.Ratings)
        rating = None
    return rating


def get_total_rating_count(book: hash) -> int:
    """Clean the total Ratings. Must be greater than zero."""
    total_rating_count: int
    try:
        total_rating_count = get_sanitized_int(book.Total_Ratings)
        if total_rating_count < MIN_RATING_COUNT:
            total_rating_count = MIN_RATING_COUNT
            logging.warning(
                "Rating count %s lower than minimum %s.",
                total_rating_count,
                MIN_RATING_COUNT
            )
    except ValueError:
        total_rating_count = MIN_RATING_COUNT
        logging.warning(
            "Rating count %s is not a number", book.Total_Ratings
        )
    return total_rating_count


def get_price(book: hash) -> Optional[float]:
    """Clean the total Ratings. Must be greater than zero."""
    price: float
    try:
        price = get_sanitized_float(book.Price)
        if price < MIN_PRICE:
            logging.warning("Price %s lower than minimum %s", price, MIN_PRICE)
            price = None
    except ValueError:
        price = None
    return price


def get_category(book: hash) -> Optional[str]:
    """Clean the category. Can be empty."""
    if not book.Category:
        logging.warning("Category is empty")
    return book.Category or None


def save_author(db: Connection, author: str) -> None:
    """Save the author into the database. Ignores it if it already there."""
    db.execute("INSERT OR IGNORE INTO authors VALUES (?)", [(author)])
    db.commit()


def save_language(db: Connection, language: str) -> None:
    """Save the language into the database. Ignores it if it already there."""
    db.execute("INSERT OR IGNORE INTO languages VALUES (?)", [(language)])
    db.commit()


def save_category(db: Connection, category: str) -> None:
    """Save the category into the database. Ignores it if it already there."""
    db.execute("INSERT OR IGNORE INTO categories VALUES (?)", [(category)])
    db.commit()


logging.info("Opening database: %s...", database_name)
db = connect(database_name)
# Extract
logging.info("Reading file: %s...", file)
books = read_csv(
    file,
    header=0,
    names=[
        "Book_Name",
        "Author",
        "Pages",
        "Language",
        "Ratings",
        "Total_Ratings",
        "Price",
        "Category"
    ]
).fillna(0)
# if a column is empty pandas uses numpy.nan
# Use fillna(0) for easier processing
# Transform
for book in books.itertuples():
    logging.debug("Processing: %s", book)
    book_name = get_name(book)
    author = get_author(book)
    if not book_name and author == ANONYMOUS_AUTHOR:
        logging.warning("Invalid book, name and author are empty: %s", book)
        continue
    page_count = get_page_count(book)
    language = get_language(book)
    rating = get_rating(book)
    total_rating_count = get_total_rating_count(book)
    price = get_price(book)
    category = get_category(book)
    logging.debug("Parsed data: %s",
        {
            "book_name": book_name,
            "author": author,
            "page_count": page_count,
            "language": language,
            "rating": rating,
            "total_rating_count": total_rating_count,
            "price": price,
            "category": category,
        }
    )
    # Load
    logging.debug("Saving data in database...")
    logging.debug("Saving author...")
    save_author(db, author)
    if language:
        logging.debug("Saving language...")
        save_language(db, language)
    if category:
        logging.debug("Saving category...")
        save_category(db, category)
    saved_book = db.execute(
        "SELECT name, authorId FROM books WHERE name=? AND authorId=?",
        [book_name, author]
    ).fetchone()
    if saved_book is None:
        logging.debug("Saving book...")
        db.execute(
            "INSERT INTO books VALUES (?,?,?,?,?,?,?,?)",
            [
                book_name,
                author,
                page_count,
                language,
                rating,
                total_rating_count,
                price,
                category
            ]
        )
        db.commit()
    else:
        logging.warning("Ignoring duplicated book: %s", book)
logging.debug("Closing database connection...")
db.close()
