#ifndef COMPONENT_TREE_PYBIND_H
#define COMPONENT_TREE_PYBIND_H


#include "../include/MorphologicalTree.hpp"
#include "../pybind/PybindUtils.hpp"
#include "../include/Common.hpp"

#include <pybind11/numpy.h>



namespace py = pybind11;
class MorphologicalTreePybind;
using MorphologicalTreePybindPtr = std::shared_ptr<MorphologicalTreePybind>;

class MorphologicalTreePybind : public MorphologicalTree {


 public:
    using MorphologicalTree::MorphologicalTree;

    MorphologicalTreePybind(py::array_t<PixelType> input, int numRows, int numCols, std::string ToSInperpolation="self-dual")
        : MorphologicalTree(Image::fromExternal(static_cast<PixelType*>(input.request().ptr), numRows, numCols), ToSInperpolation) { }

	MorphologicalTreePybind(py::array_t<PixelType> input, int numRows, int numCols, bool isMaxtree, double radiusOfAdjacencyRelation=1.5)
        : MorphologicalTree(Image::fromExternal(static_cast<PixelType*>(input.request().ptr), numRows, numCols), isMaxtree, radiusOfAdjacencyRelation) { }
   



    /*
    py::array_t<int> getOrderedPixels(){
        int n = this->numRows * this->numCols;
        return PybindUtils::toNumpy(this->orderedPixels, n);
    }

    py::array_t<int> getParent(){
        int n = this->numRows * this->numCols;
        return PybindUtils::toNumpy(this->parent, n);
    }*/

    torch::Tensor getResidues(){
        float* residues = new float[this->numNodes];
        for(NodeMTPtr node: indexToNode){
            residues[node->getIndex()] = node->getResidue();
        }
        return PybindUtils::toTensor(residues, this->numNodes);
    }
    
    torch::Tensor getAltitudes(){
        float* altitudes = new float[this->numNodes];
        for(NodeMTPtr node: indexToNode){
            if(node->isMaxtreeNode())
                altitudes[node->getIndex()] = node->getLevel();
            else
                altitudes[node->getIndex()] = -node->getLevel();
        }
        return PybindUtils::toTensor(altitudes, this->numNodes);
    }
    
    /*
    py::array_t<int> getImageAferPruning(NodeMTPtr node){
        int n = this->numRows * this->numCols;
        int* imgOut = MorphologicalTree::getImageAferPruning(node); // Chamar método da superclasse
        return PybindUtils::toNumpy(imgOut, n);
    }
    */

    py::array_t<int> reconstructionImage(){
        int n = this->numRows * this->numCols;
        PixelType* imgOut = new PixelType[n];
        MorphologicalTree::reconstruction(this->root, imgOut);
        return PybindUtils::toNumpy(imgOut, n);
    }

    torch::Tensor getJacobianOfCCs() {
        // Vetores para armazenar índices e valores
        std::vector<int64_t> row_indices;
        std::vector<int64_t> col_indices;
        std::vector<float> values;

        // Iterar pelos nós da árvore para preencher os índices e valores
        for (NodeMTPtr node : this->indexToNode) {
            for (int pixel : node->getPixelsOfCC()) {
                row_indices.push_back(node->getIndex()); // Linha da matriz
                col_indices.push_back(pixel);           // Coluna da matriz
                values.push_back(1.0);                  // Valor não zero
            }
        }


        // Criar tensores para índices e valores
        auto values_tensor = torch::tensor(values, torch::kFloat32); 
        auto row_tensor = torch::tensor(row_indices, torch::kLong);  
        auto col_tensor = torch::tensor(col_indices, torch::kLong);  

        auto indices = torch::stack({row_tensor, col_tensor}); 

        int64_t num_pixels = this->numRows * this->numCols;

        // Shape da matriz esparsa
        std::vector<int64_t> shape = {this->numNodes, num_pixels};

        // Criar a matriz esparsa no formato COO
        auto sparse_J = torch::sparse_coo_tensor(indices, values_tensor, shape);

        
        return sparse_J;
    }


    torch::Tensor getJacobianOfCNPs() {
        // Vetores para armazenar índices e valores
        std::vector<int64_t> row_indices;
        std::vector<int64_t> col_indices;
        std::vector<float> values;

        // Iterar pelos nós da árvore para preencher os índices e valores
        for (NodeMTPtr node : this->indexToNode) {
            for (int pixel : node->getCNPs()) {
                row_indices.push_back(node->getIndex()); // Linha da matriz
                col_indices.push_back(pixel);           // Coluna da matriz
                values.push_back(1.0);                  // Valor não zero
            }
        }

        // Criar tensores para índices e valores
        auto values_tensor = torch::tensor(values, torch::kFloat32); 
        auto row_tensor = torch::tensor(row_indices, torch::kLong);  
        auto col_tensor = torch::tensor(col_indices, torch::kLong);  

        auto indices = torch::stack({row_tensor, col_tensor}); 

        int64_t num_pixels = this->numRows * this->numCols;

        // Shape da matriz esparsa
        std::vector<int64_t> shape = {this->numNodes, num_pixels};

        // Criar a matriz esparsa no formato COO
        auto sparse_J = torch::sparse_coo_tensor(indices, values_tensor, shape);

        
        return sparse_J;
    }

    /*static py::array_t<int> computerParent(py::array_t<int> input, int numRows, int numCols, bool isMaxtree){
		auto buf_input = input.request();
		int* img = (int *) buf_input.ptr;
		ComponentTree tree(img, numRows, numCols, isMaxtree);
		return PybindUtils::toNumpy(tree.getParent(), numRows * numCols);;
	}*/



    static py::array_t<PixelType> recNode(NodeMTPtr _node) {
        int n = _node->getAreaCC();
        NodeMTPtr parent = _node->getParent();
        while (parent != nullptr) {
            n = parent->getAreaCC();
            parent = parent->getParent();
        }

        PixelType* imgOut = new PixelType[n];
        for (int p = 0; p < n; p++)
            imgOut[p] = 0;
        for(int p: _node->getPixelsOfCC()){
            imgOut[p] = 255;
        }
        return PybindUtils::toNumpy(imgOut, n);
    }
};



#endif