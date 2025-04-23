
#include "../include/NodeMT.hpp"
#include "../include/MorphologicalTree.hpp"
#include "../include/AttributeComputedIncrementally.hpp"
#include "../include/Common.hpp"

#include <stack>
#include <vector>
#include <limits.h>



#ifndef ATTRIBUTE_FILTERS_H
#define ATTRIBUTE_FILTERS_H

#define UNDEF -999999999999

class AttributeFilters{
    protected:
        MorphologicalTreePtr tree;

    public:

    AttributeFilters(MorphologicalTreePtr tree);

    ~AttributeFilters();


    ImagePtr filteringByPruningMin(float* attr, float threshold);

    ImagePtr filteringByPruningMax(float* attr, float threshold);

    ImagePtr filteringByPruningMin(std::vector<bool>& criterion);

    ImagePtr filteringByPruningMax(std::vector<bool>& criterion);

    ImagePtr filteringByDirectRule(std::vector<bool>& criterion);

    ImagePtr filteringBySubtractiveRule(std::vector<bool>& criterion);

    float* filteringBySubtractiveScoreRule(float* prob);

    static void filteringBySubtractiveScoreRule(MorphologicalTreePtr tree, float* prob, float *imgOutput){
        std::unique_ptr<float[]> mapLevel(new float[tree->getNumNodes()]);
        
        //the root is always kept
        mapLevel[0] = tree->getRoot()->getLevel();

        for(NodeMTPtr node: tree->getIndexNode()){
            if(node->getParent() != nullptr){ 
                int residue = node->getResidue();
                if(node->isMaxtreeNode())
                    mapLevel[node->getIndex()] =  (float)mapLevel[node->getParent()->getIndex()] + (residue * prob[node->getIndex()]);
                else
                    mapLevel[node->getIndex()] = (float) mapLevel[node->getParent()->getIndex()] - (residue * prob[node->getIndex()]);
            }
        }
        for(NodeMTPtr node: tree->getIndexNode()){
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = mapLevel[node->getIndex()];
            }
        }
    }


    static void filteringBySubtractiveRule(MorphologicalTreePtr tree, std::vector<bool>& criterion, PixelType *imgOutput){
        std::unique_ptr<int[]> mapLevel(new int[tree->getNumNodes()]);
        //the root is always kept
        mapLevel[0] = tree->getRoot()->getLevel();

        for(NodeMTPtr node: tree->getIndexNode()){
            if(node->getParent() != nullptr){ 
                if(criterion[node->getIndex()]){
                    if(node->isMaxtreeNode())
                        mapLevel[node->getIndex()] = mapLevel[node->getParent()->getIndex()] + node->getResidue();
                    else
                        mapLevel[node->getIndex()] = mapLevel[node->getParent()->getIndex()] - node->getResidue();
                }
                else
                    mapLevel[node->getIndex()] = mapLevel[node->getParent()->getIndex()];
            }

        }
        for(NodeMTPtr node: tree->getIndexNode()){
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = mapLevel[node->getIndex()];
            }
        }
    }

    static void filteringByDirectRule(MorphologicalTreePtr tree, std::vector<bool>& criterion, PixelType *imgOutput){
        std::unique_ptr<int[]> mapLevel(new int[tree->getNumNodes()]);

        //the root is always kept
        mapLevel[0] = tree->getRoot()->getLevel();

        for(NodeMTPtr node: tree->getIndexNode()){
            if(node->getParent() != nullptr){ 
                if(criterion[node->getIndex()])
                    mapLevel[node->getIndex()] = node->getLevel();
                else
                    mapLevel[node->getIndex()] = mapLevel[node->getParent()->getIndex()];
            }

        }
        for(NodeMTPtr node: tree->getIndexNode()){
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = mapLevel[node->getIndex()];
            }
        }
        
    }

    static void filteringByPruningMin(MorphologicalTreePtr tree, std::vector<bool>& criterion, PixelType *imgOutput){
        std::stack<NodeMTPtr> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeMTPtr node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();;
            }
            for (NodeMTPtr child: node->getChildren()){
                if(criterion[child->getIndex()]){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] = child->getLevel();
                    }
                }
            }
        }
    }

    static void filteringByPruningMax(MorphologicalTreePtr tree, std::vector<bool>& _criterion, PixelType *imgOutput){
        
        std::unique_ptr<bool[]> criterion(new bool[tree->getNumNodes()]);
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&criterion, _criterion](NodeMTPtr node) -> void { //pre-processing
                if(!_criterion[node->getIndex()])
                    criterion[node->getIndex()] = true;
                else
                    criterion[node->getIndex()] = false;
            },
            [&criterion](NodeMTPtr parent, NodeMTPtr child) -> void { 
                criterion[parent->getIndex()] = (criterion[parent->getIndex()] & criterion[child->getIndex()]);
            },
            [](NodeMTPtr node) -> void { //post-processing
                                        
            }
        );

        std::stack<NodeMTPtr> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeMTPtr node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();
            }
            for (NodeMTPtr child: node->getChildren()){
                if(!criterion[child->getIndex()]){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] = child->getLevel();
                    }
                }
            }
        }
    }


    static void filteringByPruningMin(MorphologicalTreePtr tree, float *attribute, float threshold, PixelType *imgOutput){
        std::stack<NodeMTPtr> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeMTPtr node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();
            }
            for (NodeMTPtr child: node->getChildren()){
                if(attribute[child->getIndex()] > threshold){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] =  node->getLevel();
                    }
                }
                
            }
        }
    }

    static void filteringByPruningMax(MorphologicalTreePtr tree, float *attribute, float threshold, PixelType *imgOutput){
        
        std::unique_ptr<bool[]> criterion(new bool[tree->getNumNodes()]);
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&criterion, attribute, threshold](NodeMTPtr node) -> void { //pre-processing
                if(attribute[node->getIndex()] <= threshold)
                    criterion[node->getIndex()] = true;
                else
                    criterion[node->getIndex()] = false;
            },
            [&criterion, attribute, threshold](NodeMTPtr parent, NodeMTPtr child) -> void { 
                criterion[parent->getIndex()] = (criterion[parent->getIndex()] & criterion[child->getIndex()]);
            },
            [&criterion, attribute, threshold](NodeMTPtr node) -> void { //post-processing
                                        
            }
        );

        std::stack<NodeMTPtr> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeMTPtr node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();
            }
            for (NodeMTPtr child: node->getChildren()){
                if(!criterion[child->getIndex()]){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] =  node->getLevel();
                    }
                }
            }
        }
    }
};


#endif