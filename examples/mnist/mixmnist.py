import numpy as np
import torch
from typing import Dict, Tuple
import torchvision.transforms as transforms
from numpy.typing import NDArray
import torchvision.transforms as transforms
from torch.utils.data import Dataset

class MIXMNIST_BASE:
    def __init__(self, root:str='./data', prefix:str=""):
        self.root = root
        self.prefix = prefix
        self.transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
        )
        self.datasets = self._get_dataset()

    def _get_dataset(self) -> Dict[str,Tuple[NDArray,NDArray]]:
        """
        Formatted dataset has the same form as MNIST
        """
        # NpzFile '{...}_train_test.npz' with keys: X_train, X_test, y_train, y_test
        loaded:Dict[str,NDArray] = np.load(f'{self.root}/MNIST-MIX-all/{self.prefix}_train_test.npz')
        raw_dataset = {
            'train': (loaded['X_train'], loaded['y_train']),
            'test': (loaded['X_test'], loaded['y_test'])
        }
        formatted_dataset = {}
        for split_name, (imgs, targets) in raw_dataset.items():
            formatted_items = []
            for i, img in enumerate(imgs):

                if self.transform:
                    img = self.transform(img)
                formatted_items.append((img, int(targets[i])))
            formatted_dataset[split_name] = formatted_items
        return formatted_dataset

class MIXMNIST(Dataset):
    def __init__(self, root: str = './data', prefix: str = "", subset: str = "train"):
        self.base = MIXMNIST_BASE(root=root, prefix=prefix)
        self.subset = subset
        print(f"Dataset Created for MIX MNIST: {prefix}-{subset}")

    def __getitem__(self, item: int) -> torch.Tensor:
        return self.base.datasets[self.subset][int(item[0])][0]
    
    def __len__(self) -> int:
        length = len(self.base.datasets[self.subset])
        return length

# datasets = MIXMNIST_BASE(prefix="Bangla").datasets