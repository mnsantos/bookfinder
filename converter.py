import os

class Converter:

	def convert(self, file_name):
		print "Converting " + file_name + " file to mobi..."
		name =  file_name.replace(" ", "\ ").replace("(", "\(").replace(")","\)").replace(",","\,").replace("[","\[").replace("]","\]")
		new_name = name.replace(".epub", ".mobi")
		print name
		print new_name
		os.system("ebook-convert " + name + " " + new_name)
		return file_name.replace(".epub", ".mobi")