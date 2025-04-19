from keras import layers, models
from flwr.server.strategy import Strategy, FedAvg

from netfl.core.task import Dataset, Task, TrainConfig, DatasetInfo


class MNIST(Task):
    def dataset_info(self) -> DatasetInfo:
        return DatasetInfo(
            huggingface_path="ylecun/mnist",
            item_name="image",
            label_name="label",
        )

    def dataset(self, raw_dataset: Dataset) -> Dataset:
        normalized_dataset = Dataset(
            x_train=(raw_dataset.x_train / 255.0),
            x_test=(raw_dataset.x_test / 255.0),
            y_train=raw_dataset.y_train,
            y_test=raw_dataset.y_test,
        )
        return normalized_dataset

    def model(self) -> models.Model:
        model = models.Sequential([
            layers.Input(shape=(28, 28)),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(10, activation="softmax")
        ])
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        return model

    def aggregation_strategy(self) -> Strategy:
        return self._aggregation_strategy_factory(FedAvg)
    
    def train_config(self) -> TrainConfig:
	    return TrainConfig(
            batch_size=32,
            epochs=1,
            fraction_evaluate=1.0,
            fraction_fit=1.0,
            learning_rate=0.001,
            min_available=4,
            max_available=4,
            num_rounds=10,
            seed=42,
            shuffle=True,
            test_size=0.2,
        )


class MainTask(MNIST):
    pass
