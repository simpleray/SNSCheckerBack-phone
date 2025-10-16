Japanese multi-task CNN trained on UD-Japanese BCCWJ r2.8 + GSK2014-A(2019) + transformers-ud-japanese-electra--base. Components: transformer, parser, atteribute_ruler, ner, morphologizer, compound_splitter, bunsetu_recognizer.

| Feature | Description |
| --- | --- |
| **Name** | `ja_ginza_electra` |
| **Version** | `5.1.2` |
| **spaCy** | `>=3.2.0,<3.5.0` |
| **Default Pipeline** | `transformer`, `parser`, `ner`, `morphologizer`, `compound_splitter`, `bunsetu_recognizer` |
| **Components** | `transformer`, `parser`, `attribute_ruler`, `ner`, `morphologizer`, `compound_splitter`, `bunsetu_recognizer` |
| **Vectors** | 0 keys, 0 unique vectors (0 dimensions) |
| **Sources** | [UD_Japanese-BCCWJ r2.8](https://github.com/UniversalDependencies/UD_Japanese-BCCWJ) (Asahara, M., Kanayama, H., Tanaka, T., Miyao, Y., Uematsu, S., Mori, S., Matsumoto, Y., Omura, M., & Murawaki, Y.)<br />[GSK2014-A(2019)](https://www.gsk.or.jp/catalog/gsk2014-a/) (Tokyo Institute of Technology)<br />[SudachiDict_core](https://github.com/WorksApplications/SudachiDict) (Works Applications Enterprise Co., Ltd.)<br />[mC4](https://huggingface.co/datasets/mc4) (Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, & Peter J. Liu)<br />[megagonlabs/transformers-ud-japanese-electra-base-ginza-5.1.0](https://huggingface.co/megagonlabs/transformers-ud-japanese-electra-base-ginza-5.1.0) (Hiroshi Matsuda (Megagon Labs Tokyo, Recruit Co., Ltd.)) |
| **License** | `MIT License` |
| **Author** | [Megagon Labs Tokyo.](https://github.com/megagonlabs/ginza) |

### Label Scheme

<details>

<summary>View label scheme (241 labels for 3 components)</summary>

| Component | Labels |
| --- | --- |
| **`parser`** | `ROOT`, `acl`, `acl_bunsetu`, `advcl`, `advcl_bunsetu`, `advmod`, `advmod_bunsetu`, `amod`, `amod_bunsetu`, `aux`, `aux_bunsetu`, `case`, `case_bunsetu`, `cc`, `cc_bunsetu`, `ccomp_bunsetu`, `compound`, `compound_bunsetu`, `cop`, `csubj_bunsetu`, `dep`, `dep_bunsetu`, `det_bunsetu`, `discourse_bunsetu`, `dislocated_bunsetu`, `fixed`, `mark`, `nmod`, `nmod_bunsetu`, `nsubj_bunsetu`, `nummod`, `obj_bunsetu`, `obl_bunsetu`, `punct`, `punct_bunsetu` |
| **`ner`** | `Academic`, `Age`, `Aircraft`, `Airport`, `Amphibia`, `Amusement_Park`, `Animal_Disease`, `Animal_Part`, `Archaeological_Place_Other`, `Art_Other`, `Astral_Body_Other`, `Award`, `Bay`, `Bird`, `Book`, `Bridge`, `Broadcast_Program`, `Cabinet`, `Calorie`, `Canal`, `Car`, `Car_Stop`, `Character`, `City`, `Class`, `Clothing`, `Color_Other`, `Company`, `Company_Group`, `Compound`, `Conference`, `Constellation`, `Continental_Region`, `Corporation_Other`, `Country`, `Countx_Other`, `County`, `Culture`, `Date`, `Day_Of_Week`, `Disease_Other`, `Dish`, `Doctrine_Method_Other`, `Domestic_Region`, `Drug`, `Earthquake`, `Element`, `Email`, `Era`, `Ethnic_Group_Other`, `Event_Other`, `Facility_Other`, `Facility_Part`, `Family`, `Fish`, `Flora`, `Flora_Part`, `Food_Other`, `Frequency`, `Fungus`, `GOE_Other`, `GPE_Other`, `Game`, `Geological_Region_Other`, `God`, `Government`, `ID_Number`, `Incident_Other`, `Insect`, `Intensity`, `International_Organization`, `Island`, `Lake`, `Language_Other`, `Latitude_Longtitude`, `Law`, `Line_Other`, `Living_Thing_Other`, `Living_Thing_Part_Other`, `Location_Other`, `Magazine`, `Mammal`, `Material`, `Measurement_Other`, `Military`, `Mineral`, `Mollusc_Arthropod`, `Money`, `Money_Form`, `Mountain`, `Movement`, `Movie`, `Multiplication`, `Museum`, `Music`, `N_Animal`, `N_Country`, `N_Event`, `N_Facility`, `N_Flora`, `N_Location_Other`, `N_Natural_Object_Other`, `N_Organization`, `N_Person`, `N_Product`, `Name_Other`, `National_Language`, `Nationality`, `Natural_Disaster`, `Natural_Object_Other`, `Natural_Phenomenon_Other`, `Nature_Color`, `Newspaper`, `Numex_Other`, `Occasion_Other`, `Offense`, `Ordinal_Number`, `Organization_Other`, `Park`, `Percent`, `Period_Day`, `Period_Month`, `Period_Time`, `Period_Week`, `Period_Year`, `Periodx_Other`, `Person`, `Phone_Number`, `Physical_Extent`, `Plan`, `Planet`, `Point`, `Political_Organization_Other`, `Political_Party`, `Port`, `Position_Vocation`, `Postal_Address`, `Printing_Other`, `Pro_Sports_Organization`, `Product_Other`, `Province`, `Public_Institution`, `Railroad`, `Rank`, `Region_Other`, `Religion`, `Religious_Festival`, `Reptile`, `Research_Institute`, `River`, `Road`, `Rule_Other`, `School`, `School_Age`, `Sea`, `Ship`, `Show`, `Show_Organization`, `Spa`, `Space`, `Spaceship`, `Speed`, `Sport`, `Sports_Facility`, `Sports_League`, `Sports_Organization_Other`, `Station`, `Style`, `Temperature`, `Theater`, `Theory`, `Time`, `Time_Top_Other`, `Timex_Other`, `Title_Other`, `Train`, `Treaty`, `Tumulus`, `Tunnel`, `URL`, `Unit_Other`, `Vehicle_Other`, `Volume`, `War`, `Water_Route`, `Weapon`, `Weight`, `Worship_Place`, `Zoo` |
| **`morphologizer`** | `POS=PUNCT`, `POS=NUM`, `POS=NOUN`, `POS=ADP`, `POS=AUX`, `POS=VERB`, `POS=CCONJ`, `POS=PART`, `POS=SCONJ`, `POS=SYM`, `POS=ADJ`, `POS=DET`, `POS=PRON`, `POS=PROPN`, `POS=ADV`, `POS=X`, `POS=INTJ` |

</details>

### Accuracy

| Type | Score |
| --- | --- |
| `DEP_UAS` | 93.45 |
| `DEP_LAS` | 92.09 |
| `SENTS_P` | 88.65 |
| `SENTS_R` | 88.48 |
| `SENTS_F` | 88.57 |
| `ENTS_F` | 65.43 |
| `ENTS_P` | 65.42 |
| `ENTS_R` | 65.44 |
| `POS_ACC` | 98.55 |
| `MORPH_MICRO_F` | 0.00 |
| `MORPH_PER_FEAT` | 0.00 |
| `MORPH_ACC` | 0.00 |
| `TAG_ACC` | 98.78 |
| `TRANSFORMER_LOSS` | 1594658.50 |
| `PARSER_LOSS` | 929247.42 |
| `NER_LOSS` | 27513.87 |
| `MORPHOLOGIZER_LOSS` | 34338.76 |