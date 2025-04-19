# MIT License
#
# Copyright (c) 2024 Chronulus AI Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
from copy import deepcopy
from io import StringIO
from typing import Any, List, Union, Optional

from pydantic import BaseModel

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    import warnings


class Prediction:
    """
    A class representing the output of a prediction request

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.

    Attributes
    ----------
    _id : str
        Unique identifier for the prediction.

    """

    def __init__(self, _id: str):
        self._id = _id

    @property
    def id(self) -> str:
        """Get the unique identifier for the prediction"""
        return self._id


class Forecast(Prediction):
    """
    A class representing the output of a prediction request, containing both numerical results and explanatory text.

    This class encapsulates the prediction results returned from the chronulus API,
    including a unique identifier, descriptive text, and the numerical predictions in
    a pandas DataFrame format.

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.
    text : str
        Descriptive text or notes explaining the prediction results.
    data : dict
        JSON-Split formatted dictionary containing the prediction results.

    Attributes
    ----------
    _id : str
        Unique identifier for the prediction.
    _text : str
        Explanatory text describing the prediction results.
    _data : dict
        JSON-Split formatted dictionary containing the prediction results.

    """

    def __init__(self, _id: str, text: str, data: dict):
        super().__init__(_id)
        self._text = text
        self._data = data

    @property
    def data(self) -> dict:
        """Get the forecast data after the transformation defined by this forecast"""
        return self._transform_data(self._data)

    @property
    def text(self) -> str:
        """Get the forecast explanation after the transformation defined by this forecast"""
        return self._transform_text(self._text)

    def _transform_data(self, data: dict) -> dict:
        """Hook for transforming the forecast data"""
        return data

    def _transform_text(self, text: str) -> str:
        """Hook for transforming the forecast text"""
        return text

    def to_json(self, orient='columns'):
        """
        Convert the forecast data to JSON format with specified orientation.

        Parameters
        ----------
        orient : str, optional
            Data orientation for the JSON output. Options are:

            - 'split': Original JSON-split format
            - 'rows': List of dictionaries, each representing a row
            - 'columns': Dictionary of lists, each representing a column
            Default is 'columns'.

        Returns
        -------
        dict or list
            Forecast data in the specified JSON format:

            - For 'split': Original JSON-split dictionary
            - For 'rows': List of row dictionaries
            - For 'columns': Dictionary of column arrays

        Examples
        --------
        >>> # Get data in columns format
        >>> json_cols = forecast.to_json(orient='columns')
        >>> # Get data in rows format
        >>> json_rows = forecast.to_json(orient='rows')
        """

        if orient == 'split':
            return self.data

        elif orient == 'rows':
            columns = self.data.get('columns')
            rows = list()
            for row in self.data.get('data'):
                _row = {columns[j]: val for j, val in enumerate(row)}
                rows.append(_row)
            return rows

        else:
            col_names = self.data.get('columns')
            columns = {k: list() for k in col_names}

            for row in self.data.get('data'):
                for j, val in enumerate(row):
                    columns[col_names[j]].append(val)

            return columns

    def to_pandas(self):
        """
        Convert the forecast data to a pandas DataFrame.

        The first column is automatically set as the index of the resulting DataFrame.
        Typically, this is a timestamp or date column.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the forecast data with the first column as index.

        Raises
        ------
        ImportError
            If pandas is not installed in the environment.

        Examples
        --------
        >>> df = forecast.to_pandas()
        >>> print(df.head())
                   y_hat
        date
        2025-01-01   .12345
        2025-01-02   .67890
        """
        if not PANDAS_AVAILABLE:

            message = """pandas is not installed but his method requires pandas. Please install pandas using `pip install pandas` and then try again."""
            raise ImportError(message)

        else:
            json_str = json.dumps(self.data)
            df = pd.read_json(StringIO(json_str), orient='split')
            return df.set_index(self.data.get('columns')[0], drop=True)


class NormalizedForecast(Forecast):
    """
    A class representing the output of a NormalizedForecast prediction request, containing both numerical results and explanatory text.

    This class provides methods for operating on normalized forecast data.

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.
    text : str
        Descriptive text or notes explaining the prediction results.
    data : dict
        JSON-Split formatted dictionary containing the prediction results.
    y_min : float
        The minimum value of the source scale.
    y_max : float
        The maximum value of the source scale
    """

    def __init__(self, _id: str, text: str, data: dict, y_min: float = 0.0, y_max: float = 1.0):
        super().__init__(_id, text, data)
        self.y_min = y_min
        self.y_max = y_max

    def to_rescaled_forecast(self, y_min: float = 0.0, y_max: float = 1.0, invert_scale: bool = False):
        """
        Create a RescaledForecast instance from  NormalizedForecast object.

        This static method allows conversion from a generic Forecast to a RescaledForecast,
        applying the specified scaling parameters.

        Parameters
        ----------
        y_min : float, default 0.0
            The minimum value of the target scale.
        y_max : float, default 1.0
            The maximum value of the target scale.
        invert_scale : bool, default False
            Whether to invert the scale before rescaling.

        Returns
        -------
        RescaledForecast
            A new RescaledForecast instance containing the rescaled data.
        """
        return RescaledForecast(
            _id=self.id,
            data=self.data,
            text=self.text,
            y_min=y_min,
            y_max=y_max,
            invert_scale=invert_scale
        )


class RescaledForecast(Forecast):
    """
    A class representing a RescaledForecast prediction

    This class provides methods for rescaling (denormalizing) a Forecast.

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.
    text : str
        Descriptive text or notes explaining the prediction results.
    data : dict
        JSON-Split formatted dictionary containing the prediction results.
    y_min : float
        The minimum value of the source scale.
    y_max : float
        The maximum value of the source scale
    invert_scale : bool
        Should we invert the scale before rescaling?
    """

    def __init__(self, _id: str, text: str, data: dict, y_min: float = 0.0, y_max: float = 1.0,
                 invert_scale: bool = False):
        super().__init__(_id, text, data)
        self.y_min = y_min
        self.y_max = y_max
        self.invert_scale = invert_scale

    def _transform_data(self, data: dict) -> dict:
        # data should be in split format
        # we should create types for this instead of assuming
        new_data = deepcopy(data)
        json_data = new_data.get("data")
        for i, (ds, y_hat) in enumerate(json_data):
            yhat = 1 - y_hat if self.invert_scale else y_hat
            yhat = yhat * (self.y_max - self.y_min) + self.y_min
            json_data[i][1] = yhat

        new_data['data'] = json_data

        return new_data

    @staticmethod
    def from_forecast(forecast: Forecast, y_min: float = 0.0, y_max: float = 1.0, invert_scale: bool = False):
        """
        Convert the normalized forecast to a rescaled forecast with specified scale parameters.

        This method creates a new RescaledForecast instance using the current forecast's data,
        allowing you to specify the target range and whether to invert the scale.

        Parameters
        ----------
        y_min : float, default 0.0
            The minimum value of the target scale.
        y_max : float, default 1.0
            The maximum value of the target scale.
        invert_scale : bool, default False
            Whether to invert the scale before rescaling.

        Returns
        -------
        RescaledForecast
            A new forecast instance with values rescaled to the specified range.
        """

        return RescaledForecast(
            _id=forecast.id,
            data=forecast.data,
            text=forecast.text,
            y_min=y_min,
            y_max=y_max,
            invert_scale=invert_scale
        )


class BetaParams(BaseModel):
    """Collection of alpha and beta parameters for a Beta distribution.

    The intuition for alpha and beta is simple. Consider the batting average of a baseball player. Alpha represents
    the number of hits the player records over a period of time. Beta represents the number of at-bats without a hit.
    Together, the batting average of the player over that period of time is alpha / (alpha + beta), which is exactly
    the mean of the Beta distribution. Also, as the player accumulates more at-bats, we become more and more confident
    of their true batting average.

    Parameters
    ----------
    alpha : float
        The shape parameter of successes
    beta : float
        The shape parameter of failures


    Attributes
    ----------
    alpha : float
        The shape parameter of successes
    beta : float
        The shape parameter of failures
    """

    alpha: float
    beta: float


class ExpertOpinion(BaseModel):
    """The opinion of an expert agent consulted by BinaryPredictor

    Parameters
    ----------
    prob_a: float
        The probability estimated or implied by complementation
    question: str
        The reframed question that the agent considered during estimation
    notes: str
        The text explanation justifying the expert's estimate
    beta_params : BetaParams
        The alpha and beta parameters for the Beta distribution over the opinion


    Attributes
    ----------
    prob_a: float
        The probability estimated or implied by complementation
    question: str
        The reframed question that the agent considered during estimation
    notes: str
        The text explanation justifying the expert's estimate
    beta_params : BetaParams
        The alpha and beta parameters for the Beta distribution over the opinion

    """
    prob_a: float
    question: str
    notes: str
    negative: bool = False
    beta_params: Optional[BetaParams] = None
    _prob_a: Optional[float] = None

    def model_post_init(self, __context: Any) -> None:
        self._prob_a = self.prob_a
        if self.beta_params is not None:
            self.prob_a = self.beta_params.alpha / (self.beta_params.alpha + self.beta_params.beta)

    @property
    def prob(self):
        """Gets the estimated probability and its complement."""
        return self.prob_a, 1 - self.prob_a

    @property
    def text(self):
        """Gets the text representation of the expert opinion"""
        sections = [
            "[Negative]" if self.negative else "[Positive]",
            "Q: " + self.question,
            f"Pred: ({self.prob_a * 100:2.2f}%{'' if self.negative else '*'}, {(1 - self.prob_a) * 100:2.2f}%{'*' if self.negative else ''})",
            "A: " + self.notes,
        ]
        return "\n\n".join(sections)


class BinaryPair(BaseModel):
    """A pair of ExpertOpinions produced independently by the same expert agent

    Each agent consider the question posed by the user from the original perspective as well as its complementary one.
    Considering both perspectives mitigates framing bias and improves the consistency of the probability estimate.

    Parameters
    ----------
    positive: ExpertOpinion
        The expert opinion of expert under the user's original perspective.
    negative: ExpertOpinion
        The expert opinion of expert from the perspective complementary to the user's original perspective.
    beta_params : BetaParams
        The alpha and beta parameters for the consensus Beta distribution over both opinions

    Attributes
    ----------
    positive: ExpertOpinion
        The expert opinion of expert under the user's original perspective.
    negative: ExpertOpinion
        The expert opinion of expert from the perspective complementary to the user's original perspective.
    beta_params : BetaParams
        The alpha and beta parameters for the consensus Beta distribution over both opinions

    """
    positive: ExpertOpinion
    negative: ExpertOpinion
    beta_params: Optional[BetaParams] = None

    def model_post_init(self, __context: Any) -> None:
        self.negative.negative = True

    @property
    def prob_a(self):
        """Get the consensus probability of the expert opinion pair."""
        if self.beta_params is None:
            return (self.positive.prob_a + self.negative.prob_a) / 2
        else:
            return self.beta_params.alpha / (self.beta_params.alpha + self.beta_params.beta)

    @property
    def prob(self):
        """Get the consensus probability and its complement over the expert opinion pair."""
        return self.prob_a, 1 - self.prob_a

    @property
    def text(self):
        """Gets the text representation of the pair of expert opinions"""
        return "\n\n".join([self.positive.text, self.negative.text])


class BinaryPrediction(Prediction):
    """A class representing the output of a prediction request, containing both numerical results and explanatory text.

    This class encapsulates the prediction results returned from the chronulus API,
    including a unique identifier, descriptive text, and the numerical predictions in
    a pandas DataFrame format.

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.
    opinion_set : BinaryPair
        A set of opinions provided by the expert

    Attributes
    ----------
    _id : str
        Unique identifier for the prediction.

    """

    def __init__(self, _id: str, opinion_set: BinaryPair):
        super().__init__(_id)
        self._opinion_set = opinion_set

    @property
    def opinion_set(self) -> BinaryPair:
        """Gets the set of opinions provided by the expert."""
        return self._opinion_set

    @property
    def prob_a(self):
        """Get the consensus probability of the expert opinion set."""
        return self.opinion_set.prob_a

    @property
    def prob(self):
        """Get the consensus probability and its complement over the expert opinion set."""
        return self.prob_a, 1 - self.prob_a

    @property
    def text(self) -> str:
        """Get the text representation of the expert opinion set."""
        return self.opinion_set.text

    def to_dict(self):
        """Convert the prediction to a python dict

        Returns
        -------
        dict
            A python dict containing the prediction results.
        """

        return self.opinion_set.model_dump()


class BinaryPredictionSet:
    """
    A collection of BinaryPrediction results from BinaryPredictor

    The class provides access to aggregate functions over the collection predictions, including access to the
    Beta distribution estimated over the underlying predictions.

    Parameters
    ----------
    predictions : List[BinaryPrediction]
        The list of BinaryPredictions for each expert
    beta_params : BetaParams
        The alpha and beta parameters for the Beta distribution

    """

    def __init__(self, predictions: List[BinaryPrediction], beta_params: BetaParams):
        self.predictions = predictions
        self.beta_params = beta_params
        self.id_map = {p.id: i for i, p in enumerate(predictions)}

    @property
    def text(self):
        experts = []
        for i, pred in enumerate(self.predictions):
            expert = "\n\n".join([
                f"--- Expert {i + 1} ---",
                pred.text,
            ])
            experts.append(expert)
        return "\n\n".join(experts)

    def __len__(self):
        return len(self.predictions)

    @property
    def prob_a(self):
        alpha, beta = self.beta_params.alpha, self.beta_params.beta
        return alpha / (alpha + beta)

    @property
    def prob(self):
        return self.prob_a, 1 - self.prob_a

    def __getitem__(self, idx: Union[str, int,]):
        if isinstance(idx, str):
            return self.predictions[self.id_map[idx]]
        elif isinstance(idx, int):
            return self.predictions[idx]

    def __str__(self):
        return self.text

    def to_dict(self):
        """Convert the prediction set to a python dict

        Returns
        -------
        dict
            A python dict containing the prediction set results.
        """

        ps_dict = dict(
            predictions=[p.to_dict() for p in self.predictions],
            beta_params=self.beta_params.model_dump(),
            prob_a=self.prob_a,
            prob=self.prob,
        )

        return ps_dict
