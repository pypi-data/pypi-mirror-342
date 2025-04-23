'''
    Excel reader module
'''

import pandas
import numpy

class ReadExcel:
    '''
        Excel reader class
    '''
    __slots__: list[str] = ["path",
                            "data"]

    def __init__(self,
                 path: str,
                 read_on_init: bool = False) -> None:
        '''
            Excel reader class

            .. code-block:: python
                xlsx = ReadExcel(path = "example.xlsx",
                                 read_on_init = True)

            :param path: :class:`str` Path to the excel
            :param read_on_init: :class:`Optional(bool)` Read excel's content on init. Defaults to `False`
        ''' # pylint: disable=line-too-long
        self.path: str = path
        self.data: pandas.DataFrame = self.read() if read_on_init else None


    def read(self) -> None:
        '''
            Read the excel file

            .. code-block:: python
                # Only need if ReadExcel.read_on_init was left empty or set to False on init
                xlsx.read()
        '''
        self.data = pandas.read_excel(self.path)


    def get_sheet_names(self) -> list:
        '''
            Get the sheet names of the excel file

            .. code-block:: python
                sheets = xlsx.get_sheet_names()
        '''
        return pandas.ExcelFile(self.path).sheet_names


    def get_sheet_content(self,
                          sheet_name: str) -> pandas.DataFrame:
        '''
            Get the content of a sheet

            .. code-block:: python
                pd_frame = xlsx.get_sheet_content(sheet_name = "example_sheet_name")

            :param sheet_name: :class:`str` Sheet's name
        '''
        return pandas.read_excel(self.path, sheet_name)


    def get_sheet_content_to_list(self,
                                  sheet_name: str) -> list[list[any]]:
        '''
            Get the content of a sheet in list

            .. code-block:: python
                data_matrix = xlsx.get_sheet_content_to_list(sheet_name = "example_sheet_name")

            :param sheet_name: :class:`str` Sheet's name
        '''
        return pandas.read_excel(self.path,
                                 sheet_name,
                                 header = None).replace({numpy.nan: None}).values.tolist()
