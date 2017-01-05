import os
import logging

class Converter:

	def convert(self, file_name):
		logging.info("Converting " + file_name + " file to mobi...")
		name =  file_name.replace(" ", "\ ").replace("(", "\(").replace(")","\)").replace(",","\,").replace("[","\[").replace("]","\]")
		new_name = name.replace(".epub", ".mobi")
		os.system("ebook-convert " + name + " " + new_name)
		return file_name.replace(".epub", ".mobi")