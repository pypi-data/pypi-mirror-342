#include "../pybind/MorphologicalTreePybind.hpp"
#include "../pybind/AttributeComputedIncrementallyPybind.hpp"
#include "../pybind/PybindUtils.hpp"

#include "./Tests.hpp"

#include <pybind11/embed.h>  // Necessário para usar objetos Python no C++
#include <pybind11/numpy.h>
#include <iostream>
#include <iomanip>

namespace py = pybind11;

int main(int argc, char const *argv[])
{
    py::scoped_interpreter guard{};  // Inicializa o interpretador Python

    

    // Ler a imagem de teste
    ImagePtr img = getSimpleImage();
    int numRows = img->numCols;
    int numCols = img->numRows;
    py::array_t<int> imgNumpy = PybindUtils::toNumpy(img->rawData(), numRows*numCols);    

    // Cria uma árvore de componentes usando o wrapper Pybind
    MorphologicalTreePybindPtr tree = std::make_unique<MorphologicalTreePybind>(imgNumpy, numRows, numCols, true);
    std::cout << "Árvore de componentes criada com sucesso." << std::endl;

    // Define o valor de delta
    int delta = 1;

    // Chama o método de cálculo de atributos
    std::string padding="last-padding";
    auto [attributeNames, attrsArray] = AttributeComputedIncrementallyPybind::computerBasicAttributes(tree, delta, padding);
    std::cout << "Atributos calculados com sucesso." << std::endl;

    // Exibe o dicionário de atributos
    std::cout << "\nMapeamento de índices para atributos em attributeNames:" << std::endl;
    for (auto item : attributeNames) {
        std::string key = py::str(item.first);  // Converte a chave para string
        int value = py::cast<int>(item.second);  // Converte o valor para int
        std::cout << key << ": " << value << std::endl;
    }

    // Exibe o array de atributos (attrsArray)
    auto buffer = attrsArray.request();  // Obtém as informações do buffer
    float* ptr = static_cast<float*>(buffer.ptr);
    int numNodes = buffer.shape[0];
    int numAttributes = buffer.shape[1];

    std::cout << "\nConteúdo de attrsArray:" << std::endl;
    for (int i = 0; i < numNodes; ++i) {
        std::cout << "Node " << i << ": ";
        for (int j = 0; j < numAttributes; ++j) {
            std::cout << std::setw(10) << ptr[i * numAttributes + j] << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
