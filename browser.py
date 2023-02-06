import os
import sys
import gzip
from uuid import *

ZIP_TYPES = {".gz"}

class Player:
	name: str
	uuid: str
	ips: set

	def __init__(self) -> None:
		self.name = ""
		self.uuid = ""
		self.ips = {}

	def __repr__(self) -> str:
		pass

def get_type(file: str) -> str:
	for _type in ZIP_TYPES:
		if file.endswith(_type):
			return _type
	return None

def extract_log_data(data: str, extracted: dict[UUID]) -> None:
	data = data.split("\n")
	it = iter(data)
	try:
		while True:
			line = next(it)
			if "User Authenticator" in line and "UUID" in line:
				line = line.split()
				try:
					id = UUID(line[-1])
					name = line[-3]
					line = next(it)
					line = next(it)
					line = line.split()
					ip = line[3][:-1].split("/")[1]
					print(id, name, ip)
					# TODO Finish adding players in extracted
				except:
					pass

	except:
		pass

def extract_data(path: str) -> dict[UUID]:
	data = {}
	for file in os.listdir(path):
		zip_type = get_type(file)
		if not zip_type:
			continue
		try:
			with gzip.open(path + file, 'rt', encoding="utf-8") as f_in:
				extract_log_data(f_in.read(), data)
		except:
			print(f"Error while extracting {path + file}", file=sys.stderr)
	try:
		with open(path + "latest.log", 'rt', encoding="utf-8") as f_in:
			extract_log_data(f_in.read(), data)
	except: pass
	return data

def main():
	print("Logs data crawler by Victor Egret for Minecraft 1.19.3")
	# TODO handle windows paths
	if len(sys.argv) == 1:
		path = input("Enter the logs folder path: ")
	else:
		path = sys.argv[1]
	if not path[-1] == '/':
		path += '/'
	if not os.path.exists(path):
		raise FileNotFoundError(f"Cannot find {path}")
	if not os.path.isdir(path):
		raise NotADirectoryError(f"{path} is not a directory")
	
	data = extract_data(path)
	for player in data.items():
		print(player)

if __name__ == "__main__":
	try:
		main()
	except BaseException as e:
		print(e, file=sys.stderr)
		exit(1)
