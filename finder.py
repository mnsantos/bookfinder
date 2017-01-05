from bs4 import BeautifulSoup
import urllib2
from book import Book
import logging

class Finder:

	def __init__(self):
		self.url = "https://www.epublibre.org/catalogo/index/nuevo/0/todos/sin/todos/"

	def find(self, book_name):
		book_name = book_name.replace(" ", "%20")
		url = self.url + book_name
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
		return books

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

