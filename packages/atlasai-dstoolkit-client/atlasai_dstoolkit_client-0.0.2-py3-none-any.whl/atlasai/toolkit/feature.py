# Copyright 2025 AtlasAI PBC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
import pandas as pd

from . import api, constants, utils


def export(*args, **kwargs):
    fe = FeatureExport(*args, **kwargs)
    utils.show_page(fe.page)
    return fe

class FeatureExport:
    def __init__(self, search, id=None, *args, **kwargs):
        self.id = id or uuid.uuid4()
        self._search = search
        self._export = None

    def __repr__(self):
        return f'FeatureExport({self._search.id})'

    def __str__(self):
        return f'FeatureExport({self._search.id})'

    @property
    def page(self):
        return f'{constants.DS_TOOLKIT_URL}/feature/export/{self.id}?feature_search_id={self._search.id}'

    @property
    def export(self):
        return self._export

    @property
    def search(self):
        return self._search.search

    def details(self):
        if self.export is None or self.export.status not in ['completed', 'failed']:
            self._export = self._details()
        return self.export

    def refresh(self):
        self._export = self._details()
        return self.export

    def results(self, limit=None) -> pd.DataFrame:
        if self.export.status not in ['completed', 'failed']:
            raise Exception(f'Export state is: {self.export.status}')

        path = getattr(self.export, 'url_path', getattr(self.export, 'output_path'))
        if not path:
            raise Exception('Path not found')

        df = pd.read_parquet(path, engine='pyarrow')
        if limit:
            df = df.head(limit)
        return df

    def _details(self):
        resource = f'/feature/export/{self._search.id}/details'
        _, data = api._get(resource=resource)
        return data['data']
