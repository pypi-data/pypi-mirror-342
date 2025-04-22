import json
from datetime import datetime
import numpy as np
from scipy.stats import ttest_rel
import logging

logging.basicConfig(level=logging.INFO)

class ExperimentTracker:
    _experiment_cache = {}
    _visualization_cache = {}

    def __init__(self, name: str, description: str = "", timestamp: str = None, version: int = 1, max_history_length: int = 10):
        self.name = name
        self.description = description
        self.timestamp = timestamp or datetime.now().isoformat()
        self.version = version
        self.params = {}
        self.metrics = {}
        self.tags = []
        self.history = []
        self.notifications = []
        self.max_history_length = max_history_length

    def get_tags(self):
        """Retrieve the tags of the experiment."""
        return self.tags

    def log_param(self, param_name: str, value):
        """Log a hyperparameter."""
        self.params[param_name] = value
        self._log_change("Parameter change", param_name, value)

    def log_metric(self, metric_name: str, value):
        """Log a metric."""
        self.metrics[metric_name] = value
        self._log_change("Metric change", metric_name, value)
        self._check_notifications(metric_name, value)

    def add_tag(self, tag: str):
        """Add a tag to the experiment."""
        if tag not in self.tags:
            self.tags.append(tag)
            self._log_change("Tag added", tag)

    def remove_tag(self, tag: str):
        """Remove a tag from the experiment."""
        if tag in self.tags:
            self.tags.remove(tag)
            self._log_change("Tag removed", tag)

    def _log_change(self, change_type: str, name: str, value=None):
        self.version += 1
        change = {
            "version": self.version,
            "change_type": change_type,
            "name": name,
            "value": value,
            "timestamp": datetime.now().isoformat(),
        }
        self.history.append(change)
        if len(self.history) > self.max_history_length:
            self.history = self.history[-self.max_history_length:]
        self._visualization_cache.clear()  # Clear cached visualization data


    def save(self, filepath: str):
        """Save experiment data to a JSON file."""
        experiment_data = {
            "name": self.name,
            "description": self.description,
            "timestamp": self.timestamp,
            "version": self.version,
            "parameters": self.params,
            "metrics": self.metrics,
            "tags": self.tags,
            "history": self.history,
        }
        with open(filepath, "w") as f:
            json.dump(experiment_data, f, indent=4)

    @classmethod
    def load(cls, filepath: str):
        """Load experiment data from a JSON file with caching."""
        if filepath in cls._experiment_cache:
            return cls._experiment_cache[filepath]
        with open(filepath, "r") as f:
            data = json.load(f)
        tracker = cls(data["name"], data["description"], data["timestamp"], data["version"])
        tracker.params = data["parameters"]
        tracker.metrics = data["metrics"]
        tracker.tags = data["tags"]
        tracker.history = data["history"]
        cls._experiment_cache[filepath] = tracker
        return tracker

    def get_version_history(self):
        """Get the history of all versions."""
        return self.history

    def rollback(self, version: int):
        """
        Revert the experiment to a specific version.
        
        Args:
            version (int): The target version to rollback to.
        """
        if version > self.version or version <= 0:
            raise ValueError("Invalid version number.")
        
        # Initialize to reconstruct state
        restored_params = {}
        restored_metrics = {}
        restored_tags = []
    
        # Reconstruct state from history
        for change in self.history:
            if change["version"] <= version:
                if change["change_type"] == "Parameter change":
                    restored_params[change["name"]] = change["value"]
                elif change["change_type"] == "Metric change":
                    restored_metrics[change["name"]] = change["value"]
                elif change["change_type"] == "Tag added":
                    if change["name"] not in restored_tags:
                        restored_tags.append(change["name"])
                elif change["change_type"] == "Tag removed":
                    if change["name"] in restored_tags:
                        restored_tags.remove(change["name"])
            else:
                break
    
        # Apply restored state
        self.params = restored_params
        self.metrics = restored_metrics
        self.tags = restored_tags
        self.version = version
    
    
    @staticmethod
    def filter_experiments(experiments, **criteria):
        def matches_criteria(exp, key, value):
            if callable(value):
                return value(getattr(exp, key, None))
            return getattr(exp, key, None) == value
    
        results = []
        for exp in experiments:
            if all(matches_criteria(exp, key, val) for key, val in criteria.items()):
                results.append(exp)
        return results
    

    @staticmethod
    def compare_experiments(exp1, exp2, metric_name):
        """
        Compare two experiments based on a given metric using a paired t-test.
        
        Args:
            exp1 (ExperimentTracker): First experiment.
            exp2 (ExperimentTracker): Second experiment.
            metric_name (str): The metric to compare.
        
        Returns:
            dict: Result of the paired t-test.
        """
        if metric_name not in exp1.metrics or metric_name not in exp2.metrics:
            raise ValueError(f"Metric {metric_name} not found in both experiments.")
        data1 = np.array(exp1.metrics[metric_name])
        data2 = np.array(exp2.metrics[metric_name])
        if data1.shape != data2.shape:
            raise ValueError("Metrics data must have the same shape for comparison.")
        t_stat, p_value = ttest_rel(data1, data2)
        return {
            "metric": metric_name,
            "t_stat": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    def set_notification(self, metric_name, condition, message):
        """
        Set a notification condition for a metric.
        
        Args:
            metric_name (str): The metric to monitor.
            condition (callable): A function that takes a value and returns True/False.
            message (str): Notification message if the condition is met.
        """
        self.notifications.append({
            "metric_name": metric_name,
            "condition": condition,
            "message": message
        })

    def _check_notifications(self, metric_name, value):
        """
        Check if any notification conditions are met for a metric.
        
        Args:
            metric_name (str): The metric being logged.
            value: The value of the metric.
        """
        for notification in self.notifications:
            if notification["metric_name"] == metric_name and notification["condition"](value):
                logging.info(f"Notification: {notification['message']}")

    def get_visualization_data(self, metrics_to_plot=None):
        """
        Retrieve preprocessed visualization data for the experiment.
        
        Args:
            metrics_to_plot (list): List of metrics to plot (optional).
        
        Returns:
            dict: Processed visualization data.
        """
        cache_key = tuple(metrics_to_plot or self.metrics.keys())
        if cache_key in self._visualization_cache:
            return self._visualization_cache[cache_key]
        visualization_data = {}
        for metric in metrics_to_plot or self.metrics.keys():
            visualization_data[metric] = [entry["value"] for entry in self.history if entry["change_type"] == "Metric change" and entry["name"] == metric]
        self._visualization_cache[cache_key] = visualization_data
        return visualization_data
