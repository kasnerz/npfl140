# NPFL140 Hands-on Exercise: Generating Weather Reports 🌦️

Today, you will **generate weather reports** with LLMs. 


You will have access to multiple open models running on our in-house cluster via API.

As an input, the system will use the JSONs from [OpenWeather.org](https://openweathermap.org/api) and your custom prompt.

**Overview of your goals:**

1. Find a team.
2. Run the sample code.
3. Complete the tasks below.
4. Describe your findings to your peers.

**In this exercise, you should learn:**
- How to write a basic Python code querying a LLM through an API.
- How to set up a suitable prompt and parameters to get the expected output.
- What are the opportunities and limits of recent open LLMs.

Note that the exercise is pretty much open-ended. We expect you to be creative and think about your findings :wink:

## How to start

### Find a team
It is strongly recommended that you do this assignment in a team **up to 5 people**. 
You can work in your official assignment teams, or you can form new teams.

If you do not have any teammates for some reason (for example, you have not participated in the class), you can also work on your own.

### Run the code

Clone or download this repository (`git clone https://github.com/kasnerz/npfl140`) and navigate to the subfolder `weather_forecasts`. Make sure you have Python 3 installed on your system.

For starters, try running the code:
```
pip3 install requests
python3 sample.py --node 1
```

The program should output a sample weather report from the model running on node 1 (see below for details):
> Amsterdam is experiencing a mild and cloudy day, with a temperature of 11.22°C, feeling like 10.17°C due to the moderate humidity of 68%. Scattered clouds fill the sky, with only a moderate amount of visibility impeded by the cloud cover. A gentle breeze blows from the northwest, bringing wind speeds of around 10.28 km/h and gusts of up to 13.41 km/h.

The code is just an example: you can modify the code however you wish, move it to a Jupyter notebook, etc.

If you have any issues with the code, please let us know: either in person (better) or by e-mail to *kasner (at) ufal.mff.cuni.cz*. You can also start an issue in this repository.

### Choose the data
In the `data` subfolder, you can find pre-downloaded input data for 100* cities around the world. 

We recommend that you choose a small subset of the cities (5-20 inputs)  for each task as your development set so that you can iterate quickly.

**If you look carefully, you will notice there are actually just 98 cities. That's what happens if you ask ChatGPT to generate "a list of 100 cities"* :upside_down_face:


### Access the models

You can access LLMs running on our cluster through the Ollama API at `http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{NODE}/api`.

Currently running models: 
| Node | Model                                  | Released     | Max input size (tokens) | Description                                                  |
| ---- | -------------------------------------- | ------------ | ----------------------- | ------------------------------------------------------------ |
| 1    | [LLama 3.1 8B](https://ollama.com/library/llama3.1:8b)           | Jun 23, 2024 | 128k                    | mid-size (8B), instruction-tuned   |
| 2    | [Phi 3.5 3.8B](https://ollama.com/library/phi3.5:3.8b)           | Aug 16, 2024 | 128k                    | small (3.8B), instruction-tuned    |
| 3    | [Deepseek R1 14B](https://ollama.com/library/deepseek-r1:14b)    | Jan 21, 2025 | 32k                     | mid-size (14B), reasoning          |
| 4    | [Mistral 7B](https://ollama.com/library/mistral:7b-text)         | Sep 27, 2023 | 8,192                   | mid-size (7B), base                |

*Please, do not use the API for anything else than this assignment. The service will be stopped after the class.*

## Tasks

Please enter your answers to tasks #1 - #4 in the following [shared Google doc](https://docs.google.com/document/d/1H4sPFBkC7umGo-zmV2rgsN9O-wMFT4kW1xuT9WDhN3Y/edit?usp=sharing).
Make sure your answers can be identified (for example, you can use your team name).

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

- **2a)** Which qualities would you expect the weather forecast to have (i.e., how should the generated text be evaluated)? 
- **2b)** Do the generated reports have these qualities? If not, what are the issues?
- **2c)** How does filtering data items or removing certain fields from the input data improve the output quality?
- **2d)** Do the insights from 1b)-1d) apply for this task as well? 

### 🇺🇳 BONUS Task #3: Generate a weather report in another language
Use the data from task #1 or #2 and generate the reports in non-English language(s) of your choice.

**Questions**:
- **3a)** Do you observe a drop in quality compared to English? If yes, what problems do you observe?
- **3b)** How do the models compare on this task?
- **3c)** What would be your method of choice for generating weather forecasts in this language in a practical scenario?


### 🌈 BONUS Task #4: Generate stylized weather reports
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

Note that the weather data was **up-to-date for 28 March 2024**: for evaluation the accuracy of the forecasts, feel free to check https://openweathermap.org!

## Extra links
- OpenWeather API docs: https://openweathermap.org/api/
- Prompting guide: https://www.promptingguide.ai
- [Best prompting practices from Huggingface](https://huggingface.co/docs/transformers/main/tasks/prompting#best-practices-of-llm-prompting)
