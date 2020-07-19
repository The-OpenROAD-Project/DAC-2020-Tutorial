[:arrow_backward: &nbsp; Previous: Layout Visualization](../6_layout_visualization) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Machine Learning Example &nbsp; :arrow_forward:](../8_machine_learning_example)

# OpenDB Python API

In this section, we will have a look at the OpenDB Python API. The goal of this exercise is to pave the way to building machine learning models using Python packages.

## Installation

### CentOS 7

OpenDB Python API has been released as a Python package on [PyPI](https://pypi.org/project/opendbpy/).

To install:

```Shell
pip install opendbpy
```

### Ubuntu

To use the package on Ubuntu, you need to build from sources.

> :computer: **NOTE** :computer:
> 
> If you are interested in making `opendbpy` available for Ubuntu on PyPi, get in touch with Abdelrahman Hosny <<ahosny@openroad.tools>>

To build:

```Shell
git clone https://github.com/The-OpenROAD-Project/OpenDB.git
mkdir build and cd build
cmake -DBUILD_PYTHON=ON ..
make
cd src/swig/python
python setup.py install
```

### Other dependencies

We will use PyTorch and DGL libraries. Install them using `pip`.

```Shell
pip install torch
pip install dgl
```

## Read LEF/DEF from Python

In the below example, we will read a netlist into a [DGL](https://www.dgl.ai/) graph to be used for building machine learning models.

### Import Packages

```Python
import dgl
import opendbpy as odb
```

### Read Netlist

```Python
def read_netlist(lef_file, def_file):
    # intialize the database
    db = odb.dbDatabase.create()

    # load the lef file
    try:
        odb.read_lef(db, lef_file)
    except Exception as e:
        logger.error("Problem loading the tech file!")
        return None

    # load the def file
    try:
        odb.read_def(db, def_file)
    except Exception as e:
        logger.error("Problem loading the design!")
        return None
    
    # parse the design into a DGL graph
    design = db.getChip()
    G = build_graph(design)

    print(str.format('Built a graph with %s nodes' % str(G.number_of_nodes())))
    print(str.format('.... Added %s edges' % str(G.number_of_edges())))

    return G
```

### Netlist to Graph

```Python
def build_graph(design, undirected=False):
    '''
    Input: design is an OpenDB representation of the chip
    Returns: DGL graph
    '''
    instances = design.getBlock().getInsts()
    pins = design.getBlock().getBTerms()

    # initialize graph with number of nodes
    g = dgl.DGLGraph()
    g.add_nodes(len(instances) + len(pins))

    # DGL represents nodes in numbers only. So, we need to assign mapping
    nodes_mapping = {}
    i = 0
    for inst in instances:
        nodes_mapping[inst.getName()] = i
        i += 1
    for pin in pins:
        nodes_mapping[pin.getName()] = i
        i += 1

    nets = design.getBlock().getNets()
    for net in nets:
        # exclude power nets
        if net.isSpecial():
            continue

        iterms = net.getITerms()
        bterms = net.getBTerms()

        # given a net, figure out the driving cell and the loads
        driving_cell = None
        loads = []

        # if iterm, then it needs to have direction output to be a driving cell
        for iterm in iterms:
            if iterm.getIoType() == 'OUTPUT':
                driving_cell = iterm.getInst().getName()
            else:
                loads.append(iterm.getInst().getName())
        
        # if bterm, then it needs to have direction input to be a driving cell
        for bterm in bterms:
            if bterm.getIoType() == 'INPUT':
                assert (driving_cell == None), "Something is wrong with the directions!"
                driving_cell = bterm.getName()
            else:
                loads.append(bterm.getName())
        
        assert (driving_cell != None), "Couldn't figure out the net directions"

        # add edges
        src = nodes_mapping[driving_cell]
        dst = list(map(lambda name: nodes_mapping[name], loads))
        g.add_edges(src, dst)
        
        # add self-loop
        g.add_edge(src, src)

        # add opposite-direction edges if undirected
        if undirected:
            g.add_edges(dst, src)

    return g
```

### Putting It All Together

Navigate to the data directory and run: `python read_netlist.py`

You should see an output that looks like:

```Python
Using backend: pytorch
Notice 0: Reading LEF file:  merged_spacing.lef
Notice 0:     Created 22 technology layers
Notice 0:     Created 27 technology vias
Notice 0:     Created 134 library cells
Notice 0: Finished LEF file:  merged_spacing.lef
Notice 0: 
Reading DEF file: gcd_nangate_floorplan.def
Notice 0: Design: gcd
Notice 0:     Created 54 pins.
Notice 0:     Created 272 components and 1508 component-terminals.
Notice 0:     Created 343 nets and 964 connections.
Notice 0: Finished DEF file: gcd_nangate_floorplan.def
Built a graph with 326 nodes
.... Added 1018 edges
DGLGraph(num_nodes=326, num_edges=1018,
         ndata_schemes={}
         edata_schemes={})
```

## Conclusion

What can we do with a DGL graph? In the next section, we will look at an example of learning node embeddings to classify graphs.

[:arrow_backward: &nbsp; Previous: Layout Visualization](../6_layout_visualization) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Machine Learning Example &nbsp; :arrow_forward:](../8_machine_learning_example)