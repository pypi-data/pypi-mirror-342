import torch
from sklearn.base import BaseEstimator
from sklearn import model_selection
from sklearn.metrics import mean_squared_error
import ctl
from sklearn.base import BaseEstimator

class CTLEstimator(BaseEstimator):

    def __init__(self, dataset, epochs: int, learning_rate:float=0.0001, batch_size:int=8):
        self.dataset = dataset
        self.epochs = epochs
        self.model = None
        self.learning_rate = learning_rate
        self.batch_size = batch_size

    def update_features(self, features):
      features_ds = self.dataset.get_features()
      new_features = {list(features_ds.keys())[list(features_ds.values()).index(k)]:int(k) for k in features[:, :][0] if k in features_ds.values() }
      self.dataset.set_features(new_features)

    def update_index_data(self, index_data):
        self.dataset.set_index_data(index_data)

    def fit(self, features, y):
        self.update_features(features)
        self.update_index_data(y)
        #print("call fit() ==> Features:", self.dataset.get_features())
        #print("call fit() ==> Indexes:", self.dataset.get_index_data())

        trainloader = torch.utils.data.DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)
        #print("call fit() ==> Len(Indexes):", len(self.dataset.get_index_data()), "=", len(trainloader.dataset))

        self.model = ctl.DifferentialMorphologicalTree(self.dataset)
        loss_function = ctl.TreeLossFunction(self.model)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        errors = []

        for epoch in range(self.epochs):
          for i, exemplos in enumerate(trainloader, 0):
            (entradas, saida_desejadas) = exemplos

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            saida_predicoes = self.model(entradas)

            #loss
            loss = loss_function(entradas, saida_desejadas, saida_predicoes)

            #backward + optimize
            loss.backward()
            optimizer.step()

            # print statistics
            errors.append(loss.item())

        #print('Finished Training')
        self.coef_ = features
        return self


    def predict(self, features):
        self.update_features(features)
        #print("call predict() ==> Features:", self.dataset.get_features())
        #print("call predict() ==> Indexes:", self.dataset.get_index_data())
        return self.model(self.dataset.inputs)


    def score(self, features, y):
        self.update_features(features)
        self.update_index_data(y)


        X, y = self.dataset.get_dataXy()
        with torch.no_grad():
            y_pred = self.model(X)
        result = mean_squared_error(y, y_pred)
        print("call score() ==> Features:", self.dataset.get_features(), "score:", result)
        #print("call score() ==> Indexes:", self.dataset.get_index_data())
        #print("call score() ==> Len(Indexes):", len(self.dataset.get_index_data()))
        return -result

