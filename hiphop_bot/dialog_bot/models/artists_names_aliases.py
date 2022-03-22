from typing import List, Iterable
from hiphop_bot.db.abstract_model import Model, ModelUniqueViolationError, ModelError
from hiphop_bot.base_models.model_object_class import BaseModelObject
from hiphop_bot.dialog_bot.services.tools.debug_print import debug_print
from hiphop_bot.dialog_bot.config import DEBUG_MODEL


class _ArtistsNamesAliases(BaseModelObject):
    def __init__(self, db_row_id: int, artist_name: str, aliases: List[str]):
        super().__init__(db_row_id)
        self.artist_name = artist_name
        self.aliases = aliases

    def __str__(self):
        return f'ArtistsNamesAliases: {self.artist_name, self.aliases}'

    def __repr__(self):
        return self.__str__()


class ArtistsNamesAliasesModel(Model):
    def __init__(self):
        super().__init__('artists_names_aliases', _ArtistsNamesAliases)

        self._get_all_query = (
            "SELECT ana.id, a.name, ana.aliases "
            f"from {self._table_name} as ana "
            f"inner join artist as a on a.id = ana.artist_id "
        )

    def get_all(self) -> List[_ArtistsNamesAliases]:
        return super().get_all()

    def get_by_artist_name(self, artist_name: str) -> _ArtistsNamesAliases | None:
        query = self._get_all_query + f" where a.name = '{artist_name}'"
        res = self._select_model_objects(query)
        if res:
            return res[0]
        else:
            return None

    def get_by_artist_id(self, artist_id: int) -> _ArtistsNamesAliases | None:
        query = self._get_all_query + f" where artist_id = '{artist_id}'"
        res = self._select_model_objects(query)
        if res:
            return res[0]
        else:
            return None

    def _convert_aliases_list_to_db_array(self, aliases: Iterable[str]) -> str:
        return '{' + ','.join(aliases) + '}'

    def add_record(self, artist_id: int, aliases: List[str]):
        aliases = [alias.lower() for alias in aliases]
        query = (
            f'insert into {self._table_name} (artist_id, aliases) '
            f"VALUES(%s, %s);"
        )
        values = (artist_id, self._convert_aliases_list_to_db_array(aliases))

        try:
            added_records_number = self._insert(query, values)
            if added_records_number < 1:
                raise ModelError('Failed to add record')
        except ModelUniqueViolationError:
            raise ModelError('Aliases for artist with this id already exist. Try to use update_aliases method')

    def update_aliases(
            self,
            artist_id: int = None,
            additional_aliases: List[str] = None,
            aliases_to_remove: List[str] = None):
        if not additional_aliases and not aliases_to_remove:
            raise ModelError('Failed to update record: additional_aliases and aliases_to_remove is None')

        artist = self.get_by_artist_id(artist_id)
        if not artist:
            raise ModelError('Failed to update record: artist with this id does not exist in the db')

        current_aliases = artist.aliases
        if aliases_to_remove:
            current_aliases = [alias for alias in current_aliases if alias not in aliases_to_remove]
        if additional_aliases:
            new_aliases = current_aliases + additional_aliases
        else:
            new_aliases = current_aliases

        new_aliases = set(new_aliases)

        if new_aliases == set(artist.aliases):
            debug_print(DEBUG_MODEL, f'[MODEL] [ArtistsNamesAliasesModel] Неудачная попытка обновить псевдонимы '
                                     f'артиста: новый список псевдонимов совпадает с текущим')
            return

        new_aliases = self._convert_aliases_list_to_db_array(new_aliases)
        query = (f"update {self._table_name} "
                 f"set aliases = '{new_aliases}' "
                 f"where artist_id={artist_id} ")

        updated_records_number = self._update(query)
        if updated_records_number < 1:
            raise ModelError('Failed to add record')
