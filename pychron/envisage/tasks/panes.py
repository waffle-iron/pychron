# ===============================================================================
# Copyright 2014 Jake Ross
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
from apptools.preferences.preferences_helper import PreferencesHelper
from envisage.ui.tasks.preferences_pane import PreferencesPane
from traits.api import HasTraits, Button, Str, Int, Bool, String, Property
from traitsui.api import View, Item, UItem, HGroup, VGroup
# ============= standard library imports ========================
import re
# ============= local library imports  ==========================
from pychron.core.ui.custom_label_editor import CustomLabel
from pychron.envisage.icon_button_editor import icon_button_editor
from pychron.envisage.tasks.base_preferences_helper import GitRepoPreferencesHelper


class GeneralPreferences(GitRepoPreferencesHelper):
    preferences_path = 'pychron.general'


class GeneralPreferencesPane(PreferencesPane):
    model_factory = GeneralPreferences
    category = 'General'
    def traits_view(self):
        v = View(VGroup(HGroup(Item('remote', label='Laboratory Repo'),
                               icon_button_editor('test_connection', 'test_connection')),
                        CustomLabel('remote_status',
                                    color_name='remote_status_color'),
                        show_border=True))
        return v

#============= EOF =============================================


