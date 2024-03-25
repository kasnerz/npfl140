# NPFL140 Assignment #1: Generating Weather Reports 🌦️
In this assigment, you will try **generating weather reports** with open LLMs. 

As an input, the system will use the JSONs from [OpenWeather.org](https://openweathermap.org/api) and your custom prompt.

You will use the models running on our in-house cluster. You will have access to these models through an API.

**Overview of your goals:**

1. Find a team.
2. Run the sample code.
3. Complete the tasks below.
4. Write the report describing your findings.
5. Submit the report.

**You should learn:**
- How to write a basic Python code querying a LLM through an OpenAI-like API.
- How to set up a suitable prompt and parameters to get the expected output.
- What are the opportunities and limits of recent open LLMs.

Note that the assignment is pretty open-ended. We expect you to be creative and think and discuss about your findings ;) 

## How to start

### Find a team
It is strongly recommended that you find teammates for the assignment. Your team can have **up to 5 people**. 

If you do not have any teammates for some reason (for example, you have not participated in the class), you can also submit the assignment on your own.

As an ice-breaking / team-building activity, you should invent a name for your team (you will need to fill it later in the submission form).

### Run the code

Clone or download this repository (https://github.com/kasnerz/npfl140) and navigate to the subfolder `05_task_generation`. Make sure you have Python 3 installed on your system.

For starters, try running the code:
```
python3 sample.py --node 1
```

The program should output a sample weather report from the model running on node 1 (see below for details):
> Currently in Amsterdam, the temperature is 27.98°C with a feels like temperature of 29.2°C. The pressure is 1015 hPa and the humidity is 58%. The wind is blowing at a speed of 1.34 m/s from the east with a gust of 2.24 m/s. The sky is clear with no clouds in sight. The visibility is excellent at 10,000 meters. The sun is currently rising at 6:58 AM and will set at 8:31 PM local time.


The code is just a sample: you can modify the code however you wish.

If you have any issues with the code, please let us know: either in person (better) or by e-mail to *kasner (at) ufal.mff.cuni.cz*.

### Accessing the data
You can find the data in the `data` subfolder. The data for each task is divided into a `dev` / `test` set. 

The idea is that you will tune your prompts and parameters on a subset of data (`dev`) and draw the conclusions based on another, "unseen" subset (`test`).

The `dev` set is rather small (10 inputs) so that you can do the experiments quickly.

### Evaluation

In this task, the evaluation is mainly qualitative, we do not require that any quantitative evaluation yet.

However, it could also be helpful to log your setup and outputs so that you can manually compare them.

You should also keep thinking about how would you evaluate the outputs in a more rigorous way.

## Models

You can access LLMs running on our cluster through the API at `http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{NODE}`. It is an OpenAI-compatible API provided by [text-generation-webui](https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API).


Currently running models:

| Node number | Model                                                                                             | Released     | Description                                                  |
| ----------- | ------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------ |
| 1           | [`mistralai/Mistral-7B-Instruct-v0.1`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) | Sep 27, 2023 | mid-size (7B), instruction-tuned                             |
| 2           | [`mistralai/Mistral-7B-v0.1`](https://huggingface.co/mistralai/Mistral-7B-v0.1)                   | Sep 27, 2023 | mid-size (7B), base                                          |
| 4           | [`microsoft/phi-2`](https://huggingface.co/microsoft/phi-2)                                       | Dec 13, 2023 | small (2.7B), instruction-tuned                              |
| 3           | [`CohereForAI/aya-101`](https://huggingface.co/CohereForAI/aya-101)                               | Feb 8, 2024  | large (13B), instruction-tuned, multilingual (101 languages) |


For the full list of parameters you can use in the API calls, see https://github.com/oobabooga/text-generation-webui/blob/main/extensions/openai/typing.py.

Note that:
- The instruction-tuned models (1, 3, 4) should be queried with the `chat/completions` endpoint, which makes sure that the input is appropriately formatted for each model. You can easily prompt these models with instructions in natural language.
- The base model (2) should be queried with the `completions` endpoint.  The model is only pre-trained on the next token prediction, so you need to formulate your task with that in mind (kudos if you are able to do that!)


*(Please, do not use the API for anything else than this assignment).*


## Tasks


### ☀️ Task #1: Generate the current weather description
Generate a **description of the current weather** based on a JSON file retrieved from the [**current weather API**](https://openweathermap.org/current). You can find the files in `data/current_weather`.

**Questions**:

- Do the reports look the way you would expect? 
- How can you improve the results with a better prompt?
- What happens if you change the decoding algorithms (beam search, top-k, top-p, ...) and their parameters?
- What differences between the models do you observe?

### 🌦️ Task #2: Generate a 5-day forecast

Generate a **5-day forecast** based on a JSON file retrieved from the [**forecast API**](https://openweathermap.org/forecast5). You can find the files in `data/forecast`. 

Note that by default, the data may be too long for the model.

**Questions**:

- Which qualities would you expect the weather forecast to have (i.e., how should the generated text  be evaluated)? 
- Do the generated reports have these qualities? If not, what are the issues?
- Can you improve the quality of the forecasts by removing certain fields from the input data?

### 🇺🇳 Task #3: Generate a weather report in another language
Use the data from task #1 or #2 and generate the reports in non-English language(s) of your choice.

**Questions**:
- Do you observe a drop in quality compared to English? If yes, what problems do you observe?
- Is the multilingual model (`aya-101`) better than the other models?
- If you actually had to generate similar texts in the language you selected, how would you proceed?


### 🌈 Task #4: Generate stylized weather reports
Use the data from task #1 or #2 and generate the reports with a specific style of your choice (you can do more, but one is enough), for example:
- bullet-point style weather reports,
- one-sentence reports,
- ironic weather forecasts,
- weather forecasts for kids,
- ...

**Questions:**
- How do you need to modify the prompt to efficiently control the model?
- Are the responses robustly following the style, or is there variance between outputs?
- Is there a difference in quality of the outputs compared to the default setup?



## Submission
To complete the assignment, you need to submit a PDF report via the following 👉️ **[Google Form](https://forms.gle/gpmEHNuQirmqhKcH8)** 👈️ until **11 April, 2024**.

The report should contain:
- the name of your team and your team members,
- the description of your outcomes (see the tasks below).

The most straightforward way to write the report is to answer the questions for each task in a **bullet-point format**. However,  you can also write **free-form text** as long as you answer to the outlined problems.

Any additional experiments, interesting remarks or ideas are welcome! 


You only need to submit the form **once per team**.

There are no formal restrictions on the format of the report, i.e. Google Docs is fine, as long as it is a PDF file.

## Extra tips
- OpenWeather API docs: https://openweathermap.org/api/
- Prompting guide: https://www.promptingguide.ai
- Best prompting practices from [Huggingface](https://huggingface.co/docs/transformers/main/tasks/prompting#best-practices-of-llm-prompting):
  - When choosing the model to work with, the latest and most capable models are likely to perform better.
  - Start with a simple and short prompt, and iterate from there. 
  - Put the instructions at the beginning of the prompt, or at the very end. When working with large context, models apply various optimizations to prevent Attention complexity from scaling quadratically. This may make a model more attentive to the beginning or end of a prompt than the middle.
  - Clearly separate instructions from the text they apply to - more on this in the next section.
  Be specific and descriptive about the task and the desired outcome - its format, length, style, language, etc.
  - Avoid ambiguous descriptions and instructions.
  - Favor instructions that say “what to do” instead of those that say “what not to do”.
  - “Lead” the output in the right direction by writing the first word (or even begin the first sentence for the model).
  - Use advanced techniques like Few-shot prompting and Chain-of-thought
  - Test your prompts with different models to assess their robustness.
  - Version and track the performance of your prompts.


