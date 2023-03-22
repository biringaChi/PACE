from config import Config
from freqstyle import FreqStyle
from repohandle import HandleRepo

class Data(HandleRepo):
	def __init__(self) -> None:
		super().__init__()
		self.config = Config()
		self.projects = {
			"addressbook": None,
			"dspace" : None, 
			"h2" : self.config.h2, 
			"rdf4j" : self.config.rdf4j, 
			"dubbo" : self.config.dubbo, 
			"systemds" : self.config.systemds
			}
	
	def _get_projects(self, project):
		return self.get_project(project)
	
	def _get_runtime(self, projects):
		pass

	# def _get_project_FS(self, dataset):
	# 	return FreqStyle(dataset)()

	# def _get_projects_FS(self, datasets):
	# 	return [(FreqStyle(data)()) for data in list(datasets.values())[1:]]
	
	# def _get_project_ES(self):
	# 	pass

	# def _get_projects_ES(self):
	# 	pass


if __name__ == "__main__":
	data = Data()	
	# res = data._get_projects_FS(data.projects["dubbo"])
	# res1 = data._get_projects_FS(data.projects)
	# print(res1)