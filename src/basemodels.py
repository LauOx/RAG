from pydantic import BaseModel, Field, model_validator
import uuid
from typing_extensions import Self


class ModelError(ValueError):
    pass


class MinimalSource(BaseModel):
    file_path: str = Field(min_length=1)
    first_character_index: int = Field(ge=0)
    last_character_index: int = Field(ge=1)

    @model_validator(mode="after")
    def first_less_than_last(self) -> Self:
        if self.first_character_index >= self.last_character_index:
            raise ModelError(
                "MinimalSource's first character index "
                f"({self.first_character_index}) "
                "must be less than last character index "
                f"({self.last_character_index}).")
        return self


class UnansweredQuestion(BaseModel):
    question_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), min_length=1
        )
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: list[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: list[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: list[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: list[MinimalSearchResults]
    k: int = Field(gt=0)

    @model_validator(mode="after")
    def result_have_k_length(self) -> Self:
        for i, result in enumerate(self.search_results):
            if len(result.retrieved_sources) > self.k:
                raise ModelError(
                    f"Result in search_result[{i}] has more than k sources "
                    f"(k = {self.k})"
                    )
        return self


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: list[MinimalAnswer]
    k: int = Field(gt=0)
