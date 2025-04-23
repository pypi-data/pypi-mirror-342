
import torch
import cv2
import numpy 
import math
import os
from sklearn import model_selection
import abc
import ctreelearn as ctl
from sklearn.preprocessing import StandardScaler

class FilteringImagesDataset(torch.utils.data.Dataset, abc.ABC):

  '''
   O construtor simula uma sobrecarga:
     (1) construir a partir de um path, obj = FilteringImagesDataset(dirName="path...", num_rows, num_cols, isMaxtree, isLoaded=False)
     (2) construir a partir de um subconjunto de dados (indenficados pelos indices): obj = FilteringImagesDataset(objFilteringImagesDataset, index_data)
  '''
  def __init__(self, *args, **kwargs):
    super(torch.utils.data.Dataset, self).__init__()

    '''
    - O atributo data[] armazena pares de (entrada, saída) de todo o conjunto de dados
    - O atributo index_data[] armazena os índices dos pares (entrada, saída) que serão considerados no dataset
    '''
    self.__data = []
    self.__index_data = None
    self.__data_trees = []
    self.isLoaded = False
    self.__treeType = True
    self.num_rows = None
    self.num_cols = None
    self.scaler = None
    '''
    O atributo privado ``self.__features`` armazena um dicionario das features que serão utilizadas pelo modelo.
    Estrutura: nome da feature (key do dic) -> index da feature no vetor de atributos (value do dic).
    O valor desse atributo deve ser acesso por meio do método get_features() e set_features
    '''
    self.__features = None

    if(len(args) == 4 or len(args) == 5):
      dirName = args[0]
      self.num_rows = args[1]
      self.num_cols = args[2]
      self.__treeType = int(args[3])  
      
      if(len(args) == 5):
        self.isLoaded = args[4]  
      for f in os.listdir(dirName):
        input = cv2.imread(dirName + "/" + f, cv2.IMREAD_GRAYSCALE)
        input = cv2.resize(input, (self.num_cols, self.num_rows), interpolation = cv2.INTER_AREA)
        img_vector = input.ravel()
        if(self.isLoaded):
            tree = self.get_tree(img_vector)
            features, attrs = self.computerAttributes(tree)
            self.__data_trees.append( (tree,attrs ) )
            if(self.__features is None):
              self.__features = features
        else:
          if(self.__features is None):
            tree = self.get_tree(img_vector)
            self.__features, _ = self.computerAttributes(tree)
        x, y = self.getSample(img_vector)
        self.__data.append( (x, y) )
      self.__index_data = list(range(len(self.__data)))

    elif(len(args) == 2): #Essa construção é sobre um dataset existente
      dataset = args[0]
      idx_data = args[1]
      self.__features = dataset.get_features()
      self.__data = [ dataset[i] for i in idx_data ]
      self.__index_data = list(range(len(self.__data)))
      self.num_rows = dataset.num_rows
      self.num_cols = dataset.num_cols
      self.__treeType = dataset.__treeType
      self.computerAttributes = dataset.computerAttributes
      self.isLoaded = dataset.isLoaded
      if(self.isLoaded):
        self.__data_trees = [ dataset.__data_trees[i] for i in idx_data ]

  def __getitem__(self, index):
    return self.__data[ self.__index_data[index] ]

  def get_tree(self, img_vector): #//0-mintree, 1-maxtree, 2-tree of shapes
    if(self.__treeType == 0):
      return ctl.MorphologicalTree(img_vector, self.num_rows, self.num_cols, False)
    elif(self.__treeType == 1):
      return ctl.MorphologicalTree(img_vector, self.num_rows, self.num_cols, True)
    else:
      return ctl.MorphologicalTree(img_vector, self.num_rows, self.num_cols)

  def computerAttributes(self, tree):
    return ctl.Attribute.computerBasicAttributes(tree)

  def getSample(self, img_vector):
    output= self.filter(img_vector, self.num_rows, self.num_cols)
    return torch.from_numpy(img_vector).float(), torch.from_numpy(output).float()

  def __len__(self):
    return len(self.__index_data)

  def get_features(self):
    return self.__features

  def set_features(self, features):
    self.__features = features

  def get_index_data(self):
    return self.__index_data

  def set_index_data(self, index_data):
    self.__index_data = index_data

  def get_dataXy(self):
    X = []
    y = []
    for i in self.__index_data:
      X.append(self.__data[i][0])
      y.append(self.__data[i][1])
    return X, y

  def __getitem__(self, index):
    return self.__data[ self.__index_data[index] ]

  @abc.abstractmethod
  def filter(self, img_vector):
    pass

  def get_tree_with_attributes(self, index):
    return self.__data_trees[index]

  def get_tree_type(self):
    return self.__treeType
  
  def get_scaler(self):
    return self.scaler
  
  def set_scaler(self, scaler):
    self.scaler = scaler

  def get_num_rows(self):
    return self.num_rows
  
  def get_num_cols(self):
    return self.num_cols

  def get_num_pixels(self):
    return self.num_rows * self.num_cols

  def train_test_split(self, test_size=0.25, normalization=True, random_state=42):
      if(type(test_size) == float):
        test_size = math.ceil(test_size * len(self))
      train_size = len(self) - test_size
      train_idx, test_idx = model_selection.train_test_split(list(range(len(self))), test_size=test_size, random_state=random_state)
      
      # Usar self.__class__ para chamar o construtor de uma subclasse concreta
      train_dataset = self.__class__(self, train_idx)
      test_dataset = self.__class__(self, test_idx)  
      
      if(normalization):
        self.scaler = StandardScaler()
        # Padronização Z-score
        x0, y0 = train_dataset[0]
        tree = self.get_tree(x0)
        _, attributes = self.computerAttributes(tree)

        for i in range(1, len(train_dataset)):
            x, y = train_dataset[i]
            tree = self.get_tree(x)
            _, attrs = self.computerAttributes(tree)
            attributes = numpy.concatenate((attributes, attrs))
        self.scaler.fit(attributes)
        train_dataset.set_scaler(self.scaler)
        test_dataset.set_scaler(self.scaler)
      
      return train_dataset, test_dataset




class InputAndOutputImagesDataset(torch.utils.data.Dataset):

  '''
   O construtor simula uma sobrecarga:
     (1) construir a partir de um path, obj = InputAndOutputImagesDataset(dirName="path...", sufixo_in="_in", sufixo_out="_out", num_rows, num_cols, tree_type, isLoaded=False)
     (2) construir a partir de um subconjunto de dados (indenficados pelos indices): obj = InputAndOutputImagesDataset(objInputAndOutputImagesDataset, index_data)
  '''
  def __init__(self, *args, **kwargs):
    super(torch.utils.data.Dataset, self).__init__()

    '''
    - O atributo data[] armazena pares de (entrada, saída) de todo o conjunto de dados
    - O atributo index_data[] armazena os índices dos pares (entrada, saída) que serão considerados no dataset
    '''
    self.__data = []
    self.__index_data = None
    self.__data_trees = []
    self.isLoaded = False
    self.__treeType = True
    self.num_rows = None
    self.num_cols = None
    self.scaler = None
    '''
    O atributo privado ``self.__features`` armazena um dicionario das features que serão utilizadas pelo modelo.
    Estrutura: nome da feature (key do dic) -> index da feature no vetor de atributos (value do dic).
    O valor desse atributo deve ser acesso por meio do método get_features() e set_features
    '''
    self.__features = None

    if(len(args) == 9):
      files = self.get_input_and_output_files(args[0], args[1], args[2])
      self.num_rows = args[3]
      self.num_cols = args[4]
      self.__treeType = int(args[5])  
      self.isLoaded = args[6]  
      transforms = args[7]
      self.computerAttributes = args[8]
      for input_file, output_file in files:
        input = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)
        output = cv2.imread(output_file, cv2.IMREAD_GRAYSCALE)
        
        input = cv2.resize(input, (self.num_cols, self.num_rows), interpolation = cv2.INTER_AREA)
        output = cv2.resize(output, (self.num_cols, self.num_rows), interpolation = cv2.INTER_AREA)
        input, output = transforms(input, output, self.num_rows, self.num_cols)
        
        output_vector = output.ravel()
        input_vector = input.ravel()
        if(self.isLoaded):
            tree = self.get_tree(input_vector)
            features, attrs = self.computerAttributes(tree)
            self.__data_trees.append( (tree,attrs ) )
            if(self.__features is None):
              self.__features = features
        else:
          if(self.__features is None):
            tree = self.get_tree(input_vector)
            self.__features, _ = self.computerAttributes(tree)
        x, y = self.getSample(input_vector, output_vector)
        self.__data.append( (x, y) )
      self.__index_data = list(range(len(self.__data)))

    elif(len(args) == 2): #Essa construção é sobre um dataset existente
      dataset = args[0]
      idx_data = args[1]
      self.__features = dataset.get_features()
      self.__data = [ dataset[i] for i in idx_data ]
      self.__index_data = list(range(len(self.__data)))
      self.num_rows = dataset.num_rows
      self.num_cols = dataset.num_cols
      self.computerAttributes = dataset.computerAttributes
      self.__treeType = dataset.__treeType
      self.isLoaded = dataset.isLoaded
      if(self.isLoaded):
        self.__data_trees = [ dataset.__data_trees[i] for i in idx_data ]

  def __getitem__(self, index):
    return self.__data[ self.__index_data[index] ]

  def get_input_and_output_files(self, dirName, sufixo_in, sufixo_out):
    files = []
    for in_filename in os.listdir(dirName):
      if in_filename.endswith(sufixo_in):
        base_filename = in_filename[:-len(sufixo_in)] 
        out_filename = base_filename + sufixo_out
        if os.path.exists(os.path.join(dirName, out_filename)):
          files.append( ( os.path.join(dirName, in_filename), os.path.join(dirName, out_filename) ) )
    return files

  def get_tree(self, img_vector): #//0-mintree, 1-maxtree, 2-tree of shapes
    if(self.__treeType == 0):
      return ctl.MorphologicalTree(img_vector, self.num_rows, self.num_cols, False)
    elif(self.__treeType == 1):
      return ctl.MorphologicalTree(img_vector, self.num_rows, self.num_cols, True)
    else:
      return ctl.MorphologicalTree(img_vector, self.num_rows, self.num_cols)

  def getSample(self, input_vector, output_vector):
    return torch.from_numpy(input_vector).float(), torch.from_numpy(output_vector).float()

  def __len__(self):
    return len(self.__index_data)

  def get_features(self):
    return self.__features

  def set_features(self, features):
    self.__features = features

  def get_index_data(self):
    return self.__index_data

  def set_index_data(self, index_data):
    self.__index_data = index_data

  def get_dataXy(self):
    X = []
    y = []
    for i in self.__index_data:
      X.append(self.__data[i][0])
      y.append(self.__data[i][1])
    return X, y

  def __getitem__(self, index):
    return self.__data[ self.__index_data[index] ]

  def get_tree_with_attributes(self, index):
    return self.__data_trees[index]

  def get_tree_type(self):
    return self.__treeType
  
  def get_scaler(self):
    return self.scaler
  
  def set_scaler(self, scaler):
    self.scaler = scaler

  def get_num_rows(self):
    return self.num_rows
  
  def get_num_cols(self):
    return self.num_cols

  def get_num_pixels(self):
    return self.num_rows * self.num_cols

  def train_test_split(self, test_size=0.25, normalization=True, random_state=42):
      if(type(test_size) == float):
        test_size = math.ceil(test_size * len(self))
      train_size = len(self) - test_size
      train_idx, test_idx = model_selection.train_test_split(list(range(len(self))), test_size=test_size, random_state=random_state)
      
      # Usar self.__class__ para chamar o construtor de uma subclasse concreta
      train_dataset = self.__class__(self, train_idx)
      test_dataset = self.__class__(self, test_idx)  
      
      if(normalization):
        self.scaler = StandardScaler()
        # Padronização Z-score
        x0, y0 = train_dataset[0]
        tree = self.get_tree(x0)
        _, attributes = self.computerAttributes(tree)

        for i in range(1, len(train_dataset)):
            x, y = train_dataset[i]
            tree = self.get_tree(x)
            _, attrs = self.computerAttributes(tree)
            attributes = numpy.concatenate((attributes, attrs))
        self.scaler.fit(attributes)
        train_dataset.set_scaler(self.scaler)
        test_dataset.set_scaler(self.scaler)
        
      
      return train_dataset, test_dataset





__all__ = [
    'FilteringImagesDataset',
    'InputAndOutputImagesDataset'
]