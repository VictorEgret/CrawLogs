import os
import sys
import gzip

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

def extract_log_data(data: str, extracted: list[Player]) -> None:
	print(data)


def extract_data(path: str) -> list[Player]:
	data = []
	for file in os.listdir(path):
		zip_type = get_type(file)
		if not zip_type:
			pass
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

if __name__ == "__main__":
	print("Logs data crawler by Victor Egret for Minecraft 1.19.3")
	# TODO handle windows paths
	if len(sys.argv) == 1:
		path = input("Enter the logs folder path: ")
	else:
		path = sys.argv[1]
	if not path[-1] == '/':
		path += '/'
	if not os.path.exists(path):
		print(f"Cannot find {path}", file=sys.stderr)
		exit(1)
	if not os.path.isdir(path):
		print(f"{path} is not a directory", file=sys.stderr)
		exit(1)
	
	data = extract_data(path)
	print(sys.argv)
	for player in data:
		print(player)
