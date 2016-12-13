import os

class Converter:

	def convert(self, file_name):
		print "Converting epub file to mobi..."
		os.system("ebook-convert " + file_name + " " + file_name.replace(".epub", ".mobi"))