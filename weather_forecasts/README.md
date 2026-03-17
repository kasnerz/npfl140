# Hands-on Exercise: Generating Weather Reports 🌦️

In this task, you will **generate weather reports** from weather data using open LLMs. 

You will have access to multiple open models running via API.

As an input, the system will use the JSONs pre-downloaded from [OpenWeather.org](https://openweathermap.org/api) and your custom prompt.

## How to start

Clone or download the `npfl140` repository (`git clone https://github.com/kasnerz/npfl140`) and navigate to the subfolder `weather_forecasts`. Make sure you have Python 3 installed on your system.

For starters, try running the code:
```
pip install requests
python sample.py --node 1
```

The program should output a weather report from the model running on node 1.

Example output:
> Amsterdam is experiencing a mild and cloudy day, with a temperature of 11.22°C, feeling like 10.17°C due to the moderate humidity of 68%. Scattered clouds fill the sky, with only a moderate amount of visibility impeded by the cloud cover. A gentle breeze blows from the northwest, bringing wind speeds of around 10.28 km/h and gusts of up to 13.41 km/h.

The code is mainly for your reference: you can modify the it however you wish, move it to a Jupyter notebook, etc.

> [!TIP]
> To generate forecasts for more cities, remove the `break` at the end of the generation loop.


### Choose the data
In the `data` subfolder, you can find pre-downloaded input data for 100* cities around the world. 

We recommend that you choose a small subset of the cities (5-20 inputs)  for each task as your development set so that you can iterate quickly.

> [!NOTE]
> *If you look carefully, you will notice there are actually just 98 cities. That's what happens if you ask ChatGPT to generate "a list of 100 cities" :upside_down_face:


### Access the models

You can access LLMs running on our cluster through the vLLM API at `https://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{NODE}`.

Models:
| Node | Description             |
| ---- | ----------------------- |
| 1    | Instruction-tuned model |
| 2    | Instruction-tuned model |
| 3    | Reasoning model         |
| 4    | Base model              |

All the models have maximum context length of 128,000 tokens.

> [!WARNING]
> Please, do not use the API for anything else than this assignment. The service will be stopped after the class.

## Tasks

Please enter your answers to tasks #1 - #5 in the following [shared Google doc](https://docs.google.com/document/d/1PHBdSVHyNGwr59VRov-zwPtXmXPbWR5BWXV1uAVbHVM/edit?usp=sharing).
Make sure your answers can be identified (using your names or team names as prefixes).

### 🕵 **Bonus task:** Which models are we running?

Can you reveal the "identity" of the models? Or can you at least guess their size / provider?

### ☀️ Task #1: Generate the current weather description
Generate a **description of the current weather** based on a JSON file retrieved from the [**current weather API**](https://openweathermap.org/current). You do not need to retrieve the data yourself - you can find the input files in `data/current_weather`.

**Questions**:

- **1a)** Do you see issues with model outputs? If yes, how would you mitigate them?
- **1b)** What differences between the models do you observe?
- **1c)** Try varying decoding parameters (top-k, top-p, ...). How does it affect the output?

### 🌦️ Task #2: Generate a 5-day forecast

Generate a **5-day forecast** based on a JSON file retrieved from the [**forecast API**](https://openweathermap.org/forecast5). You do not need to retrieve the data yourself - you can find the input files in `data/forecast`. 

**Careful:** *the 5-day forecast inputs may be too long and get truncated. Make sure your input fits into the maximum context length. You can use the `--forecast-pruning-factor` parameter to reduce the data resolution (originally every 3 hours).*

**Questions**:

- **2a)** How would you evaluate the quality of model outputs?
- **2b)** Can you maintain consistency of the forecast format?
- **2c)** Do the insights from 1a-c) apply here as well?

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

Note that the weather data was **up-to-date for TODO**: for evaluation the accuracy of the forecasts, feel free to check https://openweathermap.org!

## Extra links
- OpenWeather API docs: https://openweathermap.org/api/
- Prompting guide: https://www.promptingguide.ai
- [Best prompting practices from Huggingface](https://huggingface.co/docs/transformers/main/tasks/prompting#best-practices-of-llm-prompting)
