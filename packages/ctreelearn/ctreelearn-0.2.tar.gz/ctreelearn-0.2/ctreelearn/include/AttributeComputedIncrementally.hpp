

#ifndef ATTRIBUTE_COMPUTED_INCREMENTALLY_H
#define ATTRIBUTE_COMPUTED_INCREMENTALLY_H

#include "../include/NodeMT.hpp"
#include "../include/MorphologicalTree.hpp"
#include <algorithm>
#include <cmath>
#include <iostream>
#include <limits> // Para usar std::numeric_limits<float>::epsilon()
#include <unordered_map>
#include <functional>
#include <string>

#define PI 3.14159265358979323846


class PathAscendantsAndDescendants{
	private:
	MorphologicalTreePtr tree;
	std::vector<NodeMTPtr> ascendants;
	std::vector<NodeMTPtr> descendants;

	public:
	PathAscendantsAndDescendants(MorphologicalTreePtr tree): tree(tree){
	}

    NodeMTPtr getNodeAscendantBasedOnHierarchical(NodeMTPtr node, int h){
		NodeMTPtr n = node;
		int i=0;
		while(i++ < h){
			n = n->getParent();
			if(n == nullptr)
				return n;
		}
		return n;
	}


	void maxAreaDescendants(NodeMTPtr nodeAsc, NodeMTPtr nodeDes){
		if(descendants[nodeAsc->getIndex()] == nullptr)
			descendants[nodeAsc->getIndex()] = nodeDes;
		
		if(descendants[nodeAsc->getIndex()]->getAreaCC() < nodeDes->getAreaCC())
			descendants[nodeAsc->getIndex()] = nodeDes;
		
	}

	void computerAscendantsAndDescendants(int delta){
		std::vector<NodeMTPtr> tmp_asc (this->tree->getNumNodes(), nullptr);
		this->ascendants = tmp_asc;

		std::vector<NodeMTPtr> tmp_des (this->tree->getNumNodes(), nullptr);
		this->descendants = tmp_des;
		
		for(NodeMTPtr node: tree->getIndexNode()){
			NodeMTPtr nodeAsc = this->getNodeAscendantBasedOnHierarchical(node, delta);
			if(nodeAsc == nullptr) continue;
			this->maxAreaDescendants(nodeAsc, node);
			if(descendants[nodeAsc->getIndex()] != nullptr){
				ascendants[node->getIndex()] = nodeAsc;
			}
		}
	}
	std::vector<NodeMTPtr> getAscendants(){
		return this->ascendants;
	}

	std::vector<NodeMTPtr> getDescendants(){
		return this->descendants;
	}
};


class AttributeNames {
	public:
		
		std::unordered_map<std::string, int> mapIndexes;
		const int NUM_ATTRIBUTES;
	
		// Construtor genérico 
		AttributeNames(std::unordered_map<std::string, int>&& map)
			: mapIndexes(std::move(map)), NUM_ATTRIBUTES(mapIndexes.size()) {}
	
		
		static AttributeNames geometric(int n, int delta) {
		
			int offset = 0;
			std::unordered_map<std::string, int> mapIndexes;
			for (int d = -delta; d <= delta; ++d) {
				std::string suffix;
				if (d < 0) {
					suffix = "_Asc" + std::to_string(-d); 
				} else if (d > 0) {
					suffix = "_Desc" + std::to_string(d);
				}
				
				// Adiciona sufixo e incrementa o offset para cada delta
				mapIndexes["AREA" + suffix] = offset + 0 * n;
				mapIndexes["VOLUME" + suffix] = offset + 1 * n;
				mapIndexes["LEVEL" + suffix] = offset + 2 * n;
				mapIndexes["MEAN_LEVEL" + suffix] = offset + 3 * n;
				mapIndexes["VARIANCE_LEVEL" + suffix] = offset + 4 * n;
				mapIndexes["STANDARD_DEVIATION" + suffix] = offset + 5 * n;
				mapIndexes["BOX_WIDTH" + suffix] = offset + 6 * n;
				mapIndexes["BOX_HEIGHT" + suffix] = offset + 7 * n;
				mapIndexes["RECTANGULARITY" + suffix] = offset + 8 * n;
				mapIndexes["RATIO_WH" + suffix] = offset + 9 * n;
				mapIndexes["CENTRAL_MOMENT_20" + suffix] = offset + 10 * n;
				mapIndexes["CENTRAL_MOMENT_02" + suffix] = offset + 11 * n;
				mapIndexes["CENTRAL_MOMENT_11" + suffix] = offset + 12 * n;
				mapIndexes["CENTRAL_MOMENT_30" + suffix] = offset + 13 * n;
				mapIndexes["CENTRAL_MOMENT_03" + suffix] = offset + 14 * n;
				mapIndexes["CENTRAL_MOMENT_21" + suffix] = offset + 15 * n;
				mapIndexes["CENTRAL_MOMENT_12" + suffix] = offset + 16 * n;
				mapIndexes["ORIENTATION" + suffix] = offset + 17 * n;
				mapIndexes["LENGTH_MAJOR_AXIS" + suffix] = offset + 18 * n;
				mapIndexes["LENGTH_MINOR_AXIS" + suffix] = offset + 19 * n;
				mapIndexes["ECCENTRICITY" + suffix] = offset + 20 * n;
				mapIndexes["COMPACTNESS" + suffix] = offset + 21 * n;
				mapIndexes["HU_MOMENT_1_INERTIA" + suffix] = offset + 22 * n;
				mapIndexes["HU_MOMENT_2" + suffix] = offset + 23 * n;
				mapIndexes["HU_MOMENT_3" + suffix] = offset + 24 * n;
				mapIndexes["HU_MOMENT_4" + suffix] = offset + 25 * n;
				mapIndexes["HU_MOMENT_5" + suffix] = offset + 26 * n;
				mapIndexes["HU_MOMENT_6" + suffix] = offset + 27 * n;
				mapIndexes["HU_MOMENT_7" + suffix] = offset + 28 * n;

				offset += 29 * n;  // Incrementa para o próximo conjunto de atributos com delta
			}
			return AttributeNames(std::move(mapIndexes));
		}

		static AttributeNames geometric(int n) {
			return AttributeNames( {
				{"AREA", 0 * n},
				{"VOLUME", 1 * n},
				{"LEVEL", 2 * n},
				{"MEAN_LEVEL", 3 * n},
				{"VARIANCE_LEVEL", 4 * n},
				{"STANDARD_DEVIATION", 5 * n},
				{"BOX_WIDTH", 6 * n},
				{"BOX_HEIGHT", 7 * n},
				{"RECTANGULARITY", 8 * n},
				{"RATIO_WH", 9 * n},
				{"CENTRAL_MOMENT_20", 10 * n},
				{"CENTRAL_MOMENT_02", 11 * n},
				{"CENTRAL_MOMENT_11", 12 * n},
				{"CENTRAL_MOMENT_30", 13 * n},
				{"CENTRAL_MOMENT_03", 14 * n},
				{"CENTRAL_MOMENT_21", 15 * n},
				{"CENTRAL_MOMENT_12", 16 * n},
				{"ORIENTATION", 17 * n},
				{"LENGTH_MAJOR_AXIS", 18 * n},
				{"LENGTH_MINOR_AXIS", 19 * n},
				{"ECCENTRICITY", 20 * n},
				{"COMPACTNESS", 21 * n},
				{"HU_MOMENT_1_INERTIA", 22 * n},
				{"HU_MOMENT_2", 23 * n},
				{"HU_MOMENT_3", 24 * n},
				{"HU_MOMENT_4", 25 * n},
				{"HU_MOMENT_5", 26 * n},
				{"HU_MOMENT_6", 27 * n},
				{"HU_MOMENT_7", 28 * n}
			});
		}
		static AttributeNames structural(int n) {
			return AttributeNames( {
				{"HEIGHT", 0 * n}, 
				{"DEPTH", 1 * n}, 
				{"IS_LEAF", 2 * n}, 
				{"IS_ROOT", 3 * n},
				{"NUM_CHILDREN", 4 * n}, 
				{"NUM_SIBLINGS", 5 * n}, 
				{"NUM_DESCENDANTS", 6 * n},
				{"NUM_LEAF_DESCENDANTS", 7 * n},
				 {"LEAF_RATIO", 8 * n}, 
				 {"BALANCE", 9 * n},
				{"AVG_CHILD_HEIGHT", 10 * n}
			});
		}
	
	
	};
	
/*
class AttributeNames {
public:
    std::unordered_map<std::string, int> mapIndexes;
    const int NUM_ATTRIBUTES;

    // Construtor para atributos básicos
    AttributeNames(int n) : NUM_ATTRIBUTES(29) {
        mapIndexes = {
            {"AREA", 0 * n},
            {"VOLUME", 1 * n},
            {"LEVEL", 2 * n},
            {"MEAN_LEVEL", 3 * n},
            {"VARIANCE_LEVEL", 4 * n},
            {"STANDARD_DEVIATION", 5 * n},
            {"BOX_WIDTH", 6 * n},
            {"BOX_HEIGHT", 7 * n},
            {"RECTANGULARITY", 8 * n},
            {"RATIO_WH", 9 * n},
            {"CENTRAL_MOMENT_20", 10 * n},
            {"CENTRAL_MOMENT_02", 11 * n},
            {"CENTRAL_MOMENT_11", 12 * n},
            {"CENTRAL_MOMENT_30", 13 * n},
            {"CENTRAL_MOMENT_03", 14 * n},
            {"CENTRAL_MOMENT_21", 15 * n},
            {"CENTRAL_MOMENT_12", 16 * n},
            {"ORIENTATION", 17 * n},
            {"LENGTH_MAJOR_AXIS", 18 * n},
            {"LENGTH_MINOR_AXIS", 19 * n},
            {"ECCENTRICITY", 20 * n},
            {"COMPACTNESS", 21 * n},
            {"HU_MOMENT_1_INERTIA", 22 * n},
            {"HU_MOMENT_2", 23 * n},
            {"HU_MOMENT_3", 24 * n},
            {"HU_MOMENT_4", 25 * n},
            {"HU_MOMENT_5", 26 * n},
            {"HU_MOMENT_6", 27 * n},
            {"HU_MOMENT_7", 28 * n}
        };
    }

    // Construtor para atributos com sufixos
    AttributeNames(int n, int delta) : NUM_ATTRIBUTES(29 * (2 * delta + 1)) { 
        int offset = 0;

        for (int d = -delta; d <= delta; ++d) {
            std::string suffix;
            if (d < 0) {
                suffix = "_Asc" + std::to_string(-d); 
            } else if (d > 0) {
                suffix = "_Desc" + std::to_string(d);
            }

            // Adiciona sufixo e incrementa o offset para cada delta
            mapIndexes["AREA" + suffix] = offset + 0 * n;
            mapIndexes["VOLUME" + suffix] = offset + 1 * n;
            mapIndexes["LEVEL" + suffix] = offset + 2 * n;
            mapIndexes["MEAN_LEVEL" + suffix] = offset + 3 * n;
            mapIndexes["VARIANCE_LEVEL" + suffix] = offset + 4 * n;
            mapIndexes["STANDARD_DEVIATION" + suffix] = offset + 5 * n;
            mapIndexes["BOX_WIDTH" + suffix] = offset + 6 * n;
            mapIndexes["BOX_HEIGHT" + suffix] = offset + 7 * n;
            mapIndexes["RECTANGULARITY" + suffix] = offset + 8 * n;
            mapIndexes["RATIO_WH" + suffix] = offset + 9 * n;
            mapIndexes["CENTRAL_MOMENT_20" + suffix] = offset + 10 * n;
            mapIndexes["CENTRAL_MOMENT_02" + suffix] = offset + 11 * n;
            mapIndexes["CENTRAL_MOMENT_11" + suffix] = offset + 12 * n;
            mapIndexes["CENTRAL_MOMENT_30" + suffix] = offset + 13 * n;
            mapIndexes["CENTRAL_MOMENT_03" + suffix] = offset + 14 * n;
            mapIndexes["CENTRAL_MOMENT_21" + suffix] = offset + 15 * n;
            mapIndexes["CENTRAL_MOMENT_12" + suffix] = offset + 16 * n;
            mapIndexes["ORIENTATION" + suffix] = offset + 17 * n;
            mapIndexes["LENGTH_MAJOR_AXIS" + suffix] = offset + 18 * n;
            mapIndexes["LENGTH_MINOR_AXIS" + suffix] = offset + 19 * n;
            mapIndexes["ECCENTRICITY" + suffix] = offset + 20 * n;
            mapIndexes["COMPACTNESS" + suffix] = offset + 21 * n;
            mapIndexes["HU_MOMENT_1_INERTIA" + suffix] = offset + 22 * n;
            mapIndexes["HU_MOMENT_2" + suffix] = offset + 23 * n;
            mapIndexes["HU_MOMENT_3" + suffix] = offset + 24 * n;
            mapIndexes["HU_MOMENT_4" + suffix] = offset + 25 * n;
            mapIndexes["HU_MOMENT_5" + suffix] = offset + 26 * n;
            mapIndexes["HU_MOMENT_6" + suffix] = offset + 27 * n;
            mapIndexes["HU_MOMENT_7" + suffix] = offset + 28 * n;

            offset += 29 * n;  // Incrementa para o próximo conjunto de atributos com delta
        }
    }
};
*/



class AttributeComputedIncrementally{

public:

 
    virtual void preProcessing(NodeMTPtr v);

    virtual void mergeChildren(NodeMTPtr parent, NodeMTPtr child);

    virtual void postProcessing(NodeMTPtr parent);

    void computerAttribute(NodeMTPtr root);

	static void computerAttribute(NodeMTPtr root, 
										std::function<void(NodeMTPtr)> preProcessing,
										std::function<void(NodeMTPtr, NodeMTPtr)> mergeChildren,
										std::function<void(NodeMTPtr)> postProcessing ){
		
		preProcessing(root);
			
		for(NodeMTPtr child: root->getChildren()){
			AttributeComputedIncrementally::computerAttribute(child, preProcessing, mergeChildren, postProcessing);
			mergeChildren(root, child);
		}

		postProcessing(root);
	}

	static float* computerAttributeByIndex(MorphologicalTreePtr tree, std::string attrName){
		const int n = tree->getNumNodes();
		float *attr = new float[n];
		auto [attributeNames, ptrValues] = AttributeComputedIncrementally::computerBasicAttributes(tree);
		int index = attributeNames.mapIndexes[attrName];
		for(int i = 0; i < n; i++){
			attr[i] = ptrValues[i + index];
		}
		delete[] ptrValues;
		return attr;
	}
	

	static float* computerStructTreeAttributes(MorphologicalTreePtr tree){
		const int numAttribute = 11;
		const int n = tree->getNumNodes();
		float *attrs = new float[n * numAttribute];
	
		AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
			[&](NodeMTPtr node) {
				int idx = node->getIndex();
				int parentDepth = node->getParent() ? attrs[node->getParent()->getIndex() * numAttribute + 1] : 0;
	
				attrs[idx * numAttribute + 0] = 0.0f; // altura
				attrs[idx * numAttribute + 1] = node->getParent() ? parentDepth + 1 : 0; // profundidade
				attrs[idx * numAttribute + 2] = node->getChildren().empty() ? 1.0f : 0.0f; // é folha
				attrs[idx * numAttribute + 3] = node->getParent() == nullptr ? 1.0f : 0.0f; // é raiz
				attrs[idx * numAttribute + 4] = node->getChildren().size(); // número de filhos
				attrs[idx * numAttribute + 5] = node->getParent() ? node->getParent()->getChildren().size() - 1 : 0; // irmãos
				attrs[idx * numAttribute + 6] = 0.0f; // número de descendentes
				attrs[idx * numAttribute + 7] = attrs[idx * numAttribute + 2]; // folhas descendentes
				attrs[idx * numAttribute + 8] = 0.0f; // razão folhas/desc
				attrs[idx * numAttribute + 9] = 0.0f; // balanceamento
				attrs[idx * numAttribute + 10] = 0.0f; // média altura filhos
			},
			[&](NodeMTPtr parent, NodeMTPtr child) {
				int pIdx = parent->getIndex();
				int cIdx = child->getIndex();
	
				// atualiza descendentes e folhas
				attrs[pIdx * numAttribute + 6] += attrs[cIdx * numAttribute + 6] + 1;
				attrs[pIdx * numAttribute + 7] += attrs[cIdx * numAttribute + 7];
	
				// altura (máxima entre os filhos)
				float childHeight = attrs[cIdx * numAttribute + 0];
				attrs[pIdx * numAttribute + 0] = std::max(
					attrs[pIdx * numAttribute + 0],
					childHeight + 1
				);
	
				// acumulando estatísticas para balanceamento
				float& minH = attrs[pIdx * numAttribute + 9]; // usamos como min na primeira iteração
				float& sumH = attrs[pIdx * numAttribute + 10];
				int numChildren = parent->getChildren().size();
	
				if (numChildren == 1) {
					minH = childHeight;
					sumH = childHeight;
				} else {
					minH = std::min(minH, childHeight);
					sumH += childHeight;
				}
			},
			[&](NodeMTPtr node) {
				int idx = node->getIndex();
				float numDesc = attrs[idx * numAttribute + 6];
				float numFolhas = attrs[idx * numAttribute + 7];
	
				// Razão folhas / descendentes
				attrs[idx * numAttribute + 8] = numDesc > 0.0f ? numFolhas / (numDesc + 1.0f) : 1.0f;
	
				// Balanceamento
				if (!node->getChildren().empty()) {
					float alturaMax = attrs[idx * numAttribute + 0];
					float alturaMin = attrs[idx * numAttribute + 9]; // usamos campo 9 como min durante o merge
					attrs[idx * numAttribute + 9] = alturaMax - alturaMin;
					
					// Média da altura dos filhos
					attrs[idx * numAttribute + 10] = attrs[idx * numAttribute + 10] / node->getChildren().size();
				}
			}
		);
	
		return attrs;
	}

	static std::pair<AttributeNames, float*> computerBasicAttributes(MorphologicalTreePtr tree, int delta) {
		return computerBasicAttributes(tree, delta, "zero-padding");
	}

	
	static std::pair<AttributeNames, float*> computerBasicAttributes(MorphologicalTreePtr tree, int delta, std::string padding) {
		/*
		Valores de padding:
		 - zero-padding: preenchimento com zero
		 - same-padding: preenchimento com o valor do node referencia
		 - last-padding: preenchimento com o ultimo valor valido
		 - null: preenchimento com 0 todo os nos do caminho
		*/

		auto [attributeNames, attrs] = AttributeComputedIncrementally::computerBasicAttributes(tree);
		std::unordered_map<std::string, int> ATTR = attributeNames.mapIndexes;

		int n = tree->getNumNodes();
		AttributeNames attributeNamesDelta = AttributeNames::geometric(n, delta);  
		
		float *attrsDelta = new float[n * attributeNamesDelta.NUM_ATTRIBUTES];
		std::unordered_map<std::string, int> ATTR_DELTA = attributeNamesDelta.mapIndexes;

		std::fill(attrsDelta, attrsDelta + n * attributeNamesDelta.NUM_ATTRIBUTES, 0);
		
		PathAscendantsAndDescendants pathAscDesc(tree);
		std::vector<NodeMTPtr> ascendants;
		std::vector<NodeMTPtr> descendants;

		for (int d = 0; d <= delta; d++) {
			if (d > 0) {
				pathAscDesc.computerAscendantsAndDescendants(d);
				ascendants = pathAscDesc.getAscendants();
				descendants = pathAscDesc.getDescendants();
			}

			for (const auto& pair : attributeNames.mapIndexes) {
				const std::string& attrName = pair.first;

				for (NodeMTPtr node : tree->getIndexNode()) {
					int nodeIndex = node->getIndex();

					if (d == 0) {
						if (ATTR.count(attrName) && ATTR_DELTA.count(attrName)) {
							attrsDelta[nodeIndex + ATTR_DELTA[attrName]] = attrs[nodeIndex + ATTR[attrName]];
						}
					} else {
						const std::string attrNameAsc = attrName + "_Asc" + std::to_string(d);
						int ascIndex = ascendants[nodeIndex] ? ascendants[nodeIndex]->getIndex() : nodeIndex;
						if(ascIndex != nodeIndex)
							attrsDelta[nodeIndex + ATTR_DELTA[attrNameAsc]] = attrs[ascIndex + ATTR[attrName]];

						const std::string attrNameDesc = attrName + "_Desc" + std::to_string(d);
						int descIndex = descendants[nodeIndex] ? descendants[nodeIndex]->getIndex() : nodeIndex;
						if(descIndex != nodeIndex)
							attrsDelta[nodeIndex + ATTR_DELTA[attrNameDesc]] = attrs[descIndex + ATTR[attrName]];
					}
				}
			}
		}

		if (padding != "zero-padding") {
			for (const auto& pair : attributeNamesDelta.mapIndexes) {
				const std::string& attrName = pair.first;
				if (!ATTR.count(attrName) || !ATTR_DELTA.count(attrName)) {
					continue;  // Pular o atributo se não estiver em ambos os mapas
				}
				for (NodeMTPtr node : tree->getIndexNode()) {
					int nodeIndex = node->getIndex();

					// **Padding para atributos ascendentes**
					for (int d = 1; d <= delta; d++) {
						const std::string attrNameAsc = attrName + "_Asc" + std::to_string(d);
						const std::string refAttrAsc = (d == 1) ? attrName : attrName + "_Asc" + std::to_string(d - 1);

						// Se o valor atual for 0, aplica o padding conforme a estratégia
						if (attrsDelta[nodeIndex + ATTR_DELTA[attrNameAsc]] == 0) {
							if (padding == "last-padding") {
								// Usa o último valor válido para o padding
								attrsDelta[nodeIndex + ATTR_DELTA[attrNameAsc]] = attrsDelta[nodeIndex + ATTR_DELTA[refAttrAsc]];
							} else if (padding == "same-padding") {
								// Usa o valor do próprio node como referência
								attrsDelta[nodeIndex + ATTR_DELTA[attrNameAsc]] = attrs[nodeIndex + ATTR[attrName]];
							} else if (padding == "null-padding") {
								// Define como zero no próprio nó e em todos os ancestrais até delta
								for (int k = 0; k <= d; k++) {
									const std::string attrNameAsc_k = (k == 0) ? attrName : attrName + "_Asc" + std::to_string(k);
									attrsDelta[nodeIndex + ATTR_DELTA[attrNameAsc_k]] = 0;
								}
								
								const std::string attrNameDesc = attrName + "_Desc" + std::to_string(d);
								const std::string refAttrDesc = (d == 1) ? attrName : attrName + "_Desc" + std::to_string(d - 1);
								for (int k = 0; k <= d; k++) {
									const std::string attrNameDesc_k = (k == 0) ? attrName : attrName + "_Desc" + std::to_string(k);
									attrsDelta[nodeIndex + ATTR_DELTA[attrNameDesc_k]] = 0;
								}
							}
						}
					}

					// **Padding para atributos descendentes**
					for (int d = 1; d <= delta; d++) {
						const std::string attrNameDesc = attrName + "_Desc" + std::to_string(d);
						const std::string refAttrDesc = (d == 1) ? attrName : attrName + "_Desc" + std::to_string(d - 1);

						// Se o valor atual for 0, aplica o padding conforme a estratégia
						if (node->isLeaf() || attrsDelta[nodeIndex + ATTR_DELTA[attrNameDesc]] == 0) {
							if (padding == "last-padding") {
								attrsDelta[nodeIndex + ATTR_DELTA[attrNameDesc]] = attrsDelta[nodeIndex + ATTR_DELTA[refAttrDesc]];
							} else if (padding == "same-padding") {
								attrsDelta[nodeIndex + ATTR_DELTA[attrNameDesc]] = attrs[nodeIndex + ATTR[attrName]];
							} 
						}
						if(attrsDelta[nodeIndex + ATTR_DELTA[attrNameDesc]] == 0){
							if (padding == "null-padding") {
								// Define como zero no próprio nó e em todos os descendentes até delta
								for (int k = 0; k <= d; k++) {
									const std::string attrNameDesc_k = (k == 0) ? attrName : attrName + "_Desc" + std::to_string(k);
									attrsDelta[nodeIndex + ATTR_DELTA[attrNameDesc_k]] = 0;
								}	

								const std::string attrNameAsc = attrName + "_Asc" + std::to_string(d);
								const std::string refAttrAsc = (d == 1) ? attrName : attrName + "_Asc" + std::to_string(d - 1);
								for (int k = 0; k <= d; k++) {
									const std::string attrNameAsc_k = (k == 0) ? attrName : attrName + "_Asc" + std::to_string(k);
									attrsDelta[nodeIndex + ATTR_DELTA[attrNameAsc_k]] = 0;
								}						
							}
						}
					}
				}
			}


		}


		delete[] attrs;
		return std::make_pair(attributeNamesDelta, attrsDelta);
	}



	static std::pair<AttributeNames, float*> computerBasicAttributes(MorphologicalTreePtr tree){
	    
		/*
		0 - area
		1 - volume
		2 - level
		3 - mean level
		4 - variance level
		5 - standard deviation
		6 - Box width
		7 - Box height
		8 - rectangularity
		9 - ratio (Box width, Box height)
		
		10 - momentos centrais 20
		11 - momentos centrais 02
		12 - momentos centrais 11
		13 - momentos centrais 30
		14 - momentos centrais 03
		15 - momentos centrais 21
		16 - momentos centrais 12
		17 - orientation
		18 - lenght major axis
		19 - lenght minor axis
		20 - eccentricity = alongation
		21 - compactness = circularity
		22 - momentos de Hu 1 => inertia
		23 - momentos de Hu 2
		24 - momentos de Hu 3
		25 - momentos de Hu 4
		26 - momentos de Hu 5
		27 - momentos de Hu 6
		28 - momentos de Hu 7
		*/
		int n = tree->getNumNodes();
		AttributeNames attributeNames = AttributeNames::geometric(n);
		
		float *attrs = new float[n * attributeNames.NUM_ATTRIBUTES];
		std::unordered_map<std::string, int> ATTR = attributeNames.mapIndexes;
		

		std::unique_ptr<int[]> xmax(new int[n]);
		std::unique_ptr<int[]> ymax(new int[n]);
		std::unique_ptr<int[]> xmin(new int[n]);
		std::unique_ptr<int[]> ymin(new int[n]);
		
		//momentos geometricos para calcular o centroide
		std::unique_ptr<long int[]> sumX(new long int[n]);
		std::unique_ptr<long int[]> sumY(new long int[n]);
		std::unique_ptr<long int[]> sumGrayLevelSquare(new long int[n]);
		
		int numCols = tree->getNumColsOfImage();
		int numRows = tree->getNumRowsOfImage();
		

		//computação dos atributos: area, volume, gray level, mean of gray level, variance of gray level, standard deviation gray level, Box width, Box height, rectangularity, ratio (Box width, Box height) e momentos geometricos 
	    AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
						[&ATTR, &attrs, n,  &xmax, &ymax, &xmin, &ymin, &sumX, &sumY, &sumGrayLevelSquare, numCols, numRows](NodeMTPtr node) -> void {
							attrs[node->getIndex() + ATTR["AREA"]  ] = node->getCNPs().size(); //area
							attrs[node->getIndex() + ATTR["VOLUME"]] = node->getCNPs().size() * node->getLevel(); //volume =>  \sum{ f }
							attrs[node->getIndex() + ATTR["LEVEL"] ] = node->getLevel(); //level

							xmax[node->getIndex()] = 0;
							ymax[node->getIndex()] = 0;
							xmin[node->getIndex()] = numCols;
							ymin[node->getIndex()] = numRows;
							sumX[node->getIndex()] = 0;
							sumY[node->getIndex()] = 0;
							sumGrayLevelSquare[node->getIndex()] = std::pow(node->getLevel(), 2) * node->getCNPs().size(); //computando: \sum{ f^2 }
							for(int p: node->getCNPs()) {
								int x = p % numCols;
								int y = p / numCols;
								xmin[node->getIndex()] = std::min(xmin[node->getIndex()], x);
								ymin[node->getIndex()] = std::min(ymin[node->getIndex()], y);
								xmax[node->getIndex()] = std::max(xmax[node->getIndex()], x);
								ymax[node->getIndex()] = std::max(ymax[node->getIndex()], y);

								sumX[node->getIndex()] += x;
								sumY[node->getIndex()] += y;
							}
						},
						[&ATTR, &attrs, n, &xmax, &ymax, &xmin, &ymin, &sumX, &sumY, &sumGrayLevelSquare](NodeMTPtr parent, NodeMTPtr child) -> void {
							attrs[parent->getIndex() + ATTR["AREA"]  ] += attrs[child->getIndex()]; //area
							attrs[parent->getIndex() + ATTR["VOLUME"]] += attrs[child->getIndex() + n]; //volume
							
							sumGrayLevelSquare[parent->getIndex()] += sumGrayLevelSquare[child->getIndex()]; //computando: \sum{ f^2 }

							ymax[parent->getIndex()] = std::max(ymax[parent->getIndex()], ymax[child->getIndex()]);
							xmax[parent->getIndex()] = std::max(xmax[parent->getIndex()], xmax[child->getIndex()]);
							ymin[parent->getIndex()] = std::min(ymin[parent->getIndex()], ymin[child->getIndex()]);
							xmin[parent->getIndex()] = std::min(xmin[parent->getIndex()], xmin[child->getIndex()]);
		
							sumX[parent->getIndex()] += sumX[child->getIndex()];
							sumY[parent->getIndex()] += sumY[child->getIndex()];
							
						},
						[&ATTR, &attrs, n, &xmax, &ymax, &xmin, &ymin, &sumGrayLevelSquare](NodeMTPtr node) -> void {
							
							float area = attrs[node->getIndex() + ATTR["AREA"]];
							float volume = attrs[node->getIndex() + ATTR["VOLUME"]]; 
							float width = xmax[node->getIndex()] - xmin[node->getIndex()] + 1;	
							float height = ymax[node->getIndex()] - ymin[node->getIndex()] + 1;	
							
							float meanGrayLevel = volume / area; //mean graylevel - // E(f)
							double meanGrayLevelSquare = sumGrayLevelSquare[node->getIndex()] / area; // E(f^2)
							float var = meanGrayLevelSquare - (meanGrayLevel * meanGrayLevel); //variance: E(f^2) - E(f)^2
							attrs[node->getIndex() + ATTR["VARIANCE_LEVEL"] ] = var > 0? var : 0; //variance
							
							if (attrs[node->getIndex() + ATTR["VARIANCE_LEVEL"]] >= 0) {
								attrs[node->getIndex() + ATTR["STANDARD_DEVIATION"]] = std::sqrt(attrs[node->getIndex() + ATTR["VARIANCE_LEVEL"]]); // desvio padrão do graylevel
							} else {
								attrs[node->getIndex() + ATTR["STANDARD_DEVIATION"]] = 0.0; // Se a variância for negativa, definir desvio padrão como 0
							}
							
							attrs[node->getIndex() + ATTR["MEAN_LEVEL"] ] = meanGrayLevel;
							attrs[node->getIndex() + ATTR["BOX_WIDTH"] ] = width;
							attrs[node->getIndex() + ATTR["BOX_HEIGHT"] ] = height;
							attrs[node->getIndex() + ATTR["RECTANGULARITY"] ] = area / (width * height);
							attrs[node->getIndex() + ATTR["RATIO_WH"] ] = std::max(width, height) / std::min(width, height);
		});

		

		//Computação dos momentos centrais e momentos de Hu
		AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
			[&ATTR, &attrs, n,  &sumX, &sumY, numCols](NodeMTPtr node) -> void {				
				attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_20"]] = 0; // momento central 20
				attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_02"]] = 0; // momento central 02
				attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_11"]] = 0; // momento central 11
				attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_30"]] = 0; // momento central 30
				attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_03"]] = 0; // momento central 03
				attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_21"]] = 0; // momento central 21
				attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_12"]] = 0; // momento central 12

				float xCentroid = sumX[node->getIndex()] / attrs[node->getIndex() + ATTR["AREA"]];
				float yCentroid = sumY[node->getIndex()] / attrs[node->getIndex() + ATTR["AREA"]];		
				for(int p: node->getCNPs()) {
					int x = p % numCols;
					int y = p / numCols;
					float dx = x - xCentroid;
            		float dy = y - yCentroid;
					
					// Momentos centrais de segunda ordem
					attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_20"] ] += std::pow(dx, 2);
					attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_02"] ] += std::pow(dy, 2);
					attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_11"] ] += dx * dy;
	
					// Momentos centrais de terceira ordem
					attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_30"]] += std::pow(dx, 3);
					attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_03"]] += std::pow(dy, 3);
					attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_21"]] += std::pow(dx, 2) * dy;
					attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_12"]] += dx * std::pow(dy, 2);
				}

			},
			[&ATTR, &attrs, n](NodeMTPtr parent, NodeMTPtr child) -> void {
				attrs[parent->getIndex() + ATTR["CENTRAL_MOMENT_20"]] += attrs[child->getIndex() + ATTR["CENTRAL_MOMENT_20"]];
				attrs[parent->getIndex() + ATTR["CENTRAL_MOMENT_02"]] += attrs[child->getIndex() + ATTR["CENTRAL_MOMENT_02"]];
				attrs[parent->getIndex() + ATTR["CENTRAL_MOMENT_11"]] += attrs[child->getIndex() + ATTR["CENTRAL_MOMENT_11"]];
				attrs[parent->getIndex() + ATTR["CENTRAL_MOMENT_30"]] += attrs[child->getIndex() + ATTR["CENTRAL_MOMENT_30"]];
				attrs[parent->getIndex() + ATTR["CENTRAL_MOMENT_03"]] += attrs[child->getIndex() + ATTR["CENTRAL_MOMENT_03"]];
				attrs[parent->getIndex() + ATTR["CENTRAL_MOMENT_21"]] += attrs[child->getIndex() + ATTR["CENTRAL_MOMENT_21"]];
				attrs[parent->getIndex() + ATTR["CENTRAL_MOMENT_12"]] += attrs[child->getIndex() + ATTR["CENTRAL_MOMENT_12"]];
			
			},
			[&ATTR, &attrs, n](NodeMTPtr node) -> void {
				
				float area = attrs[node->getIndex() + ATTR["AREA"]]; // area
				auto normMoment = [area](float moment, int p, int q){ 
					return moment / std::pow( area, (p + q + 2.0) / 2.0); 
				}; //função para normalizacao dos momentos				
				

				//Momentos centrais
				float mu20 = attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_20"]];
				float mu02 = attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_02"]];
				float mu11 = attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_11"]];
				float mu30 = attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_30"]];
				float mu03 = attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_03"]];
				float mu21 = attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_21"]];
				float mu12 = attrs[node->getIndex() + ATTR["CENTRAL_MOMENT_12"]];
					
				float discriminant = std::pow(mu20 - mu02, 2) + 4 * std::pow(mu11, 2);
					
				// Verificar se o denominador é zero antes de calcular atan2 para evitar divisão por zero
				if (mu20 != mu02 || mu11 != 0) {
					float radians = 0.5 * std::atan2(2 * mu11, mu20 - mu02);// orientação em radianos
					float degrees = radians * (180.0 / M_PI); // Converter para graus
					if (degrees < 0) { // Ajustar para o intervalo [0, 360] graus
						degrees += 360.0;
					}
					attrs[node->getIndex() + ATTR["ORIENTATION"]] = degrees; // Armazenar a orientação em graus no intervalo [0, 360]
				} else {
					attrs[node->getIndex() + ATTR["ORIENTATION"]] = 0.0; // Se não for possível calcular a orientação, definir um valor padrão
				}

				// Verificar se o discriminante é positivo para evitar raiz quadrada de números negativos
				if (discriminant < 0) {
					std::cerr << "Erro: Discriminante negativo, ajustando para zero." << std::endl;
					discriminant = 0;
				}	
				float a1 = mu20 + mu02 + std::sqrt(discriminant); // autovalores (correspondente ao eixo maior)
				float a2 = mu20 + mu02 - std::sqrt(discriminant); // autovalores (correspondente ao eixo menor)

				// Verificar se a1 e a2 são positivos antes de calcular sqrt para evitar NaN
				if (a1 > 0) {
					attrs[node->getIndex() + ATTR["LENGTH_MAJOR_AXIS"]] = std::sqrt((2 * a1) / area); // length major axis
				} else {
					attrs[node->getIndex() + ATTR["LENGTH_MAJOR_AXIS"]] = 0.0; // Definir valor padrão
				}

				if (a2 > 0) {
					attrs[node->getIndex() + ATTR["LENGTH_MINOR_AXIS"]] = std::sqrt((2 * a2) / area); // length minor axis
				} else {
					attrs[node->getIndex() + ATTR["LENGTH_MINOR_AXIS"]] = 0.0; // Definir valor padrão
				}

				// Verificar se a2 é diferente de zero antes de calcular a excentricidade
				attrs[node->getIndex() + ATTR["ECCENTRICITY"]] = (std::abs(a2) > std::numeric_limits<float>::epsilon()) ? a1 / a2 : a1 / 0.1; // eccentricity

				// Verificar se moment20 + mu02 é diferente de zero antes de calcular a compacidade
				if ((mu20 + mu02) > std::numeric_limits<float>::epsilon()) {
					attrs[node->getIndex() + ATTR["COMPACTNESS"]] = (1.0 / (2 * PI)) * (area / (mu20 + mu02)); // compactness
				} else {
					attrs[node->getIndex() + ATTR["COMPACTNESS"]] = 0.0; // Definir valor padrão
				}


				// Calcular os momentos normalizados
				float eta20 = normMoment(mu20, 2, 0);
				float eta02 = normMoment(mu02, 0, 2);
				float eta11 = normMoment(mu11, 1, 1);
				float eta30 = normMoment(mu30, 3, 0);
				float eta03 = normMoment(mu03, 0, 3);
				float eta21 = normMoment(mu21, 2, 1);
				float eta12 = normMoment(mu12, 1, 2);

				// Cálculo dos momentos de Hu
				attrs[node->getIndex() + ATTR["HU_MOMENT_1_INERTIA"]] = eta20 + eta02; // primeiro momento de Hu => inertia
				attrs[node->getIndex() + ATTR["HU_MOMENT_2"]] = std::pow(eta20 - eta02, 2) + 4 * std::pow(eta11, 2);
				attrs[node->getIndex() + ATTR["HU_MOMENT_3"]] = std::pow(eta30 - 3 * eta12, 2) + std::pow(3 * eta21 - eta03, 2);
				attrs[node->getIndex() + ATTR["HU_MOMENT_4"]] = std::pow(eta30 + eta12, 2) + std::pow(eta21 + eta03, 2);
				
				attrs[node->getIndex() + ATTR["HU_MOMENT_5"]] = 
					(eta30 - 3 * eta12) * (eta30 + eta12) * (std::pow(eta30 + eta12, 2) - 3 * std::pow(eta21 + eta03, 2)) +
					(3 * eta21 - eta03) * (eta21 + eta03) * (3 * std::pow(eta30 + eta12, 2) - std::pow(eta21 + eta03, 2));
				
				attrs[node->getIndex() + ATTR["HU_MOMENT_6"]] = 
					(eta20 - eta02) * (std::pow(eta30 + eta12, 2) - std::pow(eta21 + eta03, 2)) + 
					4 * eta11 * (eta30 + eta12) * (eta21 + eta03);
				
				attrs[node->getIndex() + ATTR["HU_MOMENT_7"]] = 
					(3 * eta21 - eta03) * (eta30 + eta12) * (std::pow(eta30 + eta12, 2) - 3 * std::pow(eta21 + eta03, 2)) -
					(eta30 - 3 * eta12) * (eta21 + eta03) * (3 * std::pow(eta30 + eta12, 2) - std::pow(eta21 + eta03, 2));

				
		});
		return std::make_pair(attributeNames, attrs);
    }



};



#endif 