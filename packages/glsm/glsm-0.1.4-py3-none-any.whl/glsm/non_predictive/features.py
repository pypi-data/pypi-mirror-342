from pydantic import BaseModel, validator
from typing import Union
import pandas as pd


class _OptionsDataFrame(BaseModel):
    """
    This class is used to validate the options types of the DataFrame.
    Don't use it directly.
    """

    label: str
    is_ICP: bool = False
    points: Union[float, int, None] = None


class Feature(BaseModel):
    """
    A feature of a model that can be used to score a lead.
    """

    name: str
    options_df: pd.DataFrame
    weight: float
    normalized_weight: float = None

    class Config:
        arbitrary_types_allowed = True

    @validator('options_df', pre=True)
    def validate_options_df(cls, options_df: pd.DataFrame, values: dict) -> pd.DataFrame:
        options_dicts = options_df.to_dict(orient='records')

        # Pydantic will raise a ValidationError if the types are not correct
        [_OptionsDataFrame(**options_dict) for options_dict in options_dicts]

        # There must be at least one ICP option
        if options_df.is_ICP.sum() == 0:
            raise ValueError('At least one option must be an ICP')

        # ICP options need to be grouped together
        if options_df.is_ICP.sum() > 1:
            icp_options_df = options_df[options_df.is_ICP == True]

            for i in range(len(icp_options_df.index) - 1):
                idx = icp_options_df.index[i]
                idx_plus_1 = icp_options_df.index[i + 1]
                if idx_plus_1 - idx > 1:
                    raise ValueError("ICP options must be grouped together")

        options_df['Feature Name'] = values.get('name')

        return options_df

    def get_points(self, label: str) -> float:
        """
        Returns the points assigned to the label of a feature.
        """
        for item in self.options_df.values:
            if item[0] == label:
                return item[2] if type(item[2]) in [float, int] else item[3]
        raise ValueError(f'Label {label} not found in options Data Frame')
