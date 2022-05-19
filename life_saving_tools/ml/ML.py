from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)
from life_saving_tools import Notification
from sklearn.model_selection import GridSearchCV
import shelve
import matplotlib.pyplot as plt
import seaborn as sns


class Performance:
    """This module provides tool for keeping track of performance metrics \\
        using the shelve module. But of course, it can be used for other purposes\\
        too. Available methods are:

        - load_dict(dict_name)
        - update_dict(dictionary, dict_name)
        - get_all_dicts()
        - save_dict()
    """

    def __init__(self, filename, name="main_dict") -> None:
        """Instantiate the Performance class

        Parameters
        ----------
        filename : string
            the name of the shelve file to save the dictionary to
        name : string
            the name of the dictionary to save to the shelve file
            defualt is "main_dict". This is also the name for variable
            used to store the main dictionary

        Returns
        -------
        None
        """
        self.filename = filename
        self.name = name
        shelve_dict = shelve.open(self.filename)
        try:
            self.main_dict = shelve_dict[self.name]
        except KeyError:
            self.main_dict = {}

    def load_dict(self, dict_name):
        """
        This function loads the a dictionary with given `dict_name` from a shelve file.
        If the dictionary does not exist, it will return an empty dictionary.

        Parameters
        ----------
        dict_name : string
            the name of the dictionary to load

        Returns
        -------
        dictionary : dictionary
        """
        try:
            dictionary = self.main_dict[dict_name]
        except:
            dictionary = {}
        return dictionary

    def update_dict(self, dictionary, dict_name):
        """Updates the `main_dict`

        Parameters
        ----------
        dictionary : dictionary
            the dictionary to update the main_dict with
        dict_name : string
            the name of the dictionary to update
        """
        self.main_dict[dict_name] = dictionary

    def get_all_dicts(self):
        """Gets a list of all dictionaries available

        Parameters
        ----------
        None

        Returns
        -------
        list
            a list of all dictionaries available
        """
        return list(self.main_dict.keys())

    def save_dict(self):
        """
        This function saves the model_performance dictionary to a shelve file.

        Parameters
        ----------
        file : string
            the name of the shelve file to save the dictionary to

        Returns
        -------
        None
        """
        shelve_dict = shelve.open(self.filename)
        shelve_dict[self.name] = self.main_dict
        shelve_dict.close()
        print("Saved dictionary to file: {}".format(self.filename))


class Modeling:
    """A class for tracking things while experimenting with models"""

    def __init__(
        self,
        model,
        X_train=None,
        y_train=None,
        X_test=None,
        y_test=None,
        X_dev=None,
        y_dev=None,
        filepath="model_performance",
    ) -> None:
        """Instantiate the Modeling class

        Parameters
        ----------
        model : sklearn model
            the model to use
        X_train : numpy array
            the training data
        y_train : numpy array
            the training labels
        X_test : numpy array
            the testing data
        y_test : numpy array
            the testing labels
        X_dev : numpy array
            the development data
        y_dev : numpy array
            the development labels
        filepath : string
            the path to the shelve file to save the dictionary to
            defualt is "model_performance".

        Returns
        -------
        None

        """
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.X_dev = X_dev
        self.y_dev = y_dev
        self.filepath = filepath
        self.n = Notification.Notification()
        self.d = Performance(self.filepath)
        self.test_performance = self.d.load_dict("test_performance")
        self.train_performance = self.d.load_dict("train_performance")
        self.dev_performance = self.d.load_dict("dev_performance")

    def _get_data_(self, data):
        if data.lower() == "train":
            return self.X_train, self.y_train
        elif data.lower() == "test":
            return self.X_test, self.y_test
        elif data.lower() == "dev":
            return self.X_dev, self.y_dev

    def _get_dict_(self, data):
        if data.lower() == "train":
            return self.train_performance
        elif data.lower() == "test":
            return self.test_performance
        elif data.lower() == "dev":
            return self.dev_performance

    def perform_grid_search(
        self,
        params,
        data="train",
        scoring="accuracy",
        text=False,
        play=True,
        cv=5,
        **kwargs,
    ):
        """
        Performs grid serach on the model and returns the best model with parameters.

        Parameters
        ----------
        model : sklearn model

        data : string
            the data to perform grid search on.
            default is "train". Allowed values are "train", "test", "dev"

        params : dictionary
            the parameters to search over
            defualt is params

        text : boolean
            if True, a notification is sent to whatsapp
            defualt is False

        play : boolean
            if True, music is played
            defualt is True

        cv : number of folds for cross validation
            defualt is 5

        scoring : scoring metric
            defualt is 'accuracy'

        **kwargs : keyword arguments
            keyword arguments to pass to GridSearchCV

        Returns
        -------
        grid_search : sklearn GridSearchCV object
        """
        grid = GridSearchCV(self.model, params, cv=cv, scoring=scoring, **kwargs)
        X, y = self._get_data_(data)
        grid.fit(X, y)

        best_estimator = grid.best_estimator_
        best_params = grid.best_params_
        best_score = grid.best_score_
        message = f"""Following is the best model and its parameters:
        Best Model:\n{best_estimator}\nBest params:
        \n{best_params}\nBest score: {best_score}"""

        if text:
            self.n.send_whatsapp_text(message)

        if play:
            self.n.play_n_stop()
        print(message)
        return grid

    def visualize_classification_model(
        self,
        data="test",
    ):
        """
        This function plots the confusion metrics and classification report

        Parameters
        ----------
        model : sklearn model

        Returns
        -------
        None
        """
        X, y = self._get_data_(data)
        # predicting on the data
        y_pred = self.model.predict(X)

        # Printing the classification report
        print(classification_report(y, y_pred))

        # Confusion matrix
        cm = confusion_matrix(y, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d")
        plt.show()

    def evaluate_classification_model(self, model_name=None, final=False, data="test"):
        """
        The function takes a model as input and creats a dictionary with the model's \\
            accuracy, precision, recall, f1 score, and roc_auc_score and add them to the \\
            `model_performance` dictionary and returns it. The `model_performance` dictionary \\
            is instantiated just before this function is created.

        Parameters
        ----------
        model : sklearn model

        model_name : string
            the name of the model to store as a key in the `model_performance` dictionary

        final : boolean
            if True, the scores are added to the `model_performance` dictionary as well

        Returns
        -------
        model_performance : dictionary
        """
        X, y = self._get_data_(data)
        # Making predictions on the test set
        y_pred = self.model.predict(X)

        # Getting the metrics
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred)
        recall = recall_score(y, y_pred)
        f1 = f1_score(y, y_pred)
        roc_auc = roc_auc_score(y, y_pred)
        performance = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "roc_auc": roc_auc,
        }

        if final:
            # Adding the metrics to the model_performance dictionary
            if model_name is None:
                model_name = type(self.model).__name__

            self._get_dict_(data)[model_name] = performance
            self.d.update_dict(self._get_dict_(data), f"{data}_performance")
            self.d.save_dict()
            return performance
        else:
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "roc_auc": roc_auc,
            }
