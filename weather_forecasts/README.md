# NPFL140 Assignment #1: Generating Weather Reports 🌦️

- Deadline: **Friday 12 April, 2024**.
- [Submission form](https://forms.gle/gpmEHNuQirmqhKcH8)
---

In this assigment, you **generate weather reports** with LLMs. 


You will have access to multiple open models running on our in-house cluster via API.

As an input, the system will use the JSONs from [OpenWeather.org](https://openweathermap.org/api) and your custom prompt.

**Overview of your goals:**

1. Find a team.
2. Run the sample code.
3. Complete the tasks below.
4. Write the report describing your findings.
5. Submit the report.

**In this assignment, you should learn:**
- How to write a basic Python code querying a LLM through an OpenAI-like API.
- How to set up a suitable prompt and parameters to get the expected output.
- What are the opportunities and limits of recent open LLMs.

Note that the assignment is pretty much open-ended. We expect you to be creative and think about your findings :wink:

## How to start

### Find a team
It is strongly recommended that you do this assignment in a team **up to 5 people**. 


As an ice-breaking / team-building activity, you should invent a name for your team (you will need to fill it later in the submission form).

If you do not have any teammates for some reason (for example, you have not participated in the class), you can also submit the assignment on your own.

### Run the code

Clone or download this repository (`git clone https://github.com/kasnerz/npfl140`) and navigate to the subfolder `05_task_generation`. Make sure you have Python 3 installed on your system.

For starters, try running the code:
```
pip3 install requests
python3 sample.py --node 1
```

The program should output a sample weather report from the model running on node 1 (see below for details):
> Currently in Amsterdam, the temperature is 11.22°C with a feels like temperature of 10.17°C. The pressure is 983 hPa and the humidity is 68%. The wind is blowing at a speed of 10.28 m/s from the southwest direction with a gust speed of 13.41 m/s. The sky is mostly covered with scattered clouds with a cloud cover of 40%. The visibility is good with a distance of 10,000 meters. The sun is expected to rise at 5:40 AM and set at 9:22 PM local time.


The code is just a sample: you can modify the code however you wish, move it to a Jupyter notebook, etc.

If you have any issues with the code, please let us know: either in person (better) or by e-mail to *kasner (at) ufal.mff.cuni.cz*. You can also start an issue in this repository.

### Choose the data
In the `data` subfolder, you can find pre-downloaded input data for 100* cities around the world. 

We recommend that you choose a small subset of the cities (5-20 inputs)  for each task as your development set so that you can iterate quickly.

**If you look carefully, you will notice there are actually just 98 cities. That's what happens if you ask ChatGPT to generate "a list of 100 cities"* :upside_down_face:


### Access the models

You can access LLMs running on our cluster through the API at `http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{NODE}`. It is an OpenAI-compatible API provided by [text-generation-webui](https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API).


Currently running models:

| Node | Model                                                                                             | Released     | Max input size (tokens) | Description                                                  |
| ---- | ------------------------------------------------------------------------------------------------- | ------------ | ----------------------- | ------------------------------------------------------------ |
| 1    | [`mistralai/Mistral-7B-Instruct-v0.1`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) | Sep 27, 2023 | 8,192                   | mid-size (7B), instruction-tuned                             |
| 2    | [`mistralai/Mistral-7B-v0.1`](https://huggingface.co/mistralai/Mistral-7B-v0.1)                   | Sep 27, 2023 | 8,192                   | mid-size (7B), base                                          |
| 3    | [`microsoft/phi-2`](https://huggingface.co/microsoft/phi-2)                                       | Dec 13, 2023 | 2,048                   | small (2.7B), instruction-tuned                              |
| 4    | [`CohereForAI/aya-101`](https://huggingface.co/CohereForAI/aya-101)                               | Feb 8, 2024  | 1,024                   | large (13B), instruction-tuned, multilingual (101 languages) |


For the full list of parameters you can use in the API calls, see the [text-generation-webui wiki](https://github.com/oobabooga/text-generation-webui/wiki/03-%E2%80%90-Parameters-Tab#parameters-description) and the [GenerationOptions](https://github.com/oobabooga/text-generation-webui/blob/main/extensions/openai/typing.py#L8) class.

Note that:
- The instruction-tuned models (1, 3, 4) should be queried with the `chat/completions` endpoint, which makes sure that the input is appropriately formatted for each model. You can easily prompt these models with instructions in natural language.
- The base model (2) should be queried with the `completions` endpoint.  The model is only pre-trained on the next token prediction, so you need to formulate your task with that in mind (kudos if you are able to do that!)

An example of how to use both  API endpoints is included in the sample code.

*Please, do not use the API for anything else than this assignment.*


## Tasks


### ☀️ Task #1: Generate the current weather description
Generate a **description of the current weather** based on a JSON file retrieved from the [**current weather API**](https://openweathermap.org/current). You do not need to retrieve the data yourself - you can find the input files in `data/current_weather`.

**Questions**:

- **1a)** Do the reports look the way you would expect? 
- **1b)** How can you improve the results with a better prompt?
- **1c)** How can you improve the results by varying decoding algorithms (beam search, top-k, top-p, ...) and their parameters?
- **1d)** What differences between the models do you observe?

### 🌦️ Task #2: Generate a 5-day forecast

Generate a **5-day forecast** based on a JSON file retrieved from the [**forecast API**](https://openweathermap.org/forecast5). You do not need to retrieve the data yourself - you can find the input files in `data/forecast`. 

**Careful:** *the 5-day forecast inputs will be probably too large for the models and may get truncated. Keep an eye on the input size for each model. You can use the `--forecast_pruning_factor` parameter to reduce the data resolution (originally every 3 hours).*

**Questions**:

- **2a)** Which qualities would you expect the weather forecast to have (i.e., how should the generated text  be evaluated)? 
- **2b)** Do the generated reports have these qualities? If not, what are the issues?
- **2c)** How does filtering data items or removing certain fields from the input data improve the output quality?
- **2d)** Do the insights from 1b)-1d) apply for this task as well? 

### 🇺🇳 Task #3: Generate a weather report in another language
Use the data from task #1 or #2 and generate the reports in non-English language(s) of your choice.

**Questions**:
- **3a)** Do you observe a drop in quality compared to English? If yes, what problems do you observe?
- **3b)** How do the models compare on this task?
- **3c)** What would be your method of choice for generating weather forecasts in this language in a practical scenario?


### 🌈 Task #4: Generate stylized weather reports
Use the data from task #1 or #2 and generate the reports with a specific style of your choice (you can do more, but one is enough), for example:
- bullet-point style weather reports,
- one-sentence reports,
- ironic weather forecasts,
- weather forecasts for kids,
- ...

**Questions:**
- **4a)** How do you need to modify the prompt to generate stylized reports?
- **4b)** Are the responses robustly following the style for every output? If not, can you make it more robust?
- **4c)** Is there a difference in quality of the outputs compared to the default setup?

## Evaluation

In this task, the evaluation is mainly qualitative. It may be helpful to log your setup and outputs so that you have a reference for your answers.

You should also keep thinking about how would you evaluate the outputs in a more rigorous way (we will get to evaluation later!).

Note that the weather data is **up-to-date for 28 March 2024**: for evaluation the accuracy of the forecasts, feel free to check https://openweathermap.org!

## Submission
To complete the assignment, you need to submit a PDF report via the following 👉️ **[Google Form](https://forms.gle/gpmEHNuQirmqhKcH8)** 👈️ until **Friday 12 April, 2024**.

The report should contain:
- the name of your team and your team members,
- the answers to the questions.

The most straightforward way to write the report is to answer the questions for each task in a **bullet-point format**. However,  you can also write **free-form text** as long as you answer to the outlined problems. Any additional experiments, interesting remarks or ideas are welcome! 


You only need to submit the form **once per team**. There are no formal restrictions on the format of the report (i.e. Google Docs is fine).

We will provide you feedback on your responses in the following class on 18 April.

## Extra links
- OpenWeather API docs: https://openweathermap.org/api/
- Prompting guide: https://www.promptingguide.ai
- [Best prompting practices from Huggingface](https://huggingface.co/docs/transformers/main/tasks/prompting#best-practices-of-llm-prompting)
