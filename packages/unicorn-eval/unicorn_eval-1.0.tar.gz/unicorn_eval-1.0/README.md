# 🧪 UNICORN Evaluation Toolkit

Welcome to the official evaluation repository for the [UNICORN Challenge](https://unicorn.grand-challenge.org/) — a benchmark for foundation models in pathology, radiology and medical language processing. This repository provides the code used to evaluate submissions using frozen foundation model features. It ships with a set of feature adaptors that convert features into predictions and expects to community to contribute with custom & more fancy adaptors.

## 🚀 Goal

The challenge evaluates how well foundation models generalize across tasks without extensive fine-tuning. For language and vision-language tasks, the model should yield the prediction. For vision tasks, we adapt features using light-weight methods (adaptors). Participants are invited to use built-in adaptors or propose their own!

## 🧩 Custom Adaptors

Want to use a custom method to convert vision features to predictions?

- add your adaptor under the adaptors/ directory
- submit a pull request with a short description of your method, giving it a unique name that can be selected at submission time

Once approved and merged, you’ll be able to submit your model using your custom adaptor.

⚠️ All adaptors must follow the base adaptor interface (see `adaptors/base.py`).
