def _initialize_torch():
    import os
    import torch  # Garante que PyTorch seja carregado antes do ctl

    # Adicionar o caminho da biblioteca do PyTorch ao LD_LIBRARY_PATH
    torch_lib_path = os.path.join(os.path.dirname(torch.__file__), 'lib')
    os.environ["LD_LIBRARY_PATH"] = torch_lib_path + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")

# Executar a função de inicialização do PyTorch
_initialize_torch()

# Agora importa a versão e outros módulos
from .version import __version__

# Importar os arquivos python
from .dataset import FilteringImagesDataset, InputAndOutputImagesDataset
from .models import DifferentialMorphologicalTree, DifferentialMorphologicalTreeFunction, TreeLossFunction
from .featureSelection import CTLEstimator

# Importar o módulo Pybind11 nativo
import ctreelearn

# Expor as classes do módulo Pybind11
MorphologicalTree = ctreelearn.MorphologicalTree
AdjacencyRelation = ctreelearn.AdjacencyRelation
AttributeFilters = ctreelearn.AttributeFilters
#AttributeOpeningPrimitivesFamily = ctreelearn.AttributeOpeningPrimitivesFamily
ComputerDerivatives = ctreelearn.ComputerDerivatives
IteratorNodesDescendants = ctreelearn.IteratorNodesDescendants
IteratorNodesOfPathToRoot = ctreelearn.IteratorNodesOfPathToRoot
IteratorPixelsOfCC = ctreelearn.IteratorPixelsOfCC
IteratorPostOrderTraversal = ctreelearn.IteratorPostOrderTraversal
IteratorBreadthFirstTraversal = ctreelearn.IteratorBreadthFirstTraversal
NodeMT = ctreelearn.NodeMT
#ResidualTree = ctreelearn.ResidualTree
#UltimateAttributeOpening = ctreelearn.UltimateAttributeOpening
Attribute = ctreelearn.Attribute
# Expor tudo no pacote
__all__ = [
    '__version__',
    # classes dos arquivos python
    'FilteringImagesDataset',
    'InputAndOutputImagesDataset',
    'DifferentialMorphologicalTree',
    'DifferentialMorphologicalTreeFunction',
    'TreeLossFunction',
    'CTLEstimator',
    # Classes Pybind11
    'MorphologicalTree',
    'AdjacencyRelation',
    'AttributeFilters',
    #'AttributeOpeningPrimitivesFamily',
    'ComputerDerivatives',
    'IteratorNodesDescendants',
    'IteratorNodesOfPathToRoot',
    'IteratorPixelsOfCC',
    'NodeMT',
    'Attribute',
    #'ResidualTree',
    #'UltimateAttributeOpening',
]
