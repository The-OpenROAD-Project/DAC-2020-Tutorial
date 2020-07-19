'''
Copyright (c) 2020, Abdelrahman Hosny <abdelrahman_hosny@brown.edu>
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

import argparse
import dgl as dgl
from dgl.data.utils import save_graphs, load_graphs
import model
import dataset
import os
import random

class CapitalisedHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
            return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, \
        formatter_class=CapitalisedHelpFormatter, \
        description='Netlist Classification')
    parser._positionals.title = 'Positional arguments'
    parser._optionals.title = 'Optional arguments'
    parser.add_argument("designs", type=str, \
        help="Path a directory that contains all def files")
    parser.add_argument("output_dir", type=str, \
        help="Path to output directory")
    parser.add_argument("-p", "--epochs", dest='epochs', default=50, \
        help="Number of epochs to train for")

    args = parser.parse_args()
    output_dir = os.path.join(os.getcwd(), args.output_dir)    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    designs = []
    design_names = []

    dgl_files = [f for f in os.listdir(args.designs) if os.path.isfile(os.path.join(args.designs, f)) and f.endswith(".dgl")]
    
    for f in dgl_files:
        graphs, _ = load_graphs(os.path.join(args.designs, f))
        g = graphs[0]
        name = f.split('.')[0]
        
        designs.append(g)
        design_names.append(name)

    # shuffle
    analysis = list(map(list, zip(designs, design_names)))
    random.shuffle(analysis)
    designs, design_names = zip(*analysis)
    
    # prepare training/test data
    trainset = dataset.ICTunerDataset()
    for i, _ in enumerate(designs[:int(len(designs) * 0.8)]):
        trainset.add_design(designs[i], design_names[i])

    testset = dataset.ICTunerDataset()
    for i, _ in enumerate(designs[int(len(designs) * 0.8):]):
        testset.add_design(designs[i], design_names[i])

    # train model
    tutorial = model.Tutorial(trainset, testset, trainset.labels_map(), output_dir)
    tutorial.set_epochs(int(args.epochs))
    tutorial.train()
    tutorial.evalute()
