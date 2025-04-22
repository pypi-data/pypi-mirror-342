"""
Standardized result objects for experiment test results.
These classes implement the interface defined in interfaces.py.
Reporting functionality has been removed in this version.
"""

import typing as t
from pathlib import Path
import json
from datetime import datetime

from deepbridge.core.experiment.interfaces import TestResult, ModelResult
from deepbridge.core.experiment.dependencies import check_dependencies

class BaseTestResult(TestResult):
    """Base implementation of the TestResult interface"""
    
    def __init__(self, name: str, results: dict, metadata: t.Optional[dict] = None):
        """
        Initialize with test results
        
        Args:
            name: Name of the test
            results: Raw results dictionary
            metadata: Additional metadata about the test
        """
        self._name = name
        self._results = results
        self._metadata = metadata or {}
        
    @property
    def name(self) -> str:
        """Get the name of the test"""
        return self._name
    
    @property
    def results(self) -> dict:
        """Get the raw results dictionary"""
        return self._results
    
    @property
    def metadata(self) -> dict:
        """Get the test metadata"""
        return self._metadata
    
    def to_dict(self) -> dict:
        """Convert test result to a dictionary format"""
        return {
            'name': self.name,
            'results': self.results,
            'metadata': self.metadata
        }


class RobustnessResult(BaseTestResult):
    """Result object for robustness tests"""
    
    def __init__(self, results: dict, metadata: t.Optional[dict] = None):
        super().__init__("Robustness", results, metadata)


class UncertaintyResult(BaseTestResult):
    """Result object for uncertainty tests"""
    
    def __init__(self, results: dict, metadata: t.Optional[dict] = None):
        super().__init__("Uncertainty", results, metadata)


class ResilienceResult(BaseTestResult):
    """Result object for resilience tests"""
    
    def __init__(self, results: dict, metadata: t.Optional[dict] = None):
        super().__init__("Resilience", results, metadata)


class HyperparameterResult(BaseTestResult):
    """Result object for hyperparameter tests"""
    
    def __init__(self, results: dict, metadata: t.Optional[dict] = None):
        super().__init__("Hyperparameter", results, metadata)


class ExperimentResult:
    """
    Container for all test results from an experiment.
    Includes HTML report generation functionality.
    """
    
    def __init__(self, experiment_type: str, config: dict):
        """
        Initialize with experiment metadata
        
        Args:
            experiment_type: Type of experiment
            config: Experiment configuration
        """
        self.experiment_type = experiment_type
        self.config = config
        self.results = {}
        self.generation_time = datetime.now()
        
    def add_result(self, result: TestResult):
        """Add a test result to the experiment"""
        self.results[result.name.lower()] = result
        
    def get_result(self, name: str) -> t.Optional[TestResult]:
        """Get a specific test result by name"""
        return self.results.get(name.lower())
        
    def save_html(self, test_type: str, file_path: str, model_name: str = "Model") -> str:
        """
        Generate and save an HTML report for the specified test.
        
        Args:
            test_type: Type of test ('robustness', 'uncertainty', 'resilience', 'hyperparameter')
            file_path: Path where the HTML report will be saved (relative or absolute)
            model_name: Name of the model for display in the report
            
        Returns:
            Path to the generated report file
            
        Raises:
            ValueError: If test results not found or report generation fails
        """
        # Import report manager
        from deepbridge.core.experiment.report_manager import ReportManager
        import os
        
        # Convert test_type to lowercase for consistency
        test_type = test_type.lower()
        
        # Check if we have results for this test type
        # Handle the case where hyperparameters is plural but the key is singular
        lookup_key = test_type
        if test_type == "hyperparameters":
            lookup_key = "hyperparameter"
            
        result = self.results.get(lookup_key)
        if not result:
            raise ValueError(f"No {test_type} test results found. Run the test first.")
        
        # Initialize report manager
        report_manager = ReportManager()
        
        # Get the results dictionary
        if hasattr(result, 'to_dict'):
            results_dict = result.to_dict()['results']  # Extract the 'results' key from TestResult.to_dict()
        else:
            results_dict = result.results
            
        # Add experiment config if not present
        if 'config' not in results_dict:
            results_dict['config'] = self.config
            
        # Add experiment type
        results_dict['experiment_type'] = self.experiment_type
        
        # Add model_type directly - using the value from the primary model if available
        if 'primary_model' in results_dict and 'model_type' in results_dict['primary_model']:
            results_dict['model_type'] = results_dict['primary_model']['model_type']
        
        # Ensure file_path is absolute
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
            
        # Generate the report
        try:
            report_path = report_manager.generate_report(
                test_type=test_type,
                results=results_dict,
                file_path=file_path,
                model_name=model_name
            )
            return report_path
        except NotImplementedError:
            raise ValueError(f"HTML report generation for {test_type} tests is not yet implemented.")
    
    def to_dict(self) -> dict:
        """Convert all results to a dictionary"""
        result_dict = {
            'experiment_type': self.experiment_type,
            'config': self.config,
            'generation_time': self.generation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'tests_performed': list(self.results.keys())
        }
        
        # Add each test's results to the dictionary
        for name, result in self.results.items():
            result_dict[name] = self._clean_results_dict(result.results)
            
        return result_dict
    
    def _clean_results_dict(self, results_dict: dict) -> dict:
        """Clean the results dictionary by removing redundant information"""
        # Create a deep copy to avoid modifying the original
        import copy
        cleaned = copy.deepcopy(results_dict)
        
        # Handle primary model cleanup
        if 'primary_model' in cleaned:
            primary = cleaned['primary_model']
            
            # Remove redundant metrics entries
            if 'metrics' in primary and 'base_score' in primary['metrics']:
                # If base_score is duplicated in metrics, remove it
                if primary.get('base_score') == primary['metrics'].get('base_score'):
                    del primary['metrics']['base_score']
            
            # Remove metric name if metrics are present (since it's redundant)
            if 'metric' in primary and 'metrics' in primary:
                del primary['metric']
        
        # Handle alternative models cleanup
        if 'alternative_models' in cleaned:
            for model_name, model_data in cleaned['alternative_models'].items():
                # Remove redundant metrics entries
                if 'metrics' in model_data and 'base_score' in model_data['metrics']:
                    # If base_score is duplicated in metrics, remove it
                    if model_data.get('base_score') == model_data['metrics'].get('base_score'):
                        del model_data['metrics']['base_score']
                
                # Remove metric name if metrics are present
                if 'metric' in model_data and 'metrics' in model_data:
                    del model_data['metric']
        
        return cleaned
    
    def to_dict(self) -> dict:
        """
        Convert all results to a dictionary for serialization.
        This replaces the deprecated HTML report generation.
        
        Returns:
            Complete dictionary representation of experiment results
        """
        result_dict = {
            'experiment_type': self.experiment_type,
            'config': self.config,
            'generation_time': self.generation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'tests_performed': list(self.results.keys())
        }
        
        # Add each test's results to the dictionary
        for name, result in self.results.items():
            result_dict[name] = self._clean_results_dict(result.results)
            
        return result_dict
    
    @classmethod
    def from_dict(cls, results_dict: dict) -> 'ExperimentResult':
        """
        Create an ExperimentResult instance from a dictionary
        
        Args:
            results_dict: Dictionary containing test results
            
        Returns:
            ExperimentResult instance
        """
        experiment_type = results_dict.get('experiment_type', 'binary_classification')
        config = results_dict.get('config', {})
        
        # Create instance
        instance = cls(experiment_type, config)
        
        # Add test results
        if 'robustness' in results_dict:
            instance.add_result(RobustnessResult(results_dict['robustness']))
            
        if 'uncertainty' in results_dict:
            instance.add_result(UncertaintyResult(results_dict['uncertainty']))
            
        if 'resilience' in results_dict:
            instance.add_result(ResilienceResult(results_dict['resilience']))
            
        if 'hyperparameters' in results_dict:
            instance.add_result(HyperparameterResult(results_dict['hyperparameters']))
            
        return instance


def create_test_result(test_type: str, results: dict, metadata: t.Optional[dict] = None) -> TestResult:
    """
    Factory function to create the appropriate test result object
    
    Args:
        test_type: Type of test ('robustness', 'uncertainty', etc.)
        results: Raw test results
        metadata: Additional test metadata
        
    Returns:
        TestResult instance
    """
    test_type = test_type.lower()
    
    if test_type == 'robustness':
        return RobustnessResult(results, metadata)
    elif test_type == 'uncertainty':
        return UncertaintyResult(results, metadata)
    elif test_type == 'resilience':
        return ResilienceResult(results, metadata)
    elif test_type == 'hyperparameters' or test_type == 'hyperparameter':
        return HyperparameterResult(results, metadata)
    else:
        return BaseTestResult(test_type.capitalize(), results, metadata)


def wrap_results(results_dict: dict) -> ExperimentResult:
    """
    Wrap a dictionary of results in an ExperimentResult object
    
    Args:
        results_dict: Dictionary with test results
        
    Returns:
        ExperimentResult instance
    """
    return ExperimentResult.from_dict(results_dict)

# Import model results
try:
    from deepbridge.core.experiment.model_result import (
        BaseModelResult, ClassificationModelResult, RegressionModelResult, 
        create_model_result
    )
except ImportError:
    # Provide simplified implementations if model_result.py is not available
    class BaseModelResult:
        """Simplified model result implementation"""
        def __init__(self, model_name, model_type, metrics, **kwargs):
            self.model_name = model_name
            self.model_type = model_type
            self.metrics = metrics
            
    def create_model_result(model_name, model_type, metrics, **kwargs):
        """Simplified factory function"""
        return BaseModelResult(model_name, model_type, metrics, **kwargs)