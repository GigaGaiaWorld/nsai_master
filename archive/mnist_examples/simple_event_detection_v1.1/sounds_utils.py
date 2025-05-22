import os

import torch
import torch.nn as nn


class SoundVGGish(nn.Module):
    def __init__(self, n_classes=10):
        super(SoundVGGish, self).__init__()

        self.net = nn.Sequential(
            nn.Linear(in_features=128, out_features=100),
            nn.ReLU(),
            nn.Linear(in_features=100, out_features=80),
            nn.ReLU(),
            nn.Linear(in_features=80, out_features=50),
            nn.ReLU(),
            nn.Linear(in_features=50, out_features=25),
            nn.ReLU(),
            nn.Linear(in_features=25, out_features=n_classes),

            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.net(x)


def neural_predicate_vggish(network, path, use_saved_preprocessed=True):
    preprocessed_filename = 'vggish_preprocessed/' + os.path.splitext(os.path.basename(str(path)[1:-1]))[0] + '.pt'

    if use_saved_preprocessed and os.path.exists(preprocessed_filename):
        # Try to load the features from a file
        features = torch.load(preprocessed_filename)
    else:
        print(path, preprocessed_filename)

        raise Exception

    features = features.unsqueeze(0)

    # Use the neural network to get the classification of the audio
    res = network.net(features.float())

    # Return the result
    return res.squeeze(0)
