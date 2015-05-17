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
import os

from pyface.tasks.action.schema import SToolBar, SMenu
from pyface.tasks.action.schema_addition import SchemaAddition
from pyface.tasks.task_layout import TaskLayout, PaneItem, Splitter
from pyface.timer.do_later import do_after
from traits.api import Instance

# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.core.codetools.inspection import caller
from pychron.paths import paths
from pychron.pipeline.engine import PipelineEngine
from pychron.pipeline.state import EngineState
from pychron.pipeline.tasks.actions import RunAction, SavePipelineTemplateAction
from pychron.pipeline.tasks.panes import PipelinePane, AnalysesPane
from pychron.envisage.browser.browser_task import BaseBrowserTask
from pychron.processing.tasks.recall.recall_editor import RecallEditor

DEBUG = True


class DataMenu(SMenu):
    id = 'data.menu'
    name = 'Data'


class PipelineTask(BaseBrowserTask):
    name = 'Pipeline Processing'
    engine = Instance(PipelineEngine, ())
    tool_bars = [SToolBar(RunAction(),
                          SavePipelineTemplateAction())]

    def activated(self):
        super(PipelineTask, self).activated()

        dvc = self.application.get_service('pychron.dvc.dvc.DVC')
        self.engine.dvc = dvc
        self.engine.browser_model = self.browser_model
        self.engine.on_trait_change(self._handle_run_needed, 'run_needed')
        self.engine.on_trait_change(self._handle_recall, 'recall_analyses_needed')

        self.engine.task = self
        if DEBUG:
            do_after(500, self._debug)

    def _debug(self):

        self.engine.set_template('test2')
        # self.engine.add_data()
        self.engine.select_default()
        # self.engine.add_is
        # self.engine.add_grouping(run=False)
        # self.engine.add_test_filter()
        # self.engine.add_ideogram(run=False)
        # self.engine.add_series(run=False)

        # self.engine.add_test_filter()
        # self.engine.add_ideogram()
        # self.engine.add_pdf_figure_node()
        # self.engine.add_spectrum()

        self.run()

    def prepare_destroy(self):
        pass

    def create_dock_panes(self):
        panes = [PipelinePane(model=self.engine),
                 AnalysesPane(model=self.engine)]
        return panes

    # toolbar actions
    def save_pipeline_template(self):
        # path = self.save_file_dialog()
        # path = '/Users/ross/Sandbox/template.yaml'
        path = os.path.join(paths.pipeline_template_dir, 'test.yaml')
        if path:
            self.engine.save_pipeline_template(path)

    @caller
    def run(self):
        self._run_pipeline()

    def _close_editor(self, editor):
        for e in self.editor_area.editors:
            if e.name == editor.name:
                self.close_editor(e)
                break

    def _run_pipeline(self):
        self.debug('run pipeline')
        state = EngineState()

        self.engine.run(state)

        self.close_all()
        for editor in state.editors:
            self._close_editor(editor)
            self._open_editor(editor)

        self.engine.post_run(state)

    def _default_layout_default(self):
        return TaskLayout(left=Splitter(PaneItem('pychron.pipeline.pane',
                                                 width=200),
                                        PaneItem('pychron.pipeline.analyses',
                                                 width=200)))

    def _extra_actions_default(self):
        sas = (('MenuBar', DataMenu, {'before': 'tools.menu', 'after': 'view.menu'}),
               ('MenuBar/data.menu', RunAction, {}))
        return [self._sa_factory(path, factory, **kw) for path, factory, kw in sas]

    def _sa_factory(self, path, factory, **kw):
        return SchemaAddition(path=path, factory=factory, **kw)

    # handlers
    def _active_editor_changed(self, new):
        if new:
            self.engine.select_node_by_editor(new)

    def _handle_run_needed(self, new):
        self.debug('run needed for {}'.format(new))
        self.run()

        if new in self.engine.pipeline.nodes:
            self.engine.selected = new

    def _handle_recall(self, new):
        print new
        for ai in new:
            editor = RecallEditor(model=ai)
            self._open_editor(editor)
        # return [SchemaAddition(path='MenuBar',
        # before='tools.menu',
        #                        after='view.menu',
        #                        factory= DataMenu),  # lambda : SMenu(id='data.menu', name='Data')),
        #
        #         SchemaAddition(path='MenuBar/data.menu',
        #                        factory=RunAction)]
# ============= EOF =============================================


