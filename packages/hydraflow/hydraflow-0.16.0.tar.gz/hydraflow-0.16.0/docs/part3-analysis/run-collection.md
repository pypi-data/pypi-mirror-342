# Run Collection

The [`RunCollection`][hydraflow.core.run_collection.RunCollection] class is a
powerful tool for working with multiple experiment runs. It provides methods
for filtering, grouping, and analyzing sets of [`Run`][hydraflow.core.run.Run]
instances, making it easy to compare and extract insights from your experiments.

## Creating a Run Collection

There are several ways to create a `RunCollection`:

```python
from hydraflow import Run, RunCollection
from pathlib import Path

# Method 1: Using Run.load with multiple paths
run_dirs = ["mlruns/exp_id/run_id1", "mlruns/exp_id/run_id2"]
runs = Run.load(run_dirs)

# Method 2: Using a generator expression
run_dirs = Path("mlruns/exp_id").glob("*")
runs = Run.load(run_dirs)

# Method 3: Creating from a list of Run instances
run1 = Run(Path("mlruns/exp_id/run_id1"))
run2 = Run(Path("mlruns/exp_id/run_id2"))
runs = RunCollection([run1, run2])

# Method 4: Using iter_run_dirs to find runs dynamically
from hydraflow import iter_run_dirs

# Find all runs in a tracking directory
tracking_dir = "mlruns"
runs = Run.load(iter_run_dirs(tracking_dir))

# Find runs from specific experiments
runs = Run.load(iter_run_dirs(tracking_dir, ["experiment1", "experiment2"]))

# Use pattern matching for experiment names
runs = Run.load(iter_run_dirs(tracking_dir, "transformer_*"))

# Use a custom filter function for experiment names
def is_recent_version(name: str) -> bool:
    return name.startswith("model_") and "v2" in name

runs = Run.load(iter_run_dirs(tracking_dir, is_recent_version))
```

## Basic Operations

The `RunCollection` class supports common operations for working with collections:

```python
# Check the number of runs
print(f"Number of runs: {len(runs)}")

# Iterate over runs
for run in runs:
    print(f"Run ID: {run.info.run_id}")

# Access individual runs by index
first_run = runs[0]
last_run = runs[-1]

# Slice the collection
subset = runs[1:4]  # Get runs 1, 2, and 3
```

## Filtering Runs

One of the most powerful features of `RunCollection` is the ability to filter
runs based on configuration parameters or other criteria:

```python
# Filter by exact parameter value
transformer_runs = runs.filter(model_type="transformer")

# Filter with multiple conditions (AND logic)
specific_runs = runs.filter(
    model_type="transformer",
    learning_rate=0.001,
    batch_size=32
)

# Filter with dot notation for nested parameters
# Use a tuple to specify the parameter name and value
nested_filter = runs.filter(("model.hidden_size", 512))

# Filter with double underscore notation for nested parameters
# This is often more convenient with keyword arguments
nested_filter = runs.filter(model__hidden_size=512)  # Equivalent to "model.hidden_size"
nested_filter = runs.filter(model__encoder__num_layers=6)  # For deeply nested parameters

# Filter with tuple for range values (inclusive)
lr_range = runs.filter(learning_rate=(0.0001, 0.01))

# Filter with list for multiple allowed values (OR logic)
multiple_models = runs.filter(model_type=["transformer", "lstm"])

# Filter by a predicate function
def is_large_image(run: Run):
    return run.get("width") + run.get("height") > 100

good_runs = runs.filter(predicate=is_large_image)
```

The double underscore notation (`__`) is particularly useful for accessing nested
configuration parameters with keyword arguments, as it's automatically converted to
dot notation (`.`) internally. This allows you to write more natural and Pythonic
filtering expressions, especially for deeply nested configurations.

## Advanced Filtering

The `filter` method supports more complex filtering patterns:

```python
# Combine different filter types
complex_filter = runs.filter(
    model_type=["transformer", "lstm"],
    learning_rate=(0.0001, 0.01),
    batch_size=32
)

# Chained filtering
final_runs = runs.filter(model_type="transformer").filter(learning_rate=0.001)

# Advanced filtering using predicate functions with callable defaults
# This example filters runs based on learning rate efficiency (lr * batch_size)
# Even if some runs are missing one parameter, the default logic provides values
def has_efficient_lr(run: Run) -> bool:
    lr = run.get("learning_rate", default=lambda r: r.get("base_lr", 0.01) * r.get("lr_multiplier", 1.0))
    batch_size = run.get("batch_size", default=lambda r: r.get("default_batch_size", 32))
    return lr * batch_size < 0.5

# Apply the complex predicate
efficient_runs = runs.filter(predicate=has_efficient_lr)
```

The combination of predicate functions with callable defaults in `get` enables sophisticated
filtering logic that can handle missing parameters and varied configuration schemas across
different experiment runs.

## Sorting Runs

The `sort` method allows you to sort runs based on specific criteria:

```python
# Sort by accuracy in descending order
runs.sort("learning_rate", reverse=True)

# Sort by multiple keys
runs.sort("learning_rate", "model_type")
```

## Getting Individual Runs

While `filter` returns a `RunCollection`, the `get` method returns a single
`Run` instance that matches the criteria:

```python
# Get a specific run (raises error if multiple or no matches are found)
best_run = runs.get(model_type="transformer", learning_rate=0.001)

# Try to get a specific run. If no match is found, return None
fallback_run = runs.try_get(model_type="transformer")

# Get the first matching run.
first_match = runs.first(model_type="transformer")

# Get the last matching run.
last_match = runs.last(model_type="transformer")
```

## Extracting Data

RunCollection provides several methods to extract specific data from runs:

```python
# Extract values for a specific key as a list
learning_rates = runs.to_list("learning_rate")

# Extract values with a static default for missing values
batch_sizes = runs.to_list("batch_size", default=32)

# Extract values with a callable default that dynamically computes values
# This is particularly useful for handling missing parameters or derived values
accuracies = runs.to_list("accuracy", default=lambda run: run.get("val_accuracy", 0.0) * 0.9)

# Extract values as a NumPy array
batch_sizes = runs.to_numpy("batch_size")

# Extract with callable default for complex scenarios
learning_rates = runs.to_numpy(
    "learning_rate",
    default=lambda run: run.get("base_lr", 0.01) * run.get("lr_schedule_factor", 1.0)
)

# Extract values as a Polars Series
lr_series = runs.to_series("learning_rate")

# Extract with a custom name for the series
model_series = runs.to_series("model_type", name="Model Architecture")

# Extract with callable default and custom name
effective_lr = runs.to_series(
    "learning_rate",
    default=lambda run: run.get("base_lr", 0.01) * run.get("lr_multiplier", 1.0),
    name="Effective Learning Rate"
)

# Use Series for further analysis and operations
import polars as pl
# Combine multiple series into a DataFrame
df = pl.DataFrame([
    runs.to_series("model_type", name="Model"),
    runs.to_series("batch_size", default=32, name="Batch Size"),
    effective_lr
])
# Perform operations between Series
normalized_acc = runs.to_series("accuracy", default=0.0, name="Accuracy")
efficiency = normalized_acc / effective_lr  # Series division

# Get unique values for a key
model_types = runs.unique("model_type")

# Count unique values
num_model_types = runs.n_unique("model_type")
```

All data extraction methods (`to_list`, `to_numpy`, `to_series`, etc.) support both static and callable default values,
matching the behavior of the `Run.get` method. When using a callable default, the function receives
the Run instance as an argument, allowing you to:

- Implement fallback logic for missing parameters
- Create derived values based on multiple parameters
- Handle varying configuration schemas across different experiments
- Apply transformations to the raw parameter values

This makes it much easier to work with heterogeneous collections of runs that might have different
parameter sets or evolving configuration schemas.

## Converting to DataFrame

For advanced analysis, you can convert your runs to a Polars DataFrame:

```python
# DataFrame with run information and entire configuration
df = runs.to_frame()

# DataFrame with specific configuration parameters
df = runs.to_frame("model_type", "learning_rate", "batch_size")

# Specify default values for missing parameters using the defaults parameter
df = runs.to_frame(
    "model_type",
    "learning_rate",
    "batch_size",
    defaults={"learning_rate": 0.01, "batch_size": 32}
)

# Use callable defaults for dynamic values based on each run
df = runs.to_frame(
    "model_type",
    "learning_rate",
    "epochs",
    defaults={
        "learning_rate": lambda run: run.get("base_lr", 0.01) * run.get("lr_multiplier", 1.0),
        "epochs": lambda run: int(run.get("max_steps", 1000) / run.get("steps_per_epoch", 100))
    }
)

# Missing values without defaults are represented as None (null) in the DataFrame
# This allows for standard handling of missing data in Polars
missing_values_df = runs.to_frame("model_type", "parameter_that_might_be_missing")

# Filter rows with non-null values
import polars as pl
valid_rows = missing_values_df.filter(pl.col("parameter_that_might_be_missing").is_not_null())

# Fill null values after creating the DataFrame
filled_df = missing_values_df.with_columns(
    pl.col("parameter_that_might_be_missing").fill_null("default_value")
)

# Using a custom function that returns multiple columns as keyword arguments
def get_metrics(run: Run) -> dict[str, float]:
    return {
        "accuracy": run.get("accuracy", default=lambda r: r.get("val_accuracy", 0.0) * 0.9),
        "precision": run.get("precision", default=lambda r: r.get("val_precision", 0.0) * 0.9),
    }

# Add custom columns using a function
df = runs.to_frame("model_type", metrics=get_metrics)

# Combine defaults with custom column generator functions
df = runs.to_frame(
    "model_type",
    "learning_rate",
    defaults={"learning_rate": 0.01},
    metrics=get_metrics
)
```

The `to_frame` method provides several ways to handle missing data:

1. **defaults parameter**: Provide static or callable default values for specific keys
   - Static values: `defaults={"param": value}`
   - Callable values: `defaults={"param": lambda run: computed_value}`

2. **None values**: Parameters without defaults are represented as `None` (null) in the DataFrame
   - This lets you use Polars operations for handling null values:
     - Filter: `df.filter(pl.col("param").is_not_null())`
     - Fill nulls: `df.with_columns(pl.col("param").fill_null(value))`
     - Aggregations: Most aggregation functions handle nulls appropriately

3. **Custom column generators**: Use keyword argument functions to compute complex columns
   - These functions receive each Run instance and can implement custom logic
   - They can use `run.get()` with defaults to handle missing parameters

These approaches can be combined to create flexible and robust data extraction pipelines
that handle different experiment configurations and parameter evolution over time.

## Grouping Runs

The `group_by` method allows you to organize runs based on parameter values:

```python
# Group by a single parameter
model_groups = runs.group_by("model_type")

# Group by nested parameter using dot notation
architecture_groups = runs.group_by("model.architecture")

# Iterate through groups
for model_type, group in model_groups.items():
    print(f"Model type: {model_type}, Runs: {len(group)}")

# Group by multiple parameters
param_groups = runs.group_by("model_type", "learning_rate")

# Mix of regular and nested parameters using double underscore notation
param_groups = runs.group_by("model_type", "model__hidden_size", "optimizer__learning_rate")

# Access a specific group
transformer_001_group = param_groups[("transformer", 0.001)]
```

When no aggregation functions are provided, `group_by` returns a dictionary mapping keys to `RunCollection` instances. This intentional design allows you to:

- Work with each group as a separate `RunCollection` with all the filtering, sorting, and analysis capabilities
- Perform custom operations on each group that might not be expressible as simple aggregation functions
- Chain additional operations on specific groups that interest you
- Implement multi-stage analysis workflows where you need to maintain the full run information at each step

This approach preserves all information in each group, giving you maximum flexibility for downstream analysis.

## Aggregation with Group By

Combine `group_by` with aggregation for powerful analysis:

```python
# Simple aggregation function using get method with callable defaults
def mean_accuracy(runs: RunCollection) -> float:
    return runs.to_numpy(
        "accuracy",
        default=lambda run: run.get("val_accuracy", 0.0) * 0.9
    ).mean()

# Complex aggregation from implementation or configuration with fallbacks
def combined_metric(runs: RunCollection) -> float:
    # Use callable defaults to handle missing values consistently
    accuracies = runs.to_numpy("accuracy", default=lambda r: r.get("val_accuracy", 0.0))
    precisions = runs.to_numpy("precision", default=lambda r: r.get("val_precision", 0.0))
    return (accuracies.mean() + precisions.mean()) / 2


# Group by model type and calculate average accuracy
model_accuracies = runs.group_by(
    "model_type",
    accuracy=mean_accuracy
)

# Group by multiple parameters with multiple aggregations
results = runs.group_by(
    "model_type",
    "learning_rate",
    count=len,
    accuracy=mean_accuracy,
    combined=combined_metric
)

# Group by parameters that might be missing in some runs using callable defaults
def normalize_architecture(run: Run) -> str:
    # Get architecture with a fallback to model type if not available
    arch = run.get("architecture", default=lambda r: r.get("model_type", "unknown"))
    return arch.lower()  # Normalize to lowercase

# Group by the normalized architecture
arch_results = runs.group_by(normalize_architecture, accuracy=mean_accuracy)
```

With the enhanced `get` method and callable defaults support throughout the API, writing aggregation
functions becomes more straightforward and robust. You can handle missing values consistently and
implement complex transformations that work across heterogeneous runs.

When aggregation functions are provided as keyword arguments, `group_by` returns a Polars DataFrame with the group keys and aggregated values. This design choice offers several advantages:

- Directly produces analysis-ready results with all aggregations computed in a single operation
- Enables efficient downstream analysis using Polars' powerful DataFrame operations
- Simplifies visualization and reporting workflows
- Reduces memory usage by computing only the requested aggregations rather than maintaining full RunCollections
- Creates a clean interface that separates grouping from additional analysis steps

The DataFrame output is particularly useful for final analysis steps where you need to summarize results across many runs or prepare data for visualization.

## Type-Safe Run Collections

Like the `Run` class, `RunCollection` supports type parameters for better
IDE integration:

```python
from dataclasses import dataclass
from hydraflow import Run, RunCollection

@dataclass
class ModelConfig:
    type: str
    hidden_size: int

@dataclass
class Config:
    model: ModelConfig
    learning_rate: float
    batch_size: int

# Create a typed RunCollection
run_dirs = ["mlruns/exp_id/run_id1", "mlruns/exp_id/run_id2"]
runs = Run[Config].load(run_dirs)

# Type-safe access in iterations
for run in runs:
    # IDE will provide auto-completion
    model_type = run.cfg.model.type
    lr = run.cfg.learning_rate
```

## Implementation-Aware Collections

You can also create collections with custom implementation classes:

```python
class ModelAnalyzer:
    def __init__(self, artifacts_dir: Path, cfg: Config | None = None):
        self.artifacts_dir = artifacts_dir
        self.cfg = cfg

    def load_model(self):
        # Load the model from artifacts
        pass

    def evaluate(self, data):
        # Evaluate the model
        pass

# Create a collection with implementation
runs = Run[Config, ModelAnalyzer].load(run_dirs, ModelAnalyzer)

# Access implementation methods
for run in runs:
    model = run.impl.load_model()
    results = run.impl.evaluate(test_data)
```

## Best Practices

1. **Filter Early**: Apply filters as early as possible
   to reduce the number of runs you're working with.

2. **Use Type Parameters**: Specify
   configuration/implementation types
   with `Run[Config]` or `Run[Config, Impl]` and
   use `load` method to collect runs for better IDE support and
   type checking.

3. **Chain Operations**: Combine filtering, grouping,
   and aggregation for efficient analysis workflows.

4. **Use DataFrame Integration**: Convert to DataFrames
   for complex analysis and visualization needs.

## Summary

The [`RunCollection`][hydraflow.core.run_collection.RunCollection] class is a
powerful tool for comparative analysis of machine learning experiments. Its
filtering, grouping, and aggregation capabilities enable efficient extraction
of insights from large sets of experiments, helping you identify optimal
configurations and understand performance trends.