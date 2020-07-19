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

import os
import networkx as nx
import dgl as dgl
import dgl.function as fn
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

class Tutorial:
    def __init__(self, trainset, testset, labels_map, output_dir):
        self.trainset = trainset
        self.testset = testset
        self.labels_map = labels_map
        self.output_dir = output_dir

        # Hyperparameters
        self.epochs = 50
        self.batch_size = 32
        self.learning_rate = 0.01

        # Mode
        self.model = Classifier(1, 256, self.trainset.num_classes)
        self.loss_func = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

        self.model.train()
        torch.save(self.model.state_dict(), os.path.join(output_dir, 'model.pt'))

    def train(self):
        self.data_loader = DataLoader(self.trainset, batch_size=self.batch_size, shuffle=True, collate_fn=collate)

        epoch_losses = []
        for epoch in range(self.epochs):
            epoch_loss = 0
            for iter, (bg, label) in enumerate(self.data_loader):
                prediction = self.model(bg)
                loss = self.loss_func(prediction, label)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                epoch_loss += loss.detach().item()
            epoch_loss /= (iter + 1)
            print('Epoch {}, loss {:.4f}'.format(epoch, epoch_loss))
            epoch_losses.append(epoch_loss)

        plt.title('cross entropy averaged over minibatches')
        plt.plot(epoch_losses)
        plt.savefig(os.path.join(self.output_dir, 'training-loss.pdf'))

        train_X, train_Y = map(list, zip(*self.trainset))
        train_bg = dgl.batch(train_X)
        train_Y = torch.tensor(train_Y).float().view(-1, 1)

    def evalute(self):
        self.model.eval()
        test_X, test_Y = map(list, zip(*self.testset))
        test_bg = dgl.batch(test_X)
        test_Y = torch.tensor(test_Y).float().view(-1, 1)

        probs_Y = torch.softmax(self.model(test_bg), 1)
        sampled_Y = torch.multinomial(probs_Y, 1)
        argmax_Y = torch.max(probs_Y, 1)[1].view(-1, 1)
        sampled_accuracy = (test_Y == sampled_Y.float()).sum().item() / len(test_Y) * 100
        argmax_accuracy = (test_Y == argmax_Y.float()).sum().item() / len(test_Y) * 100
        print('Accuracy of sampled predictions on the test set: {:.4f}%'.format(sampled_accuracy))
        print('Accuracy of argmax predictions on the test set: {:4f}%'.format(argmax_accuracy))

    def set_epochs(self, epochs):
        self.epochs = epochs

def collate(samples):
    graphs, labels = map(list, zip(*samples))
    batched_graph = dgl.batch(graphs)
    return batched_graph, torch.tensor(labels)

msg = fn.copy_src(src='h', out='m')
def reduce(nodes):
    accum = torch.mean(nodes.mailbox['m'], 1)
    return {'h': accum}

class NodeApplyModule(nn.Module):
    def __init__(self, in_feats, out_feats, activation):
        super(NodeApplyModule, self).__init__()
        self.linear = nn.Linear(in_feats, out_feats)
        self.activation = activation
    
    def forward(self, node):
        h = self.linear(node.data['h'])
        h = self.activation(h)
        return {'h': h}

class GCN(nn.Module):
    def __init__(self, in_feats, out_feats, activation):
        super(GCN, self).__init__()
        self.apply_mod = NodeApplyModule(in_feats, out_feats, activation)
    
    def forward(self, g, feature):
        g.ndata['h'] = feature
        g.update_all(msg, reduce)
        g.apply_nodes(func=self.apply_mod)
        return g.ndata.pop('h')

class Classifier(nn.Module):
    def __init__(self, in_dim, hidden_dim, n_classes):
        super(Classifier, self).__init__()
        self.layers = nn.ModuleList([
            GCN(in_dim, hidden_dim, F.relu),
            GCN(hidden_dim, hidden_dim, F.relu)
        ])
        self.classify = nn.Linear(hidden_dim, n_classes)
    
    def forward(self, g):
        h = g.in_degrees().view(-1, 1).float()
        for conv in self.layers:
            h = conv(g, h)
        g.ndata['h'] = h
        hg = dgl.mean_nodes(g, 'h')
        return self.classify(hg)