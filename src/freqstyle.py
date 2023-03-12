from config import Config
from repohandle import HandleCodeRepo


class FreqStyle(HandleCodeRepo):
	def __init__(self) -> None:
		super().__init__()
		self.config = Config()
	
	def syntactic(self):
		return self.get_project(self.config.dubbo)
	