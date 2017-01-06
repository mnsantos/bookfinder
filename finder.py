from bs4 import BeautifulSoup
import urllib2
from book import Book
from page import Page
import logging
import re

class Finder:

	def __init__(self):
		self.url = "https://www.epublibre.org/catalogo/index/0/nuevo/todos/sin/todos/"
		self.top_url = "https://www.epublibre.org/catalogo/index/0/valorado/disponibles/sin/todos"

	def find(self, book_name):
		book_name = book_name.replace(" ", "%20")
		url = self.url + book_name
		return self.find_aux(url)
		
	def summary(self, book):
		logging.info("Making request to " + book.link)
		response = urllib2.urlopen(book.link)
		soup = BeautifulSoup(response, 'html.parser', from_encoding="utf-8")
		return soup.find("div", class_="detalle").find("div", class_="ali_justi").find("span").text#.encode('ascii', 'ignore').decode('ascii')

	def magnet_link(self, book):
		logging.info("Making request to " + book.link)
		response = urllib2.urlopen(book.link)
		soup = BeautifulSoup(response, 'html.parser', from_encoding="utf-8")
		return soup.find("div", class_="btn-toolbar2").find("div", class_="btn-group").find("a").get("href")

	def find_aux(self, url):
		logging.info("Making request to " + url)
		response = urllib2.urlopen(url)
		soup = BeautifulSoup(response, 'html.parser', from_encoding="utf-8")
		
		book_divs = soup.find_all("div", class_="span2 pad_t_20 ali_centro txt_blanco")

		books = []
		for book_div in book_divs:
			anchor_elem = book_div.find("a")
			book_name = anchor_elem.get("title")#.encode('ascii', 'ignore').decode('ascii')
			book_link = anchor_elem.get("href")
			book_author = book_div.find("div", class_="texto-portada").find("h2").text#.encode('ascii', 'ignore').decode('ascii')
			books.append(Book(book_name, book_author, book_link))

		#next_page = soup.find('a', text=re.compile(r'Siguiente')).get("href")
		next_page = url
		index = url.find("/index/") + len("/index/")
		new_index = int(next_page[index])+18
		next_page = next_page.replace("/index/" + str(url[index]), "/index/" + str(new_index))
		return Page(books, next_page)

	def top(self):
		return self.find_aux(self.top_url)

	def more(self, next_page):
		return self.find_aux(next_page)


