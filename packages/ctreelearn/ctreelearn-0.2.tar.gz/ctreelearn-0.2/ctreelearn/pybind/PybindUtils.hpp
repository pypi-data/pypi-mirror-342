#include "../include/Common.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <torch/torch.h>

namespace py = pybind11;

#ifndef PYBIND_UTILS_H
#define PYBIND_UTILS_H

class PybindUtils{
    public:

        static py::array_t<PixelType> toNumpy(PixelType* data, int size) {
            // Cria um capsule que sabe como liberar o ponteiro
            py::capsule free_when_done(data, [](void* f) {
                delete[] static_cast<PixelType*>(f);
            });
        
            // Cria o py::array com o capsule responsável por liberar a memória
            return py::array_t<PixelType>(
                { size },               // shape (tamanho do vetor)
                { sizeof(PixelType) },        // strides (distância entre elementos)
                data,                   // ponteiro para os dados
                free_when_done          // capsule que cuida da liberação
            );
        }


        static py::array_t<int> toNumpyInt(int* data, int size) {
            // Cria capsule com função de destruição
            py::capsule free_when_done(data, [](void* f) {
                delete[] static_cast<int*>(f);
            });
        
            // Cria o array NumPy com os dados e o capsule
            return py::array_t<int>(
                { size },                // shape (1D)
                { sizeof(int) },       // strides
                data,                    // ponteiro para os dados
                free_when_done           // capsule que cuida da liberação
            );
        }

        static py::array_t<float> toNumpyFloat(float* data, int size) {
            // Cria capsule com função de destruição
            py::capsule free_when_done(data, [](void* f) {
                delete[] static_cast<float*>(f);
            });
        
            // Cria o array NumPy com os dados e o capsule
            return py::array_t<float>(
                { size },                // shape (1D)
                { sizeof(float) },       // strides
                data,                    // ponteiro para os dados
                free_when_done           // capsule que cuida da liberação
            );
        }
        
    
        static torch::Tensor toTensor(float* data, int size) {
            // Cria um shared_ptr que vai deletar o buffer quando ninguém mais estiver usando
            std::shared_ptr<float> data_ptr(data, [](float* ptr) {
                delete[] ptr;
            });
        
            // Cria o Tensor e garante que o shared_ptr fique vivo até o fim da vida útil do Tensor
            return torch::from_blob(
                data_ptr.get(),         // ponteiro cru
                {size},                 // shape
                [data_ptr](void*) {}    // mantém o shared_ptr vivo (deleter vazio)
            );
        }




};

#endif
