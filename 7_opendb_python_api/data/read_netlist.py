'''
Copyright (c) 2020, Abdelrahman Hosny
All rights reserved.
BSD 3-Clause License

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import dgl as dgl
import opendbpy as odb
from dgl.data.utils import save_graphs


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

def save_graph(file_path, g):
    save_graphs(file_path, g)

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

if __name__ == "__main__":
    G = read_netlist("tech.lef", "design.def")
    print(G)
    save_graph("design.dgl", G)