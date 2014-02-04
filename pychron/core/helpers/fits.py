#===============================================================================
# Copyright 2012 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================

#============= enthought library imports =======================
#============= standard library imports ========================

#============= local library imports  ==========================


def convert_fit(f):
    err = 'SEM'
    if isinstance(f, tuple):
        f, err = f

    if isinstance(f, (str, unicode)):
        f = f.lower()
        fits = ['linear', 'parabolic', 'cubic']
        if '_' in f:

            try:
                f, err = f.split('_')
                err = err.upper()
            except ValueError:
                return None, None

        if f in fits:
            f = fits.index(f) + 1
        elif f.startswith('average'):
            f = 'average'
            if not err:
                err = 'SEM' if 'sem' in f else 'SD'
        elif f.startswith('weightedmean'):
            f = 'weightedmean'
            if not err:
                err = 'SEM' if 'sem' in f else 'SD'
        else:
            f = None

    return f, err


#============= EOF =============================================

