
#ifndef ATTRIBUTE_FILTERS_PYBIND_H
#define ATTRIBUTE_FILTERS_PYBIND_H

#include "../include/NodeMT.hpp"
#include "../include/AttributeFilters.hpp"
#include "../include/Common.hpp"

#include "../pybind/MorphologicalTreePybind.hpp"
#include "../pybind/AttributeComputedIncrementallyPybind.hpp"
#include "../pybind/PybindUtils.hpp"

#include <stack>
#include <vector>
#include <limits.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <torch/extension.h>

#define UNDEF -999999999999

class AttributeFiltersPybind : public AttributeFilters{


    public:
    using AttributeFilters::AttributeFilters;

    AttributeFiltersPybind(MorphologicalTreePybindPtr tree): AttributeFilters(tree){}

    py::array_t<int> filteringByPruningMin(py::array_t<float> &attr, float threshold){

        auto bufAttribute = attr.request();
        float *attribute = (float *) bufAttribute.ptr;
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        PixelType* imgOutput = new PixelType[n];

        AttributeFilters::filteringByPruningMin(this->tree, attribute, threshold, imgOutput);

        return PybindUtils::toNumpy(imgOutput, n);
    }

    py::array_t<int> filteringByPruningMax(py::array_t<float> &attr, float threshold){

        auto bufAttribute = attr.request();
        
        float *attribute = (float *) bufAttribute.ptr;
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        PixelType* imgOutput = new PixelType[n];

        AttributeFilters::filteringByPruningMax(this->tree, attribute, threshold, imgOutput);

        return PybindUtils::toNumpy(imgOutput, n);

    }

    py::array_t<int> filteringByPruningMin(std::vector<bool>& criterion){
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        PixelType* imgOutput = new PixelType[n];

        AttributeFilters::filteringByPruningMin(this->tree, criterion, imgOutput);

        return PybindUtils::toNumpy(imgOutput, n);
    }

    py::array_t<int> filteringByDirectRule(std::vector<bool>& criterion){
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        PixelType* imgOutput = new PixelType[n];

        AttributeFilters::filteringByDirectRule(this->tree, criterion, imgOutput);

        return PybindUtils::toNumpy(imgOutput, n);
    }

    py::array_t<int> filteringByPruningMax(std::vector<bool>& criterion){
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        PixelType* imgOutput = new PixelType[n];

        AttributeFilters::filteringByPruningMax(this->tree, criterion, imgOutput);

        return PybindUtils::toNumpy(imgOutput, n);

    }

    py::array_t<int> filteringBySubtractiveRule(std::vector<bool>& criterion){
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        PixelType* imgOutput = new PixelType[n];

        AttributeFilters::filteringBySubtractiveRule(this->tree, criterion, imgOutput);

        return PybindUtils::toNumpy(imgOutput, n);

    }

   /* py::array_t<float> filteringBySubtractiveScoreRuleNumpy(std::vector<float> prob){
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        float* imgOutput = new float[n];

        AttributeFilters::filteringBySubtractiveScoreRule(this->tree, prob, imgOutput);

        return PybindUtils::toNumpyFloat(imgOutput, n);

    }*/

    torch::Tensor filteringBySubtractiveScoreRule(torch::Tensor prob){
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        float* prt_prob = prob.data_ptr<float>();

        
        float* imgOutput = new float[n];
        AttributeFilters::filteringBySubtractiveScoreRule(this->tree, prt_prob, imgOutput);
        
        return PybindUtils::toTensor(imgOutput, n);
        
    }



};

#endif