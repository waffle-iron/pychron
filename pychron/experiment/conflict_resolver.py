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
from traits.api import HasTraits, Str, List, Instance
from traitsui.api import View, UItem, Item, EnumEditor, TableEditor
# ============= standard library imports ========================
# ============= local library imports  ==========================
from traitsui.table_column import ObjectColumn


class Conflict(HasTraits):
    queue_name = Str
    runspec = Instance('pychron.experiment.automated_run.spec.AutomatedRunSpec')
    identifier = Str
    position = Str
    experiment_id = Str
    experiment_ids = Str
    available_ids = List


class ConflictResolver(HasTraits):
    conflicts = List
    available_ids = List

    def apply(self):
        for c in self.conflicts:
            c.runspec.experiment_id = c.experiment_id

    def add_conflicts(self, qname, cs):
        for ai, exps in cs:
            self.conflicts.append(Conflict(queue_name=qname,
                                           runspec=ai,
                                           position=ai.position,
                                           experiment_id=ai.experiment_id,
                                           identifier=ai.identifier,
                                           experiment_ids=','.join(exps),
                                           available_ids=self.available_ids))

    def traits_view(self):
        cols = [ObjectColumn(name='queue_name', editable=False),
                ObjectColumn(name='identifier', editable=False),
                ObjectColumn(name='position', editable=False),
                ObjectColumn(name='experiment_id', editor=EnumEditor(name='available_ids')),
                ObjectColumn(name='experiment_ids', editable=False)]

        v = View(UItem('conflicts', editor=TableEditor(columns=cols)),
                 title='Resolve Experiment Conflicts',
                 resizable=True,
                 buttons=['OK', 'Cancel'])
        return v


if __name__ == '__main__':

    def main():
        from pychron.paths import paths
        paths.build('_dev')
        from pychron.core.helpers.logger_setup import logging_setup
        from pychron.experiment.automated_run.spec import AutomatedRunSpec
        logging_setup('dvcdb')
        from pychron.dvc.dvc_database import DVCDatabase
        from itertools import groupby
        db = DVCDatabase(kind='mysql', host='localhost', username='root', name='pychronmeta', password='Argon')
        db.connect()
        identifiers = ['63290', '63291']
        runs = [AutomatedRunSpec(identifier='63290', experiment_id='Cather_McIntoshd')]
        cr = ConflictResolver()
        experiments = {}
        with db.session_ctx():
            cr.available_ids = db.get_experiment_identifiers()
            eas = db.get_associated_experiments(identifiers)
            for idn, exps in groupby(eas, key=lambda x: x[1]):
                experiments[idn] = [e[0] for e in exps]
            conflicts = []
            for ai in runs:
                identifier = ai.identifier
                es = experiments[identifier]
                if ai.experiment_id not in es:
                    conflicts.append((ai, es))
            if conflicts:
                cr.add_conflicts('Foo', conflicts)

        if cr.conflicts:

            info = cr.edit_traits(kind='livemodal')
            if info.result:
                cr.apply()

        for ci in runs:
            print ci.identifier, ci.experiment_id


    from traits.api import Button

    class Demo(HasTraits):
        test = Button

        def traits_view(self):
            return View(Item('test'))
        def _test_fired(self):
            main()

    d=Demo()
    d.configure_traits()
# ============= EOF =============================================