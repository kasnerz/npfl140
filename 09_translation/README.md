# NPFL140 Assignment #2: Machine Translation using LLMs

- Deadline: **Wednesday 2 May, 2024**.
---

In this assigment, you will use LLMs for **translating text** in various
languages.

As in the last assignment, you will have access to multiple open models running
on our in-house cluster via API.

As an input, you provide a sentence in a soruce sentence and the goal is to
translate it to English.

**Overview of your goals:**

1. Find a team.
2. Translate the data.
3. Write a short report describing your findings.

## How to start

### Find a team
It is strongly recommended that you do this assignment in a team **up to 5
people**. You can have the same team as in the first assignment.

You should invent a name for your team (you will need to fill it later in the
submission form).

If you do not have any teammates for some reason (for example, you have not
participated in the class), you can also submit the assignment on your own.

### Run the code

Clone or download this repository (`git clone
https://github.com/kasnerz/npfl140`) and navigate to the subfolder
`09_translation`. Make sure you have Python 3 installed on your system.

For starters, try running the code:
```
pip3 install requests
python3 sample.py --node 1
```

The program should output TODO:
> TODO

The code is just a sample: you can modify the code however you wish, move it to
a Jupyter notebook, etc.

If you have any issues with the code, please let us know: either in person
(better) or by e-mail to *kasner (at) ufal.mff.cuni.cz*. You can also start an
issue in this repository.

### Get the data
Go to [the assignment page]()

### Access the models

You can access LLMs running on our cluster through the API at
`http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{NODE}`. It is an
OpenAI-compatible API provided by
[text-generation-webui](https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API).


Currently running models:

| Node | Model                                                                                             | Released     | Max input size (tokens) | Description                                                  |
| ---- | ------------------------------------------------------------------------------------------------- | ------------ | ----------------------- | ------------------------------------------------------------ |
| 1    | [`mistralai/Mistral-7B-Instruct-v0.1`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) | Sep 27, 2023 | 8,192                   | mid-size (7B), instruction-tuned                             |
| 2    | [`mistralai/Mistral-7B-v0.1`](https://huggingface.co/mistralai/Mistral-7B-v0.1)                   | Sep 27, 2023 | 8,192                   | mid-size (7B), base                                          |
| 3    | [`microsoft/phi-2`](https://huggingface.co/microsoft/phi-2)                                       | Dec 13, 2023 | 2,048                   | small (2.7B), instruction-tuned                              |
| 4    | [`CohereForAI/aya-101`](https://huggingface.co/CohereForAI/aya-101)                               | Feb 8, 2024  | 1,024                   | large (13B), instruction-tuned, multilingual (101 languages) |


For the full list of parameters you can use in the API calls, see the
[text-generation-webui
wiki](https://github.com/oobabooga/text-generation-webui/wiki/03-%E2%80%90-Parameters-Tab#parameters-description)
and the
[GenerationOptions](https://github.com/oobabooga/text-generation-webui/blob/main/extensions/openai/typing.py#L8)
class.

Note that:
- The instruction-tuned models (1, 3, 4) should be queried with the
  `chat/completions` endpoint, which makes sure that the input is appropriately
  formatted for each model. You can easily prompt these models with
  instructions in natural language.
- The base model (2) should be queried with the `completions` endpoint.  The
  model is only pre-trained on the next token prediction, so you need to
  formulate your task with that in mind (kudos if you are able to do that!)

An example of how to use both  API endpoints is included in the sample code.

*Please, do not use the API for anything else than this assignment.*


## Tasks


### Translation


TODO

Generate a **description of the current weather** based on a JSON file retrieved from the [**current weather API**](https://openweathermap.org/current). You do not need to retrieve the data yourself - you can find the input files in `data/current_weather`.

**Questions**:

- **1a)** TODO
- **1b)**
- **1c)**
- **1d)**

## Evaluation

TODO

In this task, the evaluation is mainly qualitative. It may be helpful to log
your setup and outputs so that you have a reference for your answers.

You should also keep thinking about how would you evaluate the outputs in a
more rigorous way (we will get to evaluation later!).

Note that the weather data is **up-to-date for 28 March 2024**: for evaluation
the accuracy of the forecasts, feel free to check https://openweathermap.org!

## Submission

TODO

To complete the assignment, you need to submit a PDF report via the following
👉️ **[Google Form](https://forms.gle/gpmEHNuQirmqhKcH8)** 👈️ until **Friday 12
April, 2024**.

The report should contain:
- the name of your team and your team members,
- the answers to the questions.

The most straightforward way to write the report is to answer the questions for
each task in a **bullet-point format**. However, you can also write **free-form
text** as long as you answer to the outlined problems. Any additional
experiments, interesting remarks or ideas are welcome!


You only need to submit the form **once per team**. There are no formal
restrictions on the format of the report (i.e. Google Docs is fine).

We will provide you feedback on your responses in the following class on 9 May.
