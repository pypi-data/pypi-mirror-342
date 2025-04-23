#include "../include/MorphologicalTree.hpp"
#include "../include/AttributeComputedIncrementally.hpp"
#include "../include/ComputerMSER.hpp"

#include "./Tests.hpp"

#include <iomanip> 

#include <iostream>
#include <fstream>
#include <stdexcept>

#include <vector>

int main(int argc, char const *argv[])
{
    ImagePtr image = getSimpleImage();

   // printImage(img_pointer, numRows, numCols);
    std::cout << "img_pointer ok" << std::endl;
    
    // Criar um ComponentTree
    MorphologicalTreePtr tree = std::make_shared<MorphologicalTree>(image, true);
    std::cout << "tree ok" << std::endl;

    printTree(tree->getRoot());

    // Criar um AttributeComputedIncrementally::computerArea
    int n = tree->getNumNodes();	
    
    int delta = 3;
    auto [attributeNamesDelta, attrsDelta] = AttributeComputedIncrementally::computerBasicAttributes(tree, delta, "last-padding");
    std::cout << "attributes ok" << std::endl;

    // Depuração do mapeamento em `attributeNamesDelta`
    std::cout << "Mapeamento de índices para atributos em attributeNamesDelta:" << std::endl;
    for (const auto& pair : attributeNamesDelta.mapIndexes) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }

    // Verificação direta do conteúdo de `attrsDelta`
    std::cout << "\nConteúdo de attrsDelta para verificação de AREA, AREA_Asc1, AREA_Desc1:" << std::endl;
    for (NodeMTPtr node : tree->getIndexNode()) {
        int nodeIndex = node->getIndex();
        if (attributeNamesDelta.mapIndexes.count("AREA")) {
            std::cout << "Node " << nodeIndex << " - AREA: " 
                    << attrsDelta[nodeIndex + attributeNamesDelta.mapIndexes["AREA"]] 
                    << std::endl;
        }
        if (attributeNamesDelta.mapIndexes.count("AREA_Asc1")) {
            std::cout << "Node " << nodeIndex << " - AREA_Asc1: " 
                    << attrsDelta[nodeIndex + attributeNamesDelta.mapIndexes["AREA_Asc1"]] 
                    << std::endl;
        }
        if (attributeNamesDelta.mapIndexes.count("AREA_Desc1")) {
            std::cout << "Node " << nodeIndex << " - AREA_Desc1: " 
                    << attrsDelta[nodeIndex + attributeNamesDelta.mapIndexes["AREA_Desc1"]] 
                    << std::endl;
        }
    }


  // Imprimir apenas os atributos com prefixo "AREA" e seus ascendentes/descendentes
    for (NodeMTPtr node : tree->getIndexNode()) {
        int nodeIndex = node->getIndex();
        std::cout << "Node: " << nodeIndex << std::endl;
        for (const auto& pair : attributeNamesDelta.mapIndexes) {
            const std::string& attrName = pair.first;

            if (attrName.rfind("AREA", 0) == 0) {
                // Imprime o valor principal de AREA
                std::cout << attrName << ": " 
                          << attrsDelta[nodeIndex + attributeNamesDelta.mapIndexes[attrName]] 
                          << std::endl;
            }
        }
        std::cout << std::endl;
    }

    // Limpeza final
    delete[] attrsDelta;  // Libera ptrValues, assumindo que foi alocado dinamicamente
    

    return 0;
}
