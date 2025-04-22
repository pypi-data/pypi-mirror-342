from pathlib import Path
from huggingface_hub import HfApi, login, add_collection_item


MODEL_NAMES = {
    "context": [
        "microsoft/Phi-4-mini-instruct",
        "meta-llama/Llama-3.1-8B-Instruct",
        "google/gemma-3-4b-it",
        "Qwen/Qwen2.5-7B-Instruct",
    ],
    "thought": [
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    ],
}


HF_TOKEN = "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"
COLLECTION_SLUG = "madrylab/at2-67f28846e63e1832cb208427"

README_TEMPLATE = """
---
license: mit
---

# AT2 Score Estimator for `{model_name}`

This model is an AT2 score estimator that predicts the influence of a particular source on a model's generation.
To use it, check out the `at2` package: https://github.com/madryLab/AT2
"""


PRIVATE = False


login(token=HF_TOKEN)
for model_type in MODEL_NAMES:
    for model_name in MODEL_NAMES[model_type]:
        formatted_model_name = model_name.split("/")[-1].lower()
        repo_name = f"madrylab/at2-{formatted_model_name}"
        local_path = f"outputs/{model_type}_{formatted_model_name}/estimators/default"

        readme_path = Path(local_path) / "README.md"
        with open(readme_path, "w") as f:
            f.write(README_TEMPLATE.format(model_name=model_name))

        api = HfApi()
        if api.repo_exists(repo_id=repo_name):
            api.update_repo_settings(repo_id=repo_name, private=PRIVATE)
        else:
            api.create_repo(repo_id=repo_name, private=PRIVATE)
            add_collection_item(
                collection_slug=COLLECTION_SLUG,
                item_id=repo_name,
                item_type="model",
            )


        api.upload_folder(
            folder_path=local_path,
            repo_id=repo_name,
            repo_type="model",
        )
