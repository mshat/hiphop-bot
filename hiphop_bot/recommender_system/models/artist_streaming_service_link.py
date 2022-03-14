from typing import List, Tuple, Dict
from hiphop_bot.db.abstract_model import Model, ModelError
from hiphop_bot.recommender_system.models.streaming_service import StreamingServiceModel


class _StreamingServiceLinks:
    _streaming_links: Dict[str, str]

    def __init__(self, streaming_links: Dict[str, str] = None):
        self._streaming_links = dict() if streaming_links is None else streaming_links

    def get_link_by_streaming_name(self, streaming_name: str) -> str | None:
        # check if streaming_name exists
        streaming_service_model = StreamingServiceModel()
        if streaming_name not in streaming_service_model.get_streaming_services_names():
            raise ModelError("Streaming service with that name is not in the database ")
        if streaming_name in self._streaming_links:
            return self._streaming_links[streaming_name]
        else:
            return None

    @property
    def streaming_links(self) -> Dict[str, str]:
        return self._streaming_links

    def add_link(self, streaming_name: str, link: str):
        self._streaming_links.update({streaming_name: link})

    def __str__(self):
        return f'{self._streaming_links}'

    def __repr__(self):
        return self.__str__()


class _ArtistStreamingServiceLinks:
    def __init__(self, artist_name: str, streaming_service_links: _StreamingServiceLinks):
        self.artist_name = artist_name
        self.links = streaming_service_links

    def __str__(self):
        return f'ArtistStreamingServiceLinks {self.artist_name} {self.links}'

    def __repr__(self):
        return self.__str__()


class ArtistStreamingServiceLinkModel(Model):
    def __init__(self):
        super().__init__('streaming_service_link', _ArtistStreamingServiceLinks)

        self._get_all_query = (
            "select a.name, ss.name, link "
            f"from {self._table_name} as ssl "
            "inner join artist as a on ssl.artist_id = a.id "
            "inner join streaming_service as ss on ssl.streaming_service_id = ss.id;"
        )

    def get_all(self) -> List[_ArtistStreamingServiceLinks]:
        artist_links_dict: Dict[str, _StreamingServiceLinks] = self.get_artist_links_dict()
        res = []
        for artist_name, streaming_service_links in artist_links_dict.items():
            res.append(_ArtistStreamingServiceLinks(artist_name, streaming_service_links))
        return res

    def get_artist_links_dict(self) -> Dict[str, _StreamingServiceLinks]:
        artist_links_dict = {}
        streaming_service_links_raw = self._raw_select(self._get_all_query)
        for streaming_service_link in streaming_service_links_raw:
            artist_name = streaming_service_link[0]
            streaming_name = streaming_service_link[1]
            link = streaming_service_link[2]

            if artist_name not in artist_links_dict:
                artist_links_dict[artist_name] = _StreamingServiceLinks()

            artist_links_dict[artist_name].add_link(streaming_name, link)
        return artist_links_dict

