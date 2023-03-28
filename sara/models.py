import sklearn

class RF:
	def __init__(self) -> None: pass

	def __call__(self):
		return sklearn.ensemble.RandomForestClassifier()

class SVM:
	def __init__(self) -> None: pass

	def __call__(self, max_iter):
		return sklearn.svm.LinearSVC(max_iter = max_iter)

class NB:
	def __init__(self) -> None: pass

	def __call__(self):
		return sklearn.naive_bayes.GaussianNB()

class KNN:
	def __init__(self) -> None: pass

	def __call__(self):
		return sklearn.neighbors.KNeighborsClassifier()

class LR:
	def __init__(self) -> None: pass

	def __call__(self, *lr):
		solver, max_iter = lr
		return sklearn.linear_model.LogisticRegression(solver = solver, max_iter = max_iter)

class MLP:
	def __init__(self) -> None: pass
	
	def __call__(self):
		return sklearn.neural_network.MLPRegressor()
