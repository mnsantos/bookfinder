from bs4 import BeautifulSoup
import urllib2
from book import Book

class Finder:

	def __init__(self):
		self.url = "https://www.epublibre.org/catalogo/index/nuevo/0/todos/sin/todos/"

	def find(self, book_name):
		book_name = book_name.replace(" ", "%20")
		url = self.url + book_name
		print "Making request to " + url
		response = urllib2.urlopen(url)
		soup = BeautifulSoup(response, 'html.parser')
		
		book_divs = soup.find_all("div", class_="span2 pad_t_20 ali_centro txt_blanco")

		books = []
		for book_div in book_divs:
			ancher_element = book_div.find("a")
			book_name = ancher_element.get("title")
			book_link = ancher_element.get("href")
			books.append(Book(book_name, book_link))
		return books

	def magnet_link(self, book):
		print "Making request to " + book.link
		response = urllib2.urlopen(book.link)
		soup = BeautifulSoup(response, 'html.parser')
		return soup.find("btn-toolbar2").find("btn-group").find("a").get("href")


