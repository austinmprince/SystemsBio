# SystemsBio

## Gapfilling Methanoccocus maripaludis
For the main portion of my project I worked on gap filling a model of methanococcus maripaludis. In order to do this I implemented the gapfilling algorithm for cobrapy. This algorithm fills gaps in the model so that the production of the biomass function is above a certain threshold. All the implementation of the gapfilling can be found in the Functions. Gapfilling this model gave me on the order of hundreds of possible reactions that could be plugged into the model. In order to test the real world feasability of these models and see the mechanism through which these models filled the model I tested the flux (flow) through ATP Synthase in each of the gapfilled models. ATP Synthase is the main energy producing reaction in native methanococcus maripaludis so by examining the flux I sought to find the mechanism through which the ATP was produced. I produced the following heat map and noticed clustering of the reactions in three main spots. 

![Heat Map ATP](\HeatMapATPSynthase.pdf)

Further examination is needed to determine the exact mechanism of these reactions gap filling.
