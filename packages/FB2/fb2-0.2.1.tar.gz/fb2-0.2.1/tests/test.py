from FB2 import FictionBook2, Author

book = FictionBook2()
book.titleInfo.title = "Test book"
book.titleInfo.authors = [Author(nickname="Ae-Mc")]
book.titleInfo.lang = "ru"
book.titleInfo.srcLang = "en"
book.write("test.fb2")
print(book)
