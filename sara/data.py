from config import Config
from freqstyle import FreqStyle

class Data:
	def __init__(self) -> None:
		self.config = Config()
		self.projects = {"dspace" : None, "h2" : self.config.h2, "rdf4j" : 
		self.config.rdf4j, "dubbo" : self.config.dubbo, "systemds" : self.config.systemds}
	
	def _get_project_FS(self, dataset):
		return FreqStyle(dataset)()

	def _get_projects_FS(self, datasets):
		return [(FreqStyle(data)()) for data in list(datasets.values())[1:]]
	
	def _get_project_ES(self):
		pass

	def _get_projects_ES(self):
		pass


if __name__ == "__main__":
	data = Data()	
	# res = data._get_projects_FS(data.projects["dubbo"])
	res1 = data._get_projects_FS(data.projects)
	print(res1)