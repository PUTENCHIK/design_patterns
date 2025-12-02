import unittest
from src.core.exceptions import OperationException
from src.dtos.nomenclature_group_dto import NomenclatureGroupDto
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.singletons.repository import Repository
from src.singletons.model_manager import ModelManager


class TestModelManager(unittest.TestCase):

    # При передаче методу add_model() DTO модели группы номенклатуры
    # возвращается модель, которая добавилась в репозиторий
    def test_modelmanager_addmodel_add_new_nomenclature_group_returns_model(self):
        # Подготовка
        name = "Товары"
        dto = NomenclatureGroupDto()
        dto.name = name
        # Действие
        group = ModelManager.add_model(
            Repository.nomenclature_group_key,
            NomenclatureGroupModel,
            dto
        )
        # Проверка
        assert group
        assert group.name == name
        assert Repository().get_by_name(name) == group
    
    # При изменении имени модели группы номенклатуры не выбрасывается
    # исключений, а имя у модели меняется
    def test_modelmanager_editmodel_edit_nomenclature_group_returns_edited_model(self):
        # Подготовка
        new_name = "товары"
        model = Repository().get_by_name("ингредиенты")
        dto = NomenclatureGroupDto()
        dto.name = new_name
        # Действие
        group = ModelManager.edit_model(
            model.unique_code,
            NomenclatureGroupModel,
            dto
        )
        # Проверка
        assert group
        assert group.name == new_name
        assert Repository().get_by_name(new_name) == group
    
    # При удалении группы номенклатуры её невозможно получить из репозитория
    def test_modelmanager_deletemodel_delete_nomenclature_group_returns_none(self):
        # Подготовка
        model = Repository().get_by_name("товары")
        code = model.unique_code
        # Действие
        result = ModelManager.delete_model(
            code,
            NomenclatureGroupModel,
        )
        # Проверка
        assert result
        assert Repository().get_by_unique_code(code) is None
    
    def test_modelmanager_deletemodel_delete_base_unit_raises_exception(self):
        # Подготовка
        model = Repository().get_by_name("грамм")
        code = model.unique_code
        # Действие и проверка
        with self.assertRaises(OperationException):
            ModelManager.delete_model(
                code,
                MeasureUnitModel,
            )



if __name__ == "__main__":
    unittest.main()
