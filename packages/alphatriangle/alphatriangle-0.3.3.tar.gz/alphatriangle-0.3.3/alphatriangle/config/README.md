# File: alphatriangle/config/README.md
# Configuration Module (`alphatriangle.config`)

## Purpose and Architecture

This module centralizes all configuration parameters for the AlphaTriangle project. It uses separate **Pydantic models** for different aspects of the application (environment, model, training, visualization, persistence) to promote modularity, clarity, and automatic validation.

-   **Modularity:** Separating configurations makes it easier to manage parameters for different components.
-   **Type Safety & Validation:** Using Pydantic models (`BaseModel`) provides strong type hinting, automatic parsing, and validation of configuration values based on defined types and constraints (e.g., `Field(gt=0)`).
-   **Validation Script:** The [`validation.py`](validation.py) script instantiates all configuration models, triggering Pydantic's validation, and prints a summary.
-   **Dynamic Defaults:** Some configurations, like `RUN_NAME` in `TrainConfig`, use `default_factory` for dynamic defaults (e.g., timestamp).
-   **Computed Fields:** Properties like `ACTION_DIM` in `EnvConfig` or `MLFLOW_TRACKING_URI` in `PersistenceConfig` are defined using `@computed_field` for clarity.
-   **Tuned Defaults:** The default values in `TrainConfig` and `ModelConfig` are now tuned for **more substantial learning runs** compared to the previous quick-testing defaults.

## Exposed Interfaces

-   **Pydantic Models:**
    -   [`EnvConfig`](env_config.py): Environment parameters (grid size, shapes).
    -   [`ModelConfig`](model_config.py): Neural network architecture parameters. **Defaults tuned for larger capacity.**
    -   [`TrainConfig`](train_config.py): Training loop hyperparameters (batch size, learning rate, workers, **PER settings**, etc.). **Defaults tuned for longer runs.**
    -   [`VisConfig`](vis_config.py): Visualization parameters (screen size, FPS, layout).
    -   [`PersistenceConfig`](persistence_config.py): Data saving/loading parameters (directories, filenames).
    -   [`MCTSConfig`](mcts_config.py): MCTS parameters (simulations, exploration constants, temperature).
-   **Constants:**
    -   [`APP_NAME`](app_config.py): The name of the application.
-   **Functions:**
    -   `print_config_info_and_validate(mcts_config_instance: MCTSConfig)`: Validates and prints a summary of all configurations by instantiating the Pydantic models.

## Dependencies

This module primarily defines configurations and relies heavily on **Pydantic**.

-   **`pydantic`**: The core library used for defining models and validation.
-   **Standard Libraries:** `typing`, `time`, `os`, `logging`, `pathlib`.

---

**Note:** Please keep this README updated when adding, removing, or significantly modifying configuration parameters or the structure of the Pydantic models. Accurate documentation is crucial for maintainability.