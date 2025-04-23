
#include "include/NodeMT.hpp"
#include "include/AdjacencyRelation.hpp"
#include "include/Common.hpp"
#include "pybind/AttributeComputedIncrementallyPybind.hpp"
#include "pybind/MorphologicalTreePybind.hpp"
#include "pybind/AttributeFiltersPybind.hpp"
#include "pybind/ComputerDerivativesPybind.hpp"


#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/functional.h>
#include <torch/extension.h>

#include <iterator>
#include <utility>


namespace py = pybind11;
using namespace pybind11::literals;

void init_NodeMT(py::module &m){
    py::class_<NodeMT, std::shared_ptr<NodeMT>>(m, "NodeMT")
		.def(py::init<>())
		.def_property_readonly("id", &NodeMT::getIndex )
        .def("__str__", [](NodeMT &node) {
            std::ostringstream oss;
            oss << "NodeCT(id=" << node.getIndex() 
                << ", level=" << node.getLevel() 
                << ", numCNPs=" << node.getCNPs().size() 
                << ", area=" << node.getAreaCC(); 
            return oss.str();
        })
        .def("__repr__", [](NodeMT &node) { 
            std::ostringstream oss;
            oss << "NodeCT(id=" << node.getIndex() << ", level=" << node.getLevel() << ")";
            return oss.str();
        })
 		.def_property_readonly("cnps", &NodeMT::getCNPs )
		.def_property_readonly("level", &NodeMT::getLevel )
		.def_property_readonly("children", &NodeMT::getChildren )
		.def_property_readonly("parent", &NodeMT::getParent )
        .def_property_readonly("areaCC", &NodeMT::getAreaCC )
        .def_property_readonly("numDescendants", &NodeMT::getNumDescendants )
        .def_property_readonly("isMaxtree", &NodeMT::isMaxtreeNode )
        .def_property_readonly("numSiblings", &NodeMT::getNumSiblings )
        .def_property_readonly("residue", &NodeMT::getResidue ) 
        .def("pixelsOfCC",&NodeMT::getPixelsOfCC )
        .def("nodesOfPathToRoot",&NodeMT::getNodesOfPathToRoot )
        .def("nodesDescendants",&NodeMT::getNodesDescendants )
        .def("bfsTraversal", &NodeMT::getIteratorBreadthFirstTraversal)
        .def("postOrderTraversal", &NodeMT::getIteratorPostOrderTraversal)
        .def("recNode", [](NodeMTPtr node) {
            return MorphologicalTreePybind::recNode(node);
        });

        
}


void init_NodeMT_Iterators(py::module &m) {

    py::class_<typename NodeMT::IteratorPixelsOfCC>(m, "IteratorPixelsOfCC")
        .def(py::init<std::shared_ptr<NodeMT>, int>())
        .def("__iter__", [](typename NodeMT::IteratorPixelsOfCC &iter) {
            return py::make_iterator(iter.begin(), iter.end());
        }, py::keep_alive<0, 1>());


    py::class_<typename NodeMT::IteratorNodesOfPathToRoot>(m, "IteratorNodesOfPathToRoot")
        .def(py::init<std::shared_ptr<NodeMT>>())
        .def("__iter__", [](typename NodeMT::IteratorNodesOfPathToRoot &iter) {
            return py::make_iterator(iter.begin(), iter.end());
        }, py::keep_alive<0, 1>());

    py::class_<typename NodeMT::IteratorPostOrderTraversal>(m, "IteratorPostOrderTraversal")
        .def(py::init<std::shared_ptr<NodeMT>>())
        .def("__iter__", [](typename NodeMT::IteratorPostOrderTraversal &iter) {
            return py::make_iterator(iter.begin(), iter.end());
        }, py::keep_alive<0, 1>());

    py::class_<typename NodeMT::IteratorBreadthFirstTraversal>(m, "IteratorBreadthFirstTraversal")
        .def(py::init<std::shared_ptr<NodeMT>>())
        .def("__iter__", [](typename NodeMT::IteratorBreadthFirstTraversal &iter) {
            return py::make_iterator(iter.begin(), iter.end());
        }, py::keep_alive<0, 1>());

         
    py::class_<typename NodeMT::IteratorNodesDescendants>(m, "IteratorNodesDescendants")
    .def(py::init<std::shared_ptr<NodeMT>, int>())
    .def("__iter__", [](NodeMT::IteratorNodesDescendants &iter) {
        return py::make_iterator(iter.begin(), iter.end());
        }, py::keep_alive<0, 1>()); /* Keep vector alive while iterator is used */

}



void init_MorphologicalTree(py::module &m){
    py::class_<MorphologicalTreePybind, std::shared_ptr<MorphologicalTreePybind>>(m, "MorphologicalTree")
        .def(py::init<py::array_t<int>, int, int, bool, double>(),
            "input"_a, "rows"_a, "cols"_a, "isMaxtree"_a, "radius"_a = 1.5)
        .def(py::init<py::array_t<int>, int, int, std::string>(),
            "input"_a, "rows"_a, "cols"_a, "ToSInperpolation"_a = "self-dual")
        .def("reconstructionImage", &MorphologicalTreePybind::reconstructionImage )
        .def_property_readonly("numNodes", &MorphologicalTreePybind::getNumNodes )
        .def_property_readonly("listNodes", &MorphologicalTreePybind::getIndexNode )
        .def_property_readonly("root", &MorphologicalTreePybind::getRoot )
        .def_property_readonly("treeType", &MorphologicalTreePybind::getTreeType)
        .def_property_readonly("numRows", &MorphologicalTreePybind::getNumRowsOfImage )
        .def_property_readonly("numCols", &MorphologicalTreePybind::getNumColsOfImage )
        .def_property_readonly("depth", &MorphologicalTreePybind::getDepth )
        .def("getJacobianOfCNPs", &MorphologicalTreePybind::getJacobianOfCNPs)
        .def("getJacobianOfCCs", &MorphologicalTreePybind::getJacobianOfCCs)
        .def("getResidues", &MorphologicalTreePybind::getResidues)
        .def("getAltitudes", &MorphologicalTreePybind::getAltitudes)
        .def("getSC", &MorphologicalTreePybind::getSC );
}


void init_AttributeComputedIncrementally(py::module &m){
    	py::class_<AttributeComputedIncrementallyPybind>(m, "Attribute")
        .def_static("computerAttribute", static_cast<void(*)(NodeMTPtr, 
                                                             std::function<void(NodeMTPtr)>, 
                                                             std::function<void(NodeMTPtr, NodeMTPtr)>, 
                                                             std::function<void(NodeMTPtr)>)>(&AttributeComputedIncrementally::computerAttribute))
        .def_static("computerBasicAttributes",py::overload_cast<MorphologicalTreePybindPtr>(&AttributeComputedIncrementallyPybind::computerBasicAttributes))
        .def_static("computerBasicAttributes",py::overload_cast<MorphologicalTreePybindPtr, int, std::string>(&AttributeComputedIncrementallyPybind::computerBasicAttributes))
        .def_static("computerArea", &AttributeComputedIncrementallyPybind::computerArea);
}

void init_AttributeFilters(py::module &m){
    py::class_<AttributeFiltersPybind>(m, "AttributeFilters")
    .def(py::init<MorphologicalTreePybindPtr>())
    .def("filteringMin", py::overload_cast<py::array_t<float> &, float>(&AttributeFiltersPybind::filteringByPruningMin))
    .def("filteringMin", py::overload_cast<std::vector<bool>&>(&AttributeFiltersPybind::filteringByPruningMin))
    .def("filteringMax", py::overload_cast<std::vector<bool>&>(&AttributeFiltersPybind::filteringByPruningMax))
    .def("filteringDirectRule", py::overload_cast<std::vector<bool>&>(&AttributeFiltersPybind::filteringByDirectRule))
    .def("filteringSubtractiveRule", py::overload_cast<std::vector<bool>&>(&AttributeFiltersPybind::filteringBySubtractiveRule))
    .def("filteringSubtractiveScoreRule", py::overload_cast<torch::Tensor>(&AttributeFiltersPybind::filteringBySubtractiveScoreRule))
    .def("filteringMax", py::overload_cast<py::array_t<float> &, float>(&AttributeFiltersPybind::filteringByPruningMax));

}


void init_AdjacencyRelation(py::module &m){
    	py::class_<AdjacencyRelation>(m, "AdjacencyRelation")
        .def(py::init<int, int, double>())
        .def_property_readonly("size", &AdjacencyRelation::getSize )
        .def("getAdjPixels", py::overload_cast<int, int>( &AdjacencyRelation::getAdjPixels ));
}

void init_ComputerDerivatives(py::module &m){
    	py::class_<ComputerDerivativesPybind>(m, "ComputerDerivatives")
        .def_static("gradients", &ComputerDerivativesPybind::computerGradientsWithTree)
        .def_static("gradientsWithJacobian", &ComputerDerivativesPybind::computerGradientsWithJacobian);
        //.def_static("gradientsWeightsAndBias", &ComputerDerivativesPybind::gradientsWeightsAndBias)
        //.def_static("gradients_numpy", &ComputerDerivativesPybind::gradients_numpy);

}


PYBIND11_MODULE(ctreelearn, m) {
    // Optional docstring
    m.doc() = "A simple library for learning of connected filters based on component trees";
    
    init_NodeMT(m);
    init_NodeMT_Iterators(m);
    init_MorphologicalTree(m);
    init_AttributeComputedIncrementally(m);
    init_AttributeFilters(m);
    init_AdjacencyRelation(m);
    init_ComputerDerivatives(m);

    
}
