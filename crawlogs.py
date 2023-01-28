import os
import sys
import shutil
import tarfile
from enum import Enum

class Player:
	name: str
	uuid: str
	ips: set

	def __init__(self):
		self.name = ""
		self.uuid = ""
		self.ips = {}

class ZipFile:
	def __init__(self, path:str):
		self.path = path
		if path.endswith(".tar.gz"):
			self.type = ".tar.gz"
		elif path.endswith(".zip"):
			self.type = ".zip"
	
	def __repr__(self):
		return self.path


def is_compressed_file(file: str) -> bool:
	return file.endswith(".tar.gz") or file.endswith(".zip")

def extract_files(path: str) -> list[str]:
	files = list(map(lambda file: ZipFile(path + file), filter(is_compressed_file, os.listdir(path))))
	for file in files:
		try:
			unzip = tarfile.open(file.path)
			unzip.extractall(path + "crawltemp")
			unzip.close()
		except tarfile.ReadError:
			print(f"Error wile reading {file.path}", file=sys.stderr)
	try:
		shutil.copyfile(path + "latest.log", path + "crawltemp")
	except: pass
	return os.listdir(path + "crawltemp")

def extract_data(files: list[str]) -> list[Player]:
	print(files)

if __name__ == "__main__":
	print("Logs data crawler by Victor Egret for Minecraft 1.19.3")
	#path = input("Enter the logs folder path: ")
	path = "example_logs" # Debug purpose, will be removed
	if not path[-1] == '/':
		path += '/'
	if not os.path.exists(path):
		print(f"Cannot find {path}", file=sys.stderr)
		exit(1)
	if not os.path.isdir(path):
		print(f"{path} is not a directory", file=sys.stderr)
		exit(1)
	
	files = extract_files(path)
	data = extract_data(files)

	try:
		shutil.rmtree(path + "crawltemp")
	except:
		print("Error while deleting temp file", file=sys.stderr)
	