# Annotation Guidelines

The identification of phrases and terms to label require to establish annotation guidelines that are as consistent as possible in term extractions. At first, we define some linguistic terminologies, since we observed no overall agreement for all of them in the literature.

<em>Category</em>: Information categories are Biological Named Entity Types, e.g., ORGANISM or ENVIRONMENT. In related work, sometimes the term "entity" is used for entity types.

<em>Entity</em>: Entities are instances of Entity Types, e.g., "Atlantic Ocean" [LOCATION] or "forest" [ENVIRONMENT]. An entity is an artifact with an assigned category. In literature, we sometimes encounter the term "mention" for entities.

<em>Artifact</em>: We denote an artifact as a phrase or term that has been identified for categorization (based on the guidelines described below) but that has not been classified yet.

<em>Noun Entity</em>: Noun entities are proper nouns and common nouns that can either consist of one word or several words (e.g., compound nouns). Proper nouns name specific things and always begin with a capital letter, e.g., "Europe", "Apis mellifera" (honeybee), "CO2". Common nouns are generic nouns that do not name specific things, such as water, grassland and aquifer.

<em>Nested Entity</em>: Since noun entities might consist of several words such as "benthic oxygen uptake rate" all nested terms are defined as "nested entities", e.g., "benthic", "oxygen".


We used and adapted the annotation guidelines from Kilicoglu et al (Annotating Named Entities in Consumer Health Questions, LREC2016, Portorož, Slovenia).

<em>Part-Of-Speech</em>: We solely focused on noun entities. Adjectives are only considered if they occur as nested entities in a compound noun. All other part-of-speech types are not taken into account. Noun entities can be either proper nouns or common nouns.

<em>Entity Ambiguity</em>: Annotators are only permitted to assign one category to each entity. Based on the given context (the entire question), they need to select the category that is most appropriate. That also corresponds to the search use case where keywords are usually entered with one specific meaning.

<em>Generic Terms</em>: Terms that are too broad and unspecific are neglected, such as "data", "rate" or "change". A list with too broad terms is provided in this repository.

<em>Nested Entities</em>: Nested entities are often neglected in annotation processes due to practical reasons. In compound nouns usually only the last term that determines the actual artifact is annotated. However, in Life Sciences the nested entities of compound nouns might indicate important information to the search context. In order to avoid multi-labeling, we identified nested entities as follows:
A nested entity can be either an adjective or a noun that describes or modifies the last word, e.g., "mesopelagic zone". Too generic nouns will be ignored. If a generic term occurs in a compound noun with two words, the compound noun is classified as a whole, e.g., "climate change", "uptake rate". A nested entity is selected for classification if it might refer to a different entity type as the reference word, e.g., benthic [ENVIRONMENT] oxygen [MATERIAL] uptake rate [QUALITY]. In these cases, we provided the full artifact for category assignment as well as the nested entities.

<em>Biodiversity terms</em>: In biodiversity, some compound nouns have propagated. They consist of several words but need to stay together, e.g., "climate change", "cold seep", "marine phages". We created a list of biodiversity terms that occurred in this question corpus and provide the list in this repository.


