# NPFL140 Assignment #2: Machine Translation using LLMs

- Deadline: **Thursday 2 May, 2024**.
- [Evaluation interface](https://quest.ms.mff.cuni.cz/npfl140/)
- Submission email: `helcl@ufal.mff.cuni.cz`
---

In this assigment, you will use LLMs for **translating text** in various
languages.

As in the last assignment, you will have access to multiple open models running
on our in-house cluster via API.

As an input, you provide a sentence in a source sentence and the goal is to
translate it to English.

**Overview of your goals:**

1. Find a team.
2. Translate the data into English and one another language.
3. Write a short report describing your findings.

## How to start

### Find a team
It is strongly recommended that you do this assignment in a team **up to 5
people**. You can have the same team as in the first assignment.


If you do not have any teammates for some reason (for example, you have not
participated in the class), you can also submit the assignment on your own.

### Run the code

Clone or download this repository (`git clone
https://github.com/kasnerz/npfl140`) and navigate to the subfolder
`09_translation`. Make sure you have Python 3 installed on your system.

For starters, try running the code:
```
pip3 install -r requirements.txt
python3 sample.py --node 1 --src_text "Rechtsstaatlichkeit und Menschenrechte sind weltweit"
```

The program should output:
```
"The rule of law and human rights are worldwide."
```

The code is just a sample: you can modify the code however you wish, move it to
a Jupyter notebook, etc.

If you have any issues with the code, please let us know: either in person
(better) or by e-mail to `helcl@ufal.mff.cuni.cz`. You can also start an
issue in this repository.

### Get the data
In `sources.txt`, there are 21 paragraphs (each on one line) in different languages.
For a better look at the data, you may want to go to the [evaluation interface](https://quest.ms.mff.cuni.cz/npfl140/).

### Access the models

You can access LLMs running on our cluster through the API at
`http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{NODE}`. It is an
OpenAI-compatible API provided by
[text-generation-webui](https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API).


Currently running models:

| Node | Model                                                                                             |
| ---- | ------------------------------------------------------------------------------------------------- |
| 1    | [`mistralai/Mistral-7B-Instruct-v0.1`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) |
| 2    | [`Unbabel/TowerInstruct-7B-v0.1`](https://huggingface.co/Unbabel/TowerInstruct-7B-v0.1)           |
| 3    | [`CohereForAI/aya-101`](https://huggingface.co/CohereForAI/aya-101)                               |
| 4    | [`haoranxu/ALMA-7B-R`](https://huggingface.co/haoranxu/ALMA-7B-R)                                 |


For the full list of parameters you can use in the API calls, see the
[text-generation-webui
wiki](https://github.com/oobabooga/text-generation-webui/wiki/03-%E2%80%90-Parameters-Tab#parameters-description)
and the
[GenerationOptions](https://github.com/oobabooga/text-generation-webui/blob/main/extensions/openai/typing.py#L8)
class.

Note that:
- The instruction-tuned models (1, 2, 3) should be queried with the
  `chat/completions` endpoint.
- The base model (4) should be queried with the `completions` endpoint.

An example of how to use both  API endpoints is included in the sample code.

*Please, do not use the API for anything else than this assignment.*


## Tasks


### Translation to English

Your first task will be to translate all of the texts in `sources.txt` into English and submit the translations via the [web interface](https://quest.ms.mff.cuni.cz/npfl140/).
The translations will be evaluated against a reference using Character F-score and the results will be shown on a leaderboard.
You can make multiple submissions, but please be consistent in your team name so we can keep track of your efforts.

Also please do not use translation tools like Google translate. They work. It is not the point of this assignment to get the best translations possible.

### Translation into your language

Next, try to translate the texts into a language of your choice. Experiment with including the source, the English translation, or both, in the prompt.
Summarize your findings in a short report.

## Evaluation

For evaluation of translation into English, use the [web interface](https://quest.ms.mff.cuni.cz/npfl140/) for automatic evaluation. Try to look at each of the outputs and inspect them subjectively.
Can you spot patterns in the translation quality depending on the source language?

For evaluation of translation into your language, there is no evaluation interface, so please inspect all outputs manually and comment on the quality.

## Submission

Please send us your reports via email `helcl@ufal.mff.cuni.cz`, until **May 2, 2024**.

The report should contain:
- the name of your team and your team members,
- the summary of your findings with translation into your language (plus pointer to the team name in the leaderboard if it is not the same)

The most straightforward way to write the report is to answer the questions for
each task in a **bullet-point format**. However, you can also write **free-form
text** as long as you answer to the outlined problems. Any additional
experiments, interesting remarks or ideas are welcome!

You only need to submit the form **once per team**. There are no formal
restrictions on the format of the report (i.e. Google Docs is fine).

We will provide you feedback on your responses in the following class on 9 May.
