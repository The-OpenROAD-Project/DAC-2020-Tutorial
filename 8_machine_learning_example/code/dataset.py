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

import math
import networkx as nx
import numpy as np
from sklearn.preprocessing import LabelEncoder
from dgl import DGLGraph

__all__ = ['ICTunerDataset']

class ICTunerDataset(object):
    
    def __init__(self):
        super(ICTunerDataset, self).__init__()
        self.graphs = []
        self.design_names = []
        
        self.labels = []
        

    def __len__(self):
        """Return the number of graphs in the dataset."""
        return len(self.graphs)

    def __getitem__(self, idx):
        """Get the i^th sample.
        Paramters
        ---------
        idx : int
            The sample index.
        Returns
        -------
        (dgl.DGLGraph, int)
            The graph and its label.
        """
        return self.graphs[idx], self.labels[idx]

    @property
    def num_classes(self):
        """Number of classes."""
        return len(self.design_names)
    
    @property
    def dataset_labels(self):
        return self.labels
    
    @property
    def dataset_design_names(self):
        return self.design_names
    
    def _create_labels(self):
        labelencoder = LabelEncoder()
        self.labels = labelencoder.fit_transform(self.design_names)

    def add_design(self, graph, design_name):
        self.graphs.append(graph)
        self.design_names.append(design_name)

        self._create_labels()
    
    def labels_map(self):
        labels_map = {}
        for i in range(len(self.labels)):
            labels_map[self.labels[i]] = self.design_names[i]
        
        return labels_map