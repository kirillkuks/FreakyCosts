from typing import Dict

import openpyxl

from characters_list import CharacterCost


# TODO: save constelation input
class ExcelSaver:
    class _WorkbookContext:
        row: int = 0
        column: int = 0

        def get_cell_name(self) -> str:
            excel_row = self.row + 1
            excel_column = ord('A') # TODO: support AA, AB, etc

            excel_column_as_str = chr(excel_column + self.column)
            return f'{excel_column_as_str}{excel_row}'

    def __init__(self):
        self.restore_context()

    def restore_context(self):
        self._workbook_context = ExcelSaver._WorkbookContext()

    def save(self, save_path: str, costelation_data: Dict[str, CharacterCost]):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        characters = costelation_data.keys()

        for character_name in characters:
            cost = costelation_data[character_name]
            self._process_characrter(sheet, character_name, cost)

        self.restore_context()
        self._process_control_panel(sheet, costelation_data)

        self.restore_context()
        self._process_cost_calculation(sheet, len(characters))

        workbook.save(f'{save_path}.xlsx')

    def _get_const_input_column(self) -> int:
        return CharacterCost.get_constelations_count() + 2
    
    def _get_const_output_column(self) -> int:
        return self._get_const_input_column() + 1
    
    def _get_cost_table_start_column(self) -> int:
        return 1
    
    def _process_characrter(self, sheet, character_name: str, costs_data: CharacterCost):
        sheet[self._workbook_context.get_cell_name()] = character_name
        self._workbook_context.column += 1

        for constelation_idx in range(CharacterCost.get_constelations_count()):
            sheet[self._workbook_context.get_cell_name()] = costs_data.get_constelation_value_by_index(constelation_idx)
            self._workbook_context.column += 1

        self._workbook_context.row += 1
        self._workbook_context.column = 0

    def _process_control_panel(self, sheet, constelation_data: Dict[str, CharacterCost]):
        self._workbook_context.column = self._get_const_input_column()
        characters_num = len(constelation_data)

        for _ in range(characters_num):
            sheet[self._workbook_context.get_cell_name()] = -1
            self._workbook_context.row += 1

    def _process_cost_calculation(self, sheet, characters_num: int):
        self._workbook_context.column = self._get_const_output_column()

        cost_formula_context = ExcelSaver._WorkbookContext()
        constelation_input_context = ExcelSaver._WorkbookContext()
        constelation_input_context.column = self._get_const_input_column()

        for _ in range(characters_num):
            formula = '='
            cost_formula_context.column = self._get_cost_table_start_column()

            for constelation_idx in range(CharacterCost.get_constelations_count()):
                if constelation_idx > 0:
                    formula += '+'

                formula += f'{cost_formula_context.get_cell_name()}'
                formula += '*'
                formula += f'IF({constelation_input_context.get_cell_name()}={constelation_idx}, 1, 0)'

                cost_formula_context.column += 1

            cost_formula_context.row += 1
            constelation_input_context.row += 1

            sheet[self._workbook_context.get_cell_name()] = formula
            self._workbook_context.row += 1

        self._process_accum_cost_output(sheet, characters_num)

    def _process_accum_cost_output(self, sheet, characters_num: int):
        self.restore_context()
        self._workbook_context.column = self._get_const_output_column()

        accum_cost_formula = '='
        for _ in range(characters_num):
            accum_cost_formula += f'{self._workbook_context.get_cell_name()}+'
            self._workbook_context.row += 1
        accum_cost_formula = accum_cost_formula[:-1]
        
        sheet[self._workbook_context.get_cell_name()] = accum_cost_formula
