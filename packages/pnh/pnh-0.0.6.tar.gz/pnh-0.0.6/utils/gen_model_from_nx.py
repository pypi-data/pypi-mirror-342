import pandapipes 
import networkx as nx
import math
import logging
import sys

logger = logging.getLogger('pnh.utils.gen_model_from_nx')

# node data keys 
zKey='z'

# node bc data keys 
pBcKey='extPressure' 
flowBcKey='extFlow' 
TBcKey='inletTemperature' 

# pipe data keys
lengthKey='L' 
diameterKey='D'
kKey='k' 
alphaKey='alpha'
TaKey='Ta'

# id
idKey='ID'

def pp(
        nxg=nx.Graph()

       # net std values
       ,fluid='water'       
       ,TNet=273.15+90. 
       ,pNet=10. 

       # node data keys used if available
       ,z=zKey

       # node bc data keys used if available       
       ,pBc=pBcKey 
       ,flowBc=flowBcKey 
       ,TBc=TBcKey 

       # pipe data keys used if available
       ,length=lengthKey 
       ,diameter=diameterKey
       ,k=kKey 
       ,alpha=alphaKey
       ,Ta=TaKey

       # ppID
       ,id=idKey
):
    """ Returns a pandapipes.pandapipesNet from a networkx graph with pnh-data.
    
    :param nxg: networkx graph with pnh-data

    :param fluid: pp's net fluid (default: 'water')
    :param TNet: pp's net std tfluid_k in create_junction (default: 273.15+90. [K])
    :param pNet: pp's net std pn_bar in create_junction (default: 10. [bar])

    :param z: i.e. 'z'; node data key for geodetic height in [m] - pp's height_m in create_junction; default: 0.

    :param pBc: i.e. 'extPressure'; node bc data key for pBc in [bar] - pp's p_bar in create_ext_grid; default: no pBc
    :param flowBc: i.e. 'extFlow'; node bc data key for flowBc in [kg/s] - pp's mdot_kg_per_s in create_sink/_source ; here neg. for sinks and pos. for sources; default: no flowBc
    :param TBc: i.e. 'inletTemperature'; node bc data key for TBc in [K] - pp's t_k in create_ext_grid; default: no TBc

    :param length: i.e. 'L'; pipe data key; pipe length in [m]; default: 1000.
    :param diameter: i.e. 'D'; pipe data key; pipe inner diameter in [mm]; default: 100.
    :param k: i.e. 'k'; pipe data key; pipe roughness in [mm]; default: 0.25
    ..
    :param alpha: i.e. 'alpha'; pipe data key; heat transfer coefficient in [W/(m*K)]; alpha/(pi*D/1000) = pp's alpha_w_per_m2k; default Value: None; note that both data keys ('alpha' and 'Ta') must be supplied to create a pipe with heat transfer property; note that 'D' (inner diameter Di) is used to calculate alpha_m2 from alpha_m; the following relationships exist between alpha_m, alpha_m2 and D:

    .. math::

        \\alpha_{m2}=\\frac{\\alpha_m}{\pi*D}

        \\alpha_{m_{D_i}}=\\alpha_{m_{D_a}}*\\frac{D_i}{D_a} 

        \\alpha_{m2_{D_i}}=\\alpha_{m2_{D_a}}*\\frac{D_a}{D_i}        

    :param Ta: i.e. 'Ta'; pipe data key; ambient temperatur in [K]; pp's text_k; default Value: None
    ..
    :param id: i.e. 'ID'; nxg's data key to store the corresponding ppIDs

    :return: pandapipes.pandapipesNet

    """

    logStr=f"{sys._getframe().f_code.co_name}:"
    logger.debug(f"{logStr} Start.") 

    net=None

    # create model
    net = pandapipes.create_empty_network(fluid=fluid)

    # create junctions
    js={}
    for idx,(node, data) in enumerate(nxg.nodes(data=True)):
        
        values={}
        for attribName,default in zip([z],[0.]):
            
            if attribName in data.keys():
                values[attribName]=data[attribName]
            else:
                values[attribName]=default

        nameStr=f"{str(node)}"
        j=pandapipes.create_junction(net
                            ,pn_bar=pNet
                            ,tfluid_k=TNet
                            ,height_m=values[z]
                            ,nameStr=nameStr
        ) 
        js[node]=j
        nxg.nodes[node].update({id:j})

        logger.debug(f"{logStr} junction: Nr. {idx}: nameStr: {nameStr}: j: {str(j)}: {id} (j): {j} created.")

    # create pipes
    for idx,(u, v, data) in enumerate(nxg.edges(data=True)):
        
        values={}
        for attribName,default in zip([length,diameter,k],[1000.,100.,0.25]):
            
            if attribName in data.keys():
                values[attribName]=data[attribName]
            else:
                values[attribName]=default

        #nameStr=f"{str(js[u])}-{str(js[v])}"
        nameStr=f"{str(u)}-{str(v)}" # use original node identifiers not pp's 
        if alpha in data.keys() and Ta in data.keys():
            pandapipes.create_pipe_from_parameters(net
                                            ,from_junction=js[u]
                                            ,to_junction=js[v]
                                            ,length_km=values[length]/1000.
                                            ,diameter_m=values[diameter]/1000.
                                            ,k_mm=values[k]
                                            ,nameStr=nameStr
                                            #
                                            ,alpha_w_per_m2k=data[alpha]/(math.pi*values[diameter]/1000.)
                                            ,text_k=data[Ta]
            )            
        else:
            pandapipes.create_pipe_from_parameters(net
                                            ,from_junction=js[u]
                                            ,to_junction=js[v]
                                            ,length_km=values[length]/1000.
                                            ,diameter_m=values[diameter]/1000.
                                            ,k_mm=values[k]
                                            ,nameStr=nameStr
            )

        nxg.edges[u,v].update({id:idx})
        logger.debug(f"{logStr} pipe: Nr. {idx}: nameStr: {nameStr}: {id} (idx): {idx} created.")

    # create pBcs/TBcs (ext. grids in pandapipes)
    for node, data in nxg.nodes(data=True):            
            if pBc not in data.keys() and TBc not in data.keys():
                continue
            # pt
            if pBc in data.keys() and TBc in data.keys():
                pandapipes.create_ext_grid(net
                                ,junction=js[node]
                                ,p_bar=data[pBc]
                                ,t_k=data[TBc]
                )                        
            # p
            elif pBc in data.keys() and TBc not in data.keys():
                pandapipes.create_ext_grid(net
                                ,junction=js[node]
                                ,p_bar=data[pBc]
                                #,t_k=data[TBc]
                )
            # t
            elif pBc not in data.keys() and TBc in data.keys():
                pandapipes.create_ext_grid(net
                                ,junction=js[node]
                                #,p_bar=data[pBc]
                                ,t_k=data[TBc]
                )                
            
    # create flowBcs 
    for node, data in nxg.nodes(data=True):            
            if flowBc not in data.keys():
                continue

            flowBcValue=data[flowBc]

            if flowBcValue==0.:
                 continue

            if flowBcValue>0.:
                pandapipes.create_source(net  
                            ,junction=js[node]
                            ,mdot_kg_per_s=flowBcValue
                )
            else:
                pandapipes.create_sink(net
                            ,junction=js[node]
                                            #!
                            ,mdot_kg_per_s=-flowBcValue
                )

    logger.debug(f"{logStr} End.") 
    return net 