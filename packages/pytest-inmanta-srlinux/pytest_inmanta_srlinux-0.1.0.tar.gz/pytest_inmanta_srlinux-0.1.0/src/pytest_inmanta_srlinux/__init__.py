"""
Copyright 2025 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import pathlib


def get_model(name: str = "basic.cf") -> str:
    """
    Get the model with the given name that is part of this library.

    :param name: The name of the model, including the .cf extension.
    """
    models_folder = pathlib.Path(__file__).parent / "models"
    model_file = models_folder / name
    if not model_file.is_file():
        raise LookupError(
            f"Can't find model {name} in {models_folder}, existing models are: "
            f"{[m.name for m in models_folder.glob('*.cf')]}"
        )

    # The model file exists, return its content
    return model_file.read_text()
