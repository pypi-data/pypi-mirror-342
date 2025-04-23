import numpy as np
from PIL import Image
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report
import torch
from torch import nn
from torch import optim
from torch.utils.data import random_split
from typing import List, Optional, Union, Tuple, Collection, Callable
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder

from model_wrapper.utils import acc_predict, acc_predict_dataset
from model_wrapper import (
    ModelWrapper,
    SimpleModelWrapper,
    ClassifyModelWrapper,
    SimpleClassifyModelWrapper,
    SplitClassifyModelWrapper,
    RegressModelWrapper,
    SimpleRegressModelWrapper,
    SplitRegressModelWrapper,
    log_utils,
)

__all__ = [
    "ModelWrapper",
    "SimpleModelWrapper",
    "ClassifyModelWrapper",
    "SimpleClassifyModelWrapper",
    "SplitClassifyModelWrapper",
    "ImageClassifyModelWrapper",
    "SplitImageClassifyModelWrapper",
    "RegressModelWrapper",
    "SimpleRegressModelWrapper",
    "SplitRegressModelWrapper",
]


def get_transform(imgsz: Union[int, tuple, list]):
    if imgsz:
        if isinstance(imgsz, int):
            imgsz = (imgsz, imgsz)
        return transforms.Compose([transforms.Resize(imgsz), transforms.ToTensor()])
    else:
        return transforms.ToTensor()


def get_train_transform(imgsz: Union[int, tuple, list]):
    if imgsz:
        if isinstance(imgsz, int):
            imgsz = (imgsz, imgsz)
        return transforms.Compose(
            [
                transforms.Resize(imgsz),
                transforms.ColorJitter(
                    brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1
                ),  # 亮度、对比度、饱和度和色相
                transforms.RandomAffine(
                    degrees=(-10, 10),
                    translate=(0.1, 0.1),
                    scale=(0.9, 1.1),
                    shear=(-10, 10),
                ),
                transforms.ToTensor(),
                transforms.RandomErasing(
                    p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)
                ),  # 遮挡
            ]
        )
    else:
        return transforms.Compose(
            [
                transforms.ColorJitter(
                    brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1
                ),  # 亮度、对比度、饱和度和色相
                transforms.RandomAffine(
                    degrees=(-10, 10),
                    translate=(0.1, 0.1),
                    scale=(0.9, 1.1),
                    shear=(-10, 10),
                ),
                transforms.ToTensor(),
                transforms.RandomErasing(
                    p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)
                ),  # 遮挡
            ]
        )


class ImageClassifyModelWrapper(ClassifyModelWrapper):
    """
    根文件下包含train(必须)，test(可选), val(可选)文件夹

    Examples
    --------
    >>> model_wrapper = ImageClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(train_texts, y_train val_data, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    0.9876
    """

    test_dir: Path

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)
        self.test_dir = None
        self.imgsz = None
        self.transform = None

    def train(
        self,
        data: Union[str, Path],
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        train_transform=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if isinstance(data, str):
            data = Path(data)

        train_dir = data / "train"
        test_dir = data / "test"
        val_dir = data / "val"
        if not val_dir.exists():
            val_dir = data / "valid"

        assert train_dir.exists()
        train_transform = train_transform or transform or get_train_transform(imgsz)
        self.transform = transform or get_transform(imgsz)
        train_set = ImageFolder(train_dir, train_transform)
        self.classes = train_set.classes
        log_utils.info(f"Classes: {self.classes}")

        if val_dir.exists():
            val_set = ImageFolder(val_dir, self.transform)
            result = super().train(
                train_set,
                val_set,
                epochs=epochs,
                optimizer=optimizer,
                scheduler=scheduler,
                lr=lr,
                T_max=T_max,
                batch_size=batch_size,
                eval_batch_size=eval_batch_size,
                num_workers=num_workers,
                num_eval_workers=num_eval_workers,
                pin_memory=pin_memory,
                pin_memory_device=pin_memory_device,
                persistent_workers=persistent_workers,
                early_stopping_rounds=early_stopping_rounds,
                print_per_rounds=print_per_rounds,
                drop_last=drop_last,
                checkpoint_per_rounds=checkpoint_per_rounds,
                checkpoint_name=checkpoint_name,
                show_progress=show_progress,
                eps=eps,
            )
            if test_dir.exists():
                self.test_dir = test_dir
                test_set = ImageFolder(val_dir, transform)
                preds, targets = acc_predict_dataset(self.best_model, test_set, eval_batch_size, 0.5, self.device)
                preds, targets = preds.ravel(), targets.ravel()
                print(f"Test dataset accuracy: {accuracy_score(preds, targets):.2%}")
                print(f"Test dataset classification report:\n{classification_report(preds, targets, target_names=self.classes)}")
            return result
        elif test_dir.exists():
            self.test_dir = test_dir
            test_set = ImageFolder(test_dir, self.transform)
            result = super().train(
                train_set,
                test_set,
                epochs=epochs,
                optimizer=optimizer,
                scheduler=scheduler,
                lr=lr,
                T_max=T_max,
                batch_size=batch_size,
                eval_batch_size=eval_batch_size,
                num_workers=num_workers,
                num_eval_workers=num_eval_workers,
                pin_memory=pin_memory,
                pin_memory_device=pin_memory_device,
                persistent_workers=persistent_workers,
                early_stopping_rounds=early_stopping_rounds,
                print_per_rounds=print_per_rounds,
                drop_last=drop_last,
                checkpoint_per_rounds=checkpoint_per_rounds,
                checkpoint_name=checkpoint_name,
                show_progress=show_progress,
                eps=eps,
            )
            preds, targets = acc_predict_dataset(self.best_model, test_set, eval_batch_size, 0.5, self.device)
            preds, targets = preds.ravel(), targets.ravel()
            print(f"Test dataset accuracy: {accuracy_score(preds, targets):.2%}\n")
            print(f"Test dataset classification report:\n{classification_report(preds, targets, target_names=self.classes)}")
            return result
        return super().train(
            train_set,
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            num_workers=num_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
            monitor=monitor,
        )

    def predict(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> np.ndarray:
        """
        :param source:
        :param imgsz: 图片大小
        """
        logits = self.logits(source, imgsz, batch_size)
        return acc_predict(logits)

    def predict_classes(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> list:
        """
        :param source:
        :param imgsz: 图片大小
        """
        pred = self.predict(source, imgsz, batch_size)
        return self._predict_classes(pred.ravel())

    def predict_proba(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param source:
        :param imgsz: 图片大小
        """
        logits = self.logits(source, imgsz, batch_size)
        return self._proba(logits)

    def predict_classes_proba(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> Tuple[list, np.ndarray]:
        """
        :param source:
        :param imgsz: 图片大小
        """
        indices, values = self.predict_proba(source, imgsz, batch_size)
        return self._predict_classes(indices.ravel()), values

    def logits(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> torch.Tensor:
        imgsz = imgsz or self.imgsz 
        if imgsz:
            transform = transforms.Compose(
                [transforms.Resize(imgsz), transforms.ToTensor()]
            )
        else:
            if self.transform:
                transform = self.transform
            else:
                raise ValueError("Expected 'imgsz', but None")

        if isinstance(source, str):
            source = Path(source)
        if isinstance(source, Path):
            if source.is_file():
                source = Image.open(source)
            elif source.is_dir():
                source = (
                    img
                    for img in source.rglob("*")
                    if img.suffix in (".png", ".jpg", "jpeg") and img.is_file()
                )
                source = [transform(Image.open(s)).unsqueeze(0) for s in source]
                source = torch.cat(source, dim=0)
        if isinstance(source, Image.Image):
            source = transform(source)
            source = source.unsqueeze(0)

        return super().logits(source, batch_size)

    def evaluate(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        batch_size: int = 64,
        num_workers: int = 0,
    ) -> float:
        """return accuracy"""
        dataset = self._to_dataset(data, imgsz, transform)
        return super().evaluate(dataset, batch_size, num_workers, None)     
    
    def classification_report(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        batch_size: int = 64,
        num_workers: int = 0,
        target_names: Optional[List] = None,
    ) -> Union[str, dict]:
        dataset = self._to_dataset(data, imgsz, transform)
        return super().classification_report(dataset, batch_size, num_workers, target_names=target_names)
        
    def _to_dataset(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
    ) -> Dataset:
        data = data or self.test_dir
        if isinstance(data, (str, Path)):
            transform = transform or get_transform(imgsz)
            return ImageFolder(data, transform)
        elif isinstance(data, ImageFolder):
            data.transform = data.transform or get_transform(imgsz)

        return data


class SplitImageClassifyModelWrapper(ImageClassifyModelWrapper):
    """
    根文件下是分类文件夹

    Examples
    --------
    >>> model_wrapper = SplitImageClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(train_texts, y_train val_data, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    0.9876
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        data: Union[str, Path, ImageFolder],
        val_size=0.2,
        random_state: int = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        train_transform=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        assert 0.0 <= val_size < 1.0
        if val_size > 0.0:
            train_transform = train_transform or transform or get_train_transform(imgsz)
            if isinstance(data, (str, Path)):
                # (PIL.Image.Image, int)
                dataset = ImageFolder(root=data)
                self.transform = transform or get_transform(imgsz)
            elif isinstance(data, ImageFolder):
                dataset = data
                self.transform = (
                    transform or dataset.transform or get_train_transform(imgsz)
                )
            else:
                raise TypeError(
                    f"Expected str or Path or ImageFolder, but {type(data)}"
                )

            self.classes = dataset.classes
            # dataset.transform = None
            train_size = 1 - val_size
            if random_state is None:
                train_set, val_set = random_split(dataset, [train_size, val_size])
            else:
                generator = torch.Generator().manual_seed(random_state)
                train_set, val_set = random_split(dataset, [train_size, val_size], generator)
            train_set.dataset.transform = train_transform
            val_set.dataset.transform = self.transform
        else:
            val_set = None
            if isinstance(data, (str, Path)):
                train_set = ImageFolder(root=data, transform=train_transform)
            elif isinstance(data, ImageFolder):
                train_set = data
                train_set.transform = (
                    train_transform
                    or train_set.transform
                    or transform
                    or get_train_transform(imgsz)
                )
            self.classes = train_set.classes

        log_utils.info(f"Classes: {self.classes}")

        # 调用的是ImageClassifyModelWrapper父类ClassifyModelWrapper的train方法
        super(ImageClassifyModelWrapper, self).train(
            train_set,
            val_set,
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            eval_batch_size=eval_batch_size,
            num_workers=num_workers,
            num_eval_workers=num_eval_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
            monitor=monitor
        )
