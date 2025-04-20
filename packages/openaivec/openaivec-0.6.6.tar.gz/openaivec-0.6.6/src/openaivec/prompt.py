import difflib
import logging
from typing import List
from xml.etree import ElementTree

from openai import OpenAI
from openai.types.chat import ParsedChatCompletion
from pydantic import BaseModel

__all__ = [
    "FewShotPrompt",
    "FewShotPromptBuilder",
]

"""
This is a beta version of FewShotPromptBuilder.
Using CoT method instead of multiple callings of OpenAI API.
"""

_logger = logging.getLogger(__name__)


class Example(BaseModel):
    input: str
    output: str


class FewShotPrompt(BaseModel):
    purpose: str
    cautions: List[str]
    examples: List[Example]


class Step(BaseModel):
    id: int
    analysis: str
    prompt: FewShotPrompt


class Request(BaseModel):
    prompt: FewShotPrompt


class Response(BaseModel):
    iterations: List[Step]


_prompt: str = """
<Prompt>
    <Instructions>
        <Instruction id="1">
            Receive the prompt in JSON format with fields "purpose",
            "cautions", and "examples". Ensure the entire prompt is free
            from logical contradictions, redundancies, and ambiguities.
        </Instruction>
        <Instruction id="2">
            - Modify only one element per iteration among “purpose”, “examples”, or
              “cautions”, refining each at least once.
            - Address exactly one type of issue in each step.
            - Focus solely on that issue and provide a detailed explanation of the
              problem and its negative impacts.
            - Append the results sequentially to the ‘iterations’ field.
            - Write the explanation in the ‘analysis’ field and the updated prompt in
              the ‘prompt’ field.
            - Continue iterations until all issues have been addressed.
            - For the final step, review the entire prompt to ensure no issues remain
              and apply any necessary modifications.
        </Instruction>
        <Instruction id="3">
            Always respond in the same language as specified in the "purpose" field for all output values,
            including the analysis field and chain-of-thought steps.
        </Instruction>
        <Instruction id="4">
            In the "purpose" field, clearly describe the overall semantics and main goal,
            ensuring that all critical instructions contained in the original text are
            preserved without altering the base meaning.
        </Instruction>
        <Instruction id="5">
            In the "cautions" field, list common points or edge cases found
            in the examples.
        </Instruction>
        <Instruction id="6">
            In the "examples" field, enhance the examples to cover a wide range of scenarios.
            Add as many non-redundant examples as possible,
            since having more examples leads to better coverage and understanding.
        </Instruction>
        <Instruction id="7">
            Verify that the improved prompt adheres to the Request and
            Response JSON schemas.
        </Instruction>
        <Instruction id="8">
            Generate the final refined FewShotPrompt as an iteration in
            the Response, ensuring the final output is consistent,
            unambiguous, and free from any redundancies or contradictions.
        </Instruction>
    </Instructions>
    <Example>
        <Input>{
    "origin": {
        "purpose": "some_purpose01",
        "cautions": [
            "some_caution01",
            "some_caution02",
            "some_caution03"
        ],
        "examples": [
            {
                "input": "some_input01",
                "output": "some_output01"
            },
            {
                "input": "some_input02",
                "output": "some_output02"
            },
            {
                "input": "some_input03",
                "output": "some_output03"
            },
            {
                "input": "some_input04",
                "output": "some_output04"
            },
            {
                "input": "some_input05",
                "output": "some_output05"
            }
        ]
    }
}</Input>
<Output>
{
  "iterations": [
    {
      "id": 1,
      "analysis": "The original purpose was vague and did not explicitly state the main objective. This ambiguity could lead to confusion about the task. In this iteration, we refined the purpose to clearly specify that the goal is to determine the correct category for a given word based on its context.",
      "prompt": {
        "purpose": "Determine the correct category for a given word by analyzing its context for clear meaning.",
        "cautions": [
          "Ensure the word's context is provided to avoid ambiguity.",
          "Consider multiple meanings of the word and choose the most relevant category."
        ],
        "examples": [
          {
            "input": "Apple (as a fruit)",
            "output": "Fruit"
          },
          {
            "input": "Apple (as a tech company)",
            "output": "Technology"
          },
          ...
        ]
      }
    },
    {
      "id": 2,
      "analysis": "Next, we focused solely on the cautions section. The original cautions were generic and did not mention potential pitfalls like homonyms or polysemy. Failing to address these could result in misclassification. Therefore, we added a specific caution regarding homonyms while keeping the purpose and examples unchanged.",
      "prompt": {
        "purpose": "Determine the correct category for a given word by analyzing its context for clear meaning.",
        "cautions": [
          "Ensure the word's context is provided to avoid ambiguity.",
          "Consider multiple meanings of the word and choose the most relevant category.",
          "Pay close attention to homonyms and polysemy to prevent misclassification."
        ],
        "examples": [
          {
            "input": "Apple (as a fruit)",
            "output": "Fruit"
          },
          {
            "input": "Apple (as a tech company)",
            "output": "Technology"
          },
          ...
        ]
      }
    },
    {
      "id": 3,
      "analysis": "In this step, we improved the examples section to cover a broader range of scenarios and address potential ambiguities. By adding examples that include words with multiple interpretations (such as 'Mercury' for both a planet and an element), we enhance clarity and ensure better coverage. This iteration only modifies the examples section, leaving purpose and cautions intact.",
      "prompt": {
        "purpose": "Determine the correct category for a given word by analyzing its context for clear meaning.",
        "cautions": [
          "Ensure the word's context is provided to avoid ambiguity.",
          "Consider multiple meanings of the word and choose the most relevant category.",
          "Pay close attention to homonyms and polysemy to prevent misclassification."
        ],
        "examples": [
          {
            "input": "Apple (as a fruit)",
            "output": "Fruit"
          },
          {
            "input": "Apple (as a tech company)",
            "output": "Technology"
          },
          {
            "input": "Mercury (as a planet)",
            "output": "Astronomy"
          },
          {
            "input": "Mercury (as an element)",
            "output": "Chemistry"
          },
          ...
        ]
      }
    },
    {
        "id": 4,
        "analysis": "In this final iteration, we ensured that the entire prompt...",
        ...
    }
    ...
  ]
}
</Output>
    </Example>
</Prompt>
"""


def render_prompt(prompt: FewShotPrompt) -> str:
    """Render a FewShotPrompt instance to its XML representation.

    Args:
        prompt (FewShotPrompt): The prompt object to render.

    Returns:
        str: The XML string representation of the prompt.
    """
    prompt_dict = prompt.model_dump()
    root = ElementTree.Element("Prompt")

    # Purpose (always output)
    purpose_elem = ElementTree.SubElement(root, "Purpose")
    purpose_elem.text = prompt_dict["purpose"]

    # Cautions (always output, even if empty)
    cautions_elem = ElementTree.SubElement(root, "Cautions")
    if prompt_dict.get("cautions"):
        for caution in prompt_dict["cautions"]:
            caution_elem = ElementTree.SubElement(cautions_elem, "Caution")
            caution_elem.text = caution

    # Examples (always output)
    examples_elem = ElementTree.SubElement(root, "Examples")
    for example in prompt_dict["examples"]:
        example_elem = ElementTree.SubElement(examples_elem, "Example")
        input_elem = ElementTree.SubElement(example_elem, "Input")
        input_elem.text = example.get("input")
        output_elem = ElementTree.SubElement(example_elem, "Output")
        output_elem.text = example.get("output")

    ElementTree.indent(root, level=0)
    return ElementTree.tostring(root, encoding="unicode")


class FewShotPromptBuilder:
    _prompt: FewShotPrompt
    _steps: List[Step]

    def __init__(self):
        """Initialize an empty FewShotPromptBuilder."""
        self._prompt = FewShotPrompt(purpose="", cautions=[], examples=[])

    @classmethod
    def of(cls, prompt: FewShotPrompt) -> "FewShotPromptBuilder":
        """Create a builder pre‑populated with an existing prompt.

        Args:
            prompt (FewShotPrompt): The prompt to start from.

        Returns:
            FewShotPromptBuilder: A new builder instance.
        """
        builder = cls()
        builder._prompt = prompt
        return builder

    def purpose(self, purpose: str) -> "FewShotPromptBuilder":
        """Set the purpose of the prompt.

        Args:
            purpose (str): A concise statement describing the prompt’s goal.

        Returns:
            FewShotPromptBuilder: The current builder instance (for chaining).
        """
        self._prompt.purpose = purpose
        return self

    def caution(self, caution: str) -> "FewShotPromptBuilder":
        """Append a cautionary note to the prompt.

        Args:
            caution (str): A caution or edge‑case description.

        Returns:
            FewShotPromptBuilder: The current builder instance.
        """
        if self._prompt.cautions is None:
            self._prompt.cautions = []
        self._prompt.cautions.append(caution)
        return self

    def example(
        self,
        input_value: str | BaseModel,
        output_value: str | BaseModel,
    ) -> "FewShotPromptBuilder":
        """Add a single input/output example.

        Args:
            input_value (str | BaseModel): Example input; if a Pydantic model is
                provided it is serialised to JSON.
            output_value (str | BaseModel): Expected output; serialised if needed.

        Returns:
            FewShotPromptBuilder: The current builder instance.
        """
        if self._prompt.examples is None:
            self._prompt.examples = []

        input_string = input_value if isinstance(input_value, str) else input_value.model_dump_json()
        output_string = output_value if isinstance(output_value, str) else output_value.model_dump_json()
        self._prompt.examples.append(Example(input=input_string, output=output_string))
        return self

    def improve(
        self,
        client: OpenAI,
        model_name: str,
        temperature: float = 0.0,
        top_p: float = 1.0,
    ) -> "FewShotPromptBuilder":
        """Iteratively refine the prompt using an LLM.

        The method calls a single LLM request that returns multiple
        editing steps and stores each step for inspection.

        Args:
            client (openai.OpenAI): Configured OpenAI client.
            model_name (str): Model identifier (e.g. ``gpt-4o-mini``).
            temperature (float, optional): Sampling temperature. Defaults to 0.0.
            top_p (float, optional): Nucleus sampling parameter. Defaults to 1.0.

        Raises:
            ValueError: If fewer than five examples are present.

        Returns:
            FewShotPromptBuilder: The current builder instance containing the
            refined prompt and iteration history.
        """
        # At least 5 examples are required to enhance the prompt.
        if len(self._prompt.examples) < 5:
            raise ValueError("At least 5 examples are required to enhance the prompt.")

        completion: ParsedChatCompletion[Response] = client.beta.chat.completions.parse(
            model=model_name,
            messages=[
                {"role": "system", "content": _prompt},
                {
                    "role": "user",
                    "content": Request(prompt=self._prompt).model_dump_json(),
                },
            ],
            temperature=temperature,
            top_p=top_p,
            response_format=Response,
        )

        # keep the original prompt
        self._steps = [Step(id=0, analysis="Original Prompt", prompt=self._prompt)]

        # add the histories
        for step in completion.choices[0].message.parsed.iterations:
            self._steps.append(step)

        # set the final prompt
        self._prompt = self._steps[-1].prompt

        return self

    def explain(self) -> "FewShotPromptBuilder":
        """Pretty‑print the diff of each improvement iteration.

        Returns:
            FewShotPromptBuilder: The current builder instance.
        """
        for previous, current in zip(self._steps, self._steps[1:]):
            print(f"=== Iteration {current.id} ===\n")
            print(f"Instruction: {current.analysis}")
            diff = difflib.unified_diff(
                render_prompt(previous.prompt).splitlines(),
                render_prompt(current.prompt).splitlines(),
                fromfile="before",
                tofile="after",
                lineterm="",
            )
            for line in diff:
                print(line)
        return self

    def _validate(self) -> None:
        """Validate the internal FewShotPrompt.

        Raises:
            ValueError: If required fields such as purpose or examples are
                missing.
        """
        # Validate that 'purpose' and 'examples' are not empty.
        if not self._prompt.purpose:
            raise ValueError("Purpose is required.")
        if not self._prompt.examples or len(self._prompt.examples) == 0:
            raise ValueError("At least one example is required.")

    def get_object(self) -> FewShotPrompt:
        """Return the underlying FewShotPrompt object.

        Returns:
            FewShotPrompt: The validated prompt object.
        """
        self._validate()
        return self._prompt

    def build(self) -> str:
        """Build and return the prompt as XML.

        Returns:
            str: XML representation of the prompt.
        """
        self._validate()
        return self.build_xml()

    def build_json(self, **kwargs) -> str:
        """Build and return the prompt as a JSON string.

        Args:
            **kwargs: Keyword arguments forwarded to ``model_dump_json``.

        Returns:
            str: JSON representation of the prompt.
        """
        self._validate()
        return self._prompt.model_dump_json(**kwargs)

    def build_xml(self) -> str:
        """Alias for :py:meth:`build` for explicit XML generation.

        Returns:
            str: XML representation of the prompt.
        """
        self._validate()
        return render_prompt(self._prompt)
