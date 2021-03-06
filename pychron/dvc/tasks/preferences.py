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
from envisage.ui.tasks.preferences_pane import PreferencesPane
from traits.api import Str, Password
from traitsui.api import View, Item, VGroup, UItem
# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.database.tasks.connection_preferences import ConnectionPreferences, ConnectionPreferencesPane
from pychron.envisage.tasks.base_preferences_helper import BasePreferencesHelper


class DVCPreferences(BasePreferencesHelper):
    preferences_path = 'pychron.dvc'
    meta_repo_name = Str
    organization = Str
    github_user = Str
    github_password = Password
    default_team = Str
    work_offline_user = Str
    work_offline_password = Password
    work_offline_host = Str


class DVCDBConnectionPreferences(ConnectionPreferences):
    preferences_path = 'pychron.dvc.db'
    _adapter_klass = 'pychron.dvc.dvc_database.DVCDatabase'


class DVCDBConnectionPreferencesPane(ConnectionPreferencesPane):
    model_factory = DVCDBConnectionPreferences
    category = 'DVC'


class DVCPreferencesPane(PreferencesPane):
    model_factory = DVCPreferences
    category = 'DVC'

    def traits_view(self):
        repo = VGroup(Item('github_user', label='Username'),
                      Item('github_password', label='Password'),
                      label='Credentials', show_border=True)

        org = VGroup(UItem('organization'),
                     Item('default_team', tooltip='Name of the GitHub Team to add to new repositories'),
                     label='Organization', show_border=True)
        meta = VGroup(UItem('meta_repo_name'), label='Meta', show_border=True)
        # proj = VGroup(Item(''), label='Projects', show_border=True)
        offline = VGroup(Item('work_offline_host', label='Host'),
                         Item('work_offline_user', label='Username'),
                         Item('work_offline_password', label='Password'),
                         label='Work Offline',
                         show_border=True)

        v = View(VGroup(repo, VGroup(org, meta), label='Git',
                        show_border=True),
                 offline)
        return v

# class DVCPreferences(FavoritesPreferencesHelper):
#     preferences_path = 'pychron.dvc'
#     enabled = Bool
#     rsync_user = Str
#     rsync_port = CInt(22)
#     rsync_remote = Str
#     rsync_options = Str
#
#     repo_root = Str
#     repo_user = Str
#     repo_password = Password
#
#     def _get_attrs(self):
#         return ['fav_name',
#                 'rsync_user', 'rsync_remote', 'rsync_port', 'rsync_options',
#                 'repo_root', 'repo_user', 'repo_password']
#
#     def _get_values(self):
#         return [self.fav_name,
#                 self.rsync_user, self.rsync_remote, self.rsync_port, self.rsync_options,
#                 self.repo_root, self.repo_user, self.repo_password]
#
#     @on_trait_change('rsync+, repo+')
#     def attribute_changed(self, name, new):
#
#         if self.favorites:
#             attrs = self._get_attrs()
#             for i, fastr in enumerate(self.favorites):
#                 vs = fastr.split(',')
#                 if vs[0] == self.fav_name:
#                     aind = attrs.index(name)
#                     fa = fastr.split(',')
#                     fa[aind] = new
#                     fastr = ','.join(map(str, fa))
#                     self.favorites[i] = fastr
#                     self.selected = fastr
#                     break
#
#
# class DVCPreferencesPane(PreferencesPane):
#     model_factory = DVCPreferences
#     category = 'DVC'
#
#     def traits_view(self):
#         fav_grp = VGroup(Item('fav_name',
#                               show_label=False),
#                          Item('favorites',
#                               show_label=False,
#                               width=100,
#                               editor=ListStrEditor(
#                                   editable=False,
#                                   adapter=FavoritesAdapter(),
#                                   selected='object.selected')),
#                          HGroup(
#                              icon_button_editor('add_favorite', 'add',
#                                                 tooltip='Add saved connection'),
#                              icon_button_editor('delete_favorite', 'delete',
#                                                 tooltip='Delete saved connection')))
#         conn_grp = VGroup(Item('rsync_remote'),
#                           Item('rsync_user'),
#                           Item('rsync_port'),
#                           Item('rsync_options')
#                           )
#         cgrp = VGroup(HGroup(fav_grp, conn_grp),
#                       show_border=True,
#                       label='Connections')
#         ggrp = VGroup(Item('enabled', tooltip='Use the DVC backend instead of the central database'), label='General',
#                       show_border=True)
#         rgrp = VGroup(Item('repo_root'),
#                       Item('repo_user'),
#                       Item('repo_password'),
#                       label='Repo', show_border=True)
#         v = View(VGroup(ggrp, rgrp, cgrp))
#         return v

# ============= EOF =============================================



