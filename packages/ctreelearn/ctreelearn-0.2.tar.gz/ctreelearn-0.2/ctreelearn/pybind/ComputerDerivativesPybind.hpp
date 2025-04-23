
#include "../pybind/MorphologicalTreePybind.hpp"
#include "../include/NodeMT.hpp"
#include "../include/AttributeComputedIncrementally.hpp"

#include <vector>
#include <stack>
#include <tuple>
#include <pybind11/pybind11.h>
#include <torch/extension.h>
#include <ATen/ops/_sparse_mm.h> 

#include <iostream>

namespace py = pybind11;

#ifndef COMPUTER_DERIVATIVE_PYBIND_H
#define COMPUTER_DERIVATIVE_PYBIND_H


class ComputerDerivativesPybind {
    
    private:
        

    public:

    /*
    static py::tuple gradientsResidualTree(ResidualTreePybind* residualTree, torch::Tensor attrs, torch::Tensor sigmoid, torch::Tensor gradientOfLoss) {
        float* attributes = attrs.data_ptr<float>(); 
        float* sigmoid_ptr = sigmoid.data_ptr<float>();
        float* gradLoss = gradientOfLoss.data_ptr<float>();

        int rows = attrs.size(0);
        int cols = attrs.size(1);
        torch::Tensor gradFilterWeights = torch::empty({rows * cols}, torch::kFloat32);
        torch::Tensor gradFilterBias = torch::empty({rows}, torch::kFloat32);

        float* gradFilterWeights_ptr = gradFilterWeights.data_ptr<float>();
        float* gradFilterBias_ptr = gradFilterBias.data_ptr<float>();

        PixelType* restOfImage = residualTree->getRestOfImage()->rawData();
        MorphologicalTreePtr tree = residualTree->getCTree();
        int residuePos=0;
        int residueNeg=0;
        int residue;
        for(NodeMTPtr node: tree->getIndexNode()){
            int id = node->getIndex();
            
            //computer residue
            if(id > 0){
                 if(node->isMaxtreeNode()){
                    residuePos += node->getParent()->getResidue();
                }else{
                    residueNeg -= node->getParent()->getResidue();
                }
            }
            if(node->isMaxtreeNode())
                residue = restOfImage[node->getCNPs().front()] + residuePos;
            else
                residue = restOfImage[node->getCNPs().front()] - residueNeg;
            
            //computer gradients
            float dSigmoid = sigmoid_ptr[id] * (1 - sigmoid_ptr[id]);
            gradFilterBias_ptr[id] = residue * dSigmoid;
            for (int j = 0; j < cols; j++){
                gradFilterWeights_ptr[id * cols + j] = residue * dSigmoid * attributes[j * rows + id];
            }
        }
    

        torch::Tensor gradWeight = torch::zeros({cols}, torch::kFloat32);
        torch::Tensor gradBias = torch::zeros({1}, torch::kFloat32);

        float* gradWeight_ptr = gradWeight.data_ptr<float>();
        float* gradBias_ptr = gradBias.data_ptr<float>();
        
        std::unique_ptr<float[]> summationGrad_ptr(new float[tree->getNumNodes()]);  
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&summationGrad_ptr, &gradLoss](NodeMTPtr node) -> void { // pre-processing
                summationGrad_ptr[node->getIndex()] = 0;
                for (int p : node->getCNPs()) {
                    summationGrad_ptr[node->getIndex()] += gradLoss[p];
                }
            },
            [&summationGrad_ptr](NodeMTPtr parent, NodeMTPtr child) -> void { // merge-processing
                summationGrad_ptr[parent->getIndex()] += summationGrad_ptr[child->getIndex()];
            },
            [&summationGrad_ptr, &gradWeight_ptr, &gradBias_ptr, &gradFilterBias_ptr, &gradFilterWeights_ptr, &cols](NodeMTPtr node) -> void { // post-processing
                gradBias_ptr[0] += summationGrad_ptr[node->getIndex()] * gradFilterBias_ptr[node->getIndex()];
                for (int j = 0; j < cols; j++)
                    gradWeight_ptr[j] += summationGrad_ptr[node->getIndex()] * gradFilterWeights_ptr[node->getIndex() * cols + j];
                
            }
        );
        return py::make_tuple(gradWeight, gradBias);
    }*/
        
    static py::tuple computerGradientsWithTree(MorphologicalTreePybindPtr tree, torch::Tensor attrs, torch::Tensor sigmoid, torch::Tensor gradientOfLoss) {
        float* attributes = attrs.data_ptr<float>(); 
        float* sigmoid_ptr = sigmoid.data_ptr<float>();
        float* gradLoss = gradientOfLoss.data_ptr<float>();

        int rows = attrs.size(0);
        int cols = attrs.size(1);
        torch::Tensor gradFilterWeights = torch::empty({rows * cols}, torch::kFloat32);
        torch::Tensor gradFilterBias = torch::empty({rows}, torch::kFloat32);

        float* gradFilterWeights_ptr = gradFilterWeights.data_ptr<float>();
        float* gradFilterBias_ptr = gradFilterBias.data_ptr<float>();

        
        std::unique_ptr<float[]> mapLevel(new float[tree->getNumNodes()]);
        mapLevel[0] = tree->getRoot()->getLevel();
        for(NodeMTPtr node: tree->getIndexNode()){
            int id = node->getIndex();
            float dSigmoid = sigmoid_ptr[id] * (1 - sigmoid_ptr[id]);
            if(node->getParent() != nullptr){ 
                int residue = (int)std::abs(node->getLevel() - node->getParent()->getLevel());
                if(node->isMaxtreeNode())
                    mapLevel[node->getIndex()] =  (float)mapLevel[node->getParent()->getIndex()] + (residue * dSigmoid);
                else
                    mapLevel[node->getIndex()] = (float) mapLevel[node->getParent()->getIndex()] - (residue * dSigmoid);
            }
            //computer gradients            
            gradFilterBias_ptr[id] = mapLevel[id];
            for (int j = 0; j < cols; j++){
                gradFilterWeights_ptr[id * cols + j] = mapLevel[id] * attributes[j * rows + id];
            }
        }
        
        /*
        int level;
        for(NodeCT* node: tree->getListNodes()){
            int id = node->getIndex();
            if(node->isMaxtreeNode())
                level = node->getLevel();
            else
                level = -node->getLevel();
            
            //computer gradients
            float dSigmoid = sigmoid_ptr[id] * (1 - sigmoid_ptr[id]);
            gradFilterBias_ptr[id] = level * dSigmoid;
            for (int j = 0; j < cols; j++){
                gradFilterWeights_ptr[id * cols + j] = level * dSigmoid * attributes[j * rows + id];
            }
        }*/
    

        torch::Tensor gradWeight = torch::zeros({cols}, torch::kFloat32);
        torch::Tensor gradBias = torch::zeros({1}, torch::kFloat32);

        float* gradWeight_ptr = gradWeight.data_ptr<float>();
        float* gradBias_ptr = gradBias.data_ptr<float>();
        
        std::unique_ptr<float[]> summationGrad_ptr(new float[tree->getNumNodes()]);  
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&summationGrad_ptr, &gradLoss](NodeMTPtr node) -> void { // pre-processing
                summationGrad_ptr[node->getIndex()] = 0;
                for (int p : node->getCNPs()) {
                    summationGrad_ptr[node->getIndex()] += gradLoss[p];
                }
            },
            [&summationGrad_ptr](NodeMTPtr parent, NodeMTPtr child) -> void { // merge-processing
                summationGrad_ptr[parent->getIndex()] += summationGrad_ptr[child->getIndex()];
            },
            [&summationGrad_ptr, &gradWeight_ptr, &gradBias_ptr, &gradFilterBias_ptr, &gradFilterWeights_ptr, &cols](NodeMTPtr node) -> void { // post-processing
                gradBias_ptr[0] += summationGrad_ptr[node->getIndex()] * gradFilterBias_ptr[node->getIndex()];
                for (int j = 0; j < cols; j++)
                    gradWeight_ptr[j] += summationGrad_ptr[node->getIndex()] * gradFilterWeights_ptr[node->getIndex() * cols + j];
                
            }
        );
        
        return py::make_tuple(gradWeight, gradBias);
    }

    static py::tuple computerGradientsWithJacobian(const torch::Tensor& jacobian,  
                                                    const torch::Tensor& altitudes, 
                                                    const torch::Tensor& attributes, 
                                                    const torch::Tensor& sigmoid,  
                                                    const torch::Tensor& grad_output) { 

        // 1. Gradiente da sigmoide
        auto d_sigmoid = sigmoid * (1 - sigmoid); // Element-wise, Shape: [N_nodes]

        // 2. Gradientes para os nós
        auto grad_filter = altitudes * d_sigmoid; // Shape: [N_nodes]
        auto grad_bias_nodes = grad_filter.unsqueeze(1); // Shape: [N_nodes, 1]
        auto grad_weight_nodes = grad_bias_nodes * attributes; // Shape: [N_nodes, D_attributes]

        // 3. Projeção com Jacobiana
        auto grad_bias_pixels = at::_sparse_mm(jacobian.t(), grad_bias_nodes); // [N_pixels, 1]
        auto grad_weight_pixels = at::_sparse_mm(jacobian.t(), grad_weight_nodes); // [N_pixels, D_attributes]

        // 4. Gradientes finais
        auto grad_bias = grad_output.t().matmul(grad_bias_pixels); // Scalar [1]
        auto grad_weight = grad_output.t().matmul(grad_weight_pixels).reshape({-1, 1});  // Shape: [D_attributes, 1]; // [1, D_attributes]

        return py::make_tuple(grad_bias, grad_weight); 
    }
        
    /*    
    static py::tuple gradients(MorphologicalTreePybindPtr tree, torch::Tensor attrs, torch::Tensor sigmoid, torch::Tensor gradientOfLoss) {
        float* attributes = attrs.data_ptr<float>(); 
        float* sigmoid_ptr = sigmoid.data_ptr<float>();
        float* gradLoss = gradientOfLoss.data_ptr<float>();

        int rows = attrs.size(0);
        int cols = attrs.size(1);
        torch::Tensor gradFilterWeights = torch::empty({rows * cols}, torch::kFloat32);
        torch::Tensor gradFilterBias = torch::empty({rows}, torch::kFloat32);

        float* gradFilterWeights_ptr = gradFilterWeights.data_ptr<float>();
        float* gradFilterBias_ptr = gradFilterBias.data_ptr<float>();

        int residuePos=tree->getRoot()->getLevel();
        int residueNeg=tree->getRoot()->getLevel();
        int residue;
        for(NodeCT* node: tree->getListNodes()){
            int id = node->getIndex();
            
            //computer residue
            if(id > 0){
                 if(node->isMaxtreeNode()){
                    residuePos += node->getParent()->getResidue();
                }else{
                    residueNeg -= node->getParent()->getResidue();
                }
            }
            if(node->isMaxtreeNode())
                residue = residuePos;
            else
                residue = residueNeg;
            
            //computer gradients
            float dSigmoid = sigmoid_ptr[id] * (1 - sigmoid_ptr[id]);
            gradFilterBias_ptr[id] = residue * dSigmoid;
            for (int j = 0; j < cols; j++){
                gradFilterWeights_ptr[id * cols + j] = residue * dSigmoid * attributes[j * rows + id];
            }
        }
    

        torch::Tensor gradWeight = torch::zeros({cols}, torch::kFloat32);
        torch::Tensor gradBias = torch::zeros({1}, torch::kFloat32);

        float* gradWeight_ptr = gradWeight.data_ptr<float>();
        float* gradBias_ptr = gradBias.data_ptr<float>();
        
        float* summationGrad_ptr = new float[tree->getNumNodes()];  
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&summationGrad_ptr, &gradLoss](NodeCT* node) -> void { // pre-processing
                summationGrad_ptr[node->getIndex()] = 0;
                for (int p : node->getCNPs()) {
                    summationGrad_ptr[node->getIndex()] += gradLoss[p];
                }
            },
            [&summationGrad_ptr](NodeCT* parent, NodeCT* child) -> void { // merge-processing
                summationGrad_ptr[parent->getIndex()] += summationGrad_ptr[child->getIndex()];
            },
            [&summationGrad_ptr, &gradWeight_ptr, &gradBias_ptr, &gradFilterBias_ptr, &gradFilterWeights_ptr, &cols](NodeCT* node) -> void { // post-processing
                gradBias_ptr[0] += summationGrad_ptr[node->getIndex()] * gradFilterBias_ptr[node->getIndex()];
                for (int j = 0; j < cols; j++)
                    gradWeight_ptr[j] += summationGrad_ptr[node->getIndex()] * gradFilterWeights_ptr[node->getIndex() * cols + j];
                
            }
        );
        delete[] summationGrad_ptr;
        return py::make_tuple(gradWeight, gradBias);
    }
    */

};

#endif