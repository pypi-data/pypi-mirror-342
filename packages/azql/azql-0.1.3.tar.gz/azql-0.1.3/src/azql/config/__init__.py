from re import IGNORECASE
from re import compile as re_compile

ENCODING = "utf-8"
DDL_DIR = "ddl"
EXTENSIONS = re_compile(r"csv|json|tsv", IGNORECASE)
COMMON_DELIMITERS = [",", ";", "\t", "|"]
