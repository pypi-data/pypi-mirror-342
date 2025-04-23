import torch
import pickle
import ctreelearn as ctl
import numpy


class DifferentialMorphologicalTreeFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx, tree, attributes, filter, weight, bias):

        # sigmoid(attributes x W + B)
        #sigmoid = torch.sigmoid( attributes.mm(weight) + bias[None, :] )[:, 0]
        sigmoid = torch.sigmoid(attributes @ weight + bias).squeeze(-1)

        y_pred = filter.filteringSubtractiveScoreRule(sigmoid)

        ctx.tree = tree
        ctx.save_for_backward(attributes, sigmoid)

        # reset the maxtree output on the input device
        return y_pred


    @staticmethod
    def backward(ctx, gradientOfLoss):
        attributes, sigmoid = ctx.saved_tensors
        tree =  ctx.tree
        
        (grad_weight, grad_bias) = ctl.ComputerDerivatives.gradients(tree, attributes, sigmoid, gradientOfLoss)

        #grad_weight = grad_weight.view(grad_weight.size(0), 1)
        #grad_bias = grad_bias.view(1, 1)
        grad_weight = grad_weight.unsqueeze(1)
        grad_bias = grad_bias.unsqueeze(0).unsqueeze(0)

        return None, None, None, grad_weight, grad_bias





class DifferentialMorphologicalTree(torch.nn.Module):

    def __init__(self, trainset):
        super().__init__()
        self.trainset = trainset
        self.trees = {}
        self.filters = {}
        self.attributes = {}
        self.attrs_indexes = list(trainset.get_features().values())
        NUM_FEATURES = 0
        for index, example in enumerate(trainset):
          input, output = example
          if(trainset.isLoaded):
            tree, attrs = trainset.get_tree_with_attributes(index)
          else:    
            tree = trainset.get_tree(input)
            #tree = ctl.MorphologicalTree(input, self.trainset.num_rows, self.trainset.num_cols, trainset.isMaxtree())
            _, attrs = trainset.computerAttributes(tree)
          
          attrs = trainset.get_scaler().transform(attrs)
          
          selected_attrs = attrs[:, self.attrs_indexes]
          NUM_FEATURES = numpy.size(selected_attrs, 1)
          key = str(input.tolist())
          self.trees[key] = tree
          self.attributes[key] = torch.from_numpy(selected_attrs)
          self.filters[key] = ctl.AttributeFilters(tree)

        self.weight = torch.nn.Parameter(torch.empty(NUM_FEATURES, 1), requires_grad=True)
        self.bias = torch.nn.Parameter(torch.empty(1), requires_grad=True)
        #torch.manual_seed(42)
        #torch.nn.init.xavier_uniform_(self.weight)
        #torch.nn.init.zeros_(self.bias)
        self.weight.data.uniform_(-0.00001, 0.00001)
        self.bias.data.fill_(0)

    def saveWeightsAndBias(self, filename):
        file = open(filename, 'wb+')
        pickle.dump((self.weight,self.bias), file)
        file.close()

    def loadWeightsAndBias(self, filename):
        file = open(filename, 'rb')
        (self.weight,self.bias) = pickle.load(file)
        file.close()

    def predict(self, batched_input):
        batched_out = []
        for input in batched_input:
            tree = self.trainset.get_tree(input)
            #tree = ctl.MorphologicalTree(input, self.trainset.num_rows, self.trainset.num_cols, self.trainset.isMaxtree())
            dic, attrs = self.trainset.computerAttributes(tree)
            attrs = self.trainset.get_scaler().transform(attrs)
            attributes = torch.from_numpy(attrs[:, self.attrs_indexes])
            filter = ctl.AttributeFilters(tree)
            sigmoid = torch.sigmoid( attributes.mm(self.weight) + self.bias[None, :] )[:, 0]
            filtered = filter.filteringSubtractiveRule( list(sigmoid > 0.5) )
            batched_out.append(filtered)
        batched_out = numpy.stack(batched_out)
        return batched_out
                      
        
    def get_trees(self, inputs):
      return [ self.trees[str(input.tolist())] for input in inputs ]

    def forward(self, batched_input):
        batched_out = []
        for input in batched_input:
            key = str(input.tolist())

            if(key in self.trees):
              tree = self.trees[key]
              selected_attrs = self.attributes[key]
              filter = self.filters[key]
            else:
              tree = self.trainset.get_tree(input)
              #tree = ctl.MorphologicalTree(input, self.trainset.num_rows, self.trainset.num_cols, self.trainset.isMaxtree())
              dic, attrs = self.trainset.computerAttributes(tree)
              attrs = self.trainset.get_scaler().transform(attrs)
              selected_attrs = torch.from_numpy(attrs[:, self.attrs_indexes])
              filter = ctl.AttributeFilters(tree)

            filtered = DifferentialMorphologicalTreeFunction.apply(tree, selected_attrs, filter, self.weight, self.bias)
            batched_out.append(filtered)
        batched_out = torch.stack(batched_out, dim=0)
        return batched_out



class TreeLossFunction(torch.nn.Module):
    def __init__(self, model):
        super(TreeLossFunction, self).__init__()
        self.model = model

    def forward(self, x, y, y_pred):
        #loss = torch.mean((y_pred - y)**2)
        #regularization = 0
        #for tree in self.model.get_trees(x):
        #  height = self.getHeightTree(tree)
        #  for node in tree.listNodes:
        #    regularization += self.paramReg * height[node]

        #return loss #+ regularization
        return torch.nn.MSELoss()(y_pred, y)
    


## 7. Função de custo customizada

#TODO: Pensar em criar loss function regularizada pela estrutura das árvores.
#- Para um dado `(x, y, y_pred)` as árvores relacionadas estão em `model.get_trees(x)`

#$$Loss(y, \hat{y}) =\frac{1}{m} \sum_{i=0}^{m}(y_i - \hat{y}_i)^2 + \lambda \sum_{C \in T_{f_i}}\text{HeightTree(C)}$$

__all__ = [
    'DifferentialMorphologicalTree',
    'TreeLossFunction',
    'DifferentialMorphologicalTreeFunction'
]