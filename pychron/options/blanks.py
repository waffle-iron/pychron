# ===============================================================================
# Copyright 2015 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
from traits.api import List
from traitsui.api import EnumEditor
# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.options.blanks_views import VIEWS
from pychron.options.options import object_column, checkbox_column, MainOptions
from pychron.options.series import SeriesOptions
from pychron.pychron_constants import FIT_TYPES_INTERPOLATE, FIT_ERROR_TYPES


class BlanksMainOptions(MainOptions):
    def _get_columns(self):
        return [object_column(name='name'),
                checkbox_column(name='plot_enabled', label='Enabled'),
                checkbox_column(name='save_enabled', label='Save'),
                object_column(name='fit',
                              editor=EnumEditor(values=FIT_TYPES_INTERPOLATE),
                              width=75),
                object_column(name='error_type',
                              editor=EnumEditor(values=FIT_ERROR_TYPES),
                              width=75, label='Error'), ]


class BlanksOptions(SeriesOptions):
    subview_names = List(['Main', 'Blanks', 'Appearance'])
    _main_options_klass = BlanksMainOptions

    def _get_subview(self, name):
        return VIEWS[name]

# ============= EOF =============================================