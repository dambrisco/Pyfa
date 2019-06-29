# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


from eos.utils.spoolSupport import SpoolType, SpoolOptions
from gui.utils.numberFormatter import roundToPrec
from .base import FitGraph, XDef, YDef, Input, VectorDef


class FitDamageStatsGraph(FitGraph):

    # UI stuff
    name = 'Damage Stats'
    xDefs = [
        XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km')),
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
        XDef(handle='tgtSpeed', unit='m/s', label='Target speed', mainInput=('tgtSpeed', '%')),
        XDef(handle='tgtSpeed', unit='%', label='Target speed', mainInput=('tgtSpeed', '%')),
        XDef(handle='tgtSigRad', unit='m', label='Target signature radius', mainInput=('tgtSigRad', '%')),
        XDef(handle='tgtSigRad', unit='%', label='Target signature radius', mainInput=('tgtSigRad', '%'))]
    yDefs = [
        YDef(handle='dps', unit=None, label='DPS'),
        YDef(handle='volley', unit=None, label='Volley'),
        YDef(handle='damage', unit=None, label='Damage inflicted')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=None, defaultRange=(0, 80), mainOnly=False),
        Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=50, defaultRange=(0, 100), mainOnly=False),
        Input(handle='tgtSpeed', unit='%', label='Target speed', iconID=1389, defaultValue=100, defaultRange=(0, 100), mainOnly=False),
        Input(handle='tgtSigRad', unit='%', label='Target signature', iconID=1390, defaultValue=100, defaultRange=(100, 200), mainOnly=True)]
    srcVectorDef = VectorDef(lengthHandle='atkSpeed', lengthUnit='%', angleHandle='atkAngle', angleUnit='degrees', label='Attacker')
    tgtVectorDef = VectorDef(lengthHandle='tgtSpeed', lengthUnit='%', angleHandle='tgtAngle', angleUnit='degrees', label='Target')
    hasTargets = True

    # Calculation stuff
    _normalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v * 1000,
        ('atkSpeed', '%'): lambda v, fit, tgt: v / 100 * fit.ship.getModifiedItemAttr('maxVelocity'),
        #('tgtSpeed', '%'): lambda v, fit, tgt: v / 100 * tgt.ship.getModifiedItemAttr('maxVelocity'),
        #('tgtSigRad', '%'): lambda v, fit, tgt: v / 100 * fit.ship.getModifiedItemAttr('signatureRadius')
    }
    _limiters = {
        'time': lambda fit, tgt: (0, 2500)}
    _denormalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v / 1000,
        #('tgtSpeed', '%'): lambda v, fit, tgt: v * 100 / tgt.ship.getModifiedItemAttr('maxVelocity'),
        #('tgtSigRad', '%'): lambda v, fit, tgt: v * 100 / fit.ship.getModifiedItemAttr('signatureRadius')
    }

    def _distance2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _distance2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _distance2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2damage(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        minX, maxX = mainInput[1]
        self._generateTimeCacheDmg(fit, maxX)
        cache = self._calcCache[fit.ID]['timeDmg']
        currentY = None
        for time in sorted(cache):
            prevY = currentY
            currentX = time / 1000
            currentY = roundToPrec(cache[time], 6)
            if currentX < minX:
                continue
            # First set of data points
            if not xs:
                # Start at exactly requested time, at last known value
                initialY = prevY or 0
                xs.append(minX)
                ys.append(initialY)
                # If current time is bigger then starting, extend plot to that time with old value
                if currentX > minX:
                    xs.append(currentX)
                    ys.append(initialY)
                # If new value is different, extend it with new point to the new value
                if currentY != prevY:
                    xs.append(currentX)
                    ys.append(currentY)
                continue
            # Last data point
            if currentX >= maxX:
                xs.append(maxX)
                ys.append(prevY)
                break
            # Anything in-between
            if currentY != prevY:
                if prevY is not None:
                    xs.append(currentX)
                    ys.append(prevY)
                xs.append(currentX)
                ys.append(currentY)
        return xs, ys

    def _tgtSpeed2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSpeed2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSpeed2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    _getters = {
        ('distance', 'dps'): _distance2dps,
        ('distance', 'volley'): _distance2volley,
        ('distance', 'damage'): _distance2damage,
        ('time', 'dps'): _time2dps,
        ('time', 'volley'): _time2volley,
        ('time', 'damage'): _time2damage,
        ('tgtSpeed', 'dps'): _tgtSpeed2dps,
        ('tgtSpeed', 'volley'): _tgtSpeed2volley,
        ('tgtSpeed', 'damage'): _tgtSpeed2damage,
        ('tgtSigRad', 'dps'): _tgtSigRad2dps,
        ('tgtSigRad', 'volley'): _tgtSigRad2volley,
        ('tgtSigRad', 'damage'): _tgtSigRad2damage}

    # Cache generation
    def _generateTimeCacheDmg(self, fit, maxTime):
        if fit.ID in self._calcCache and 'timeDmg' in self._calcCache[fit.ID]:
            return

        fitCache = self._calcCache.setdefault(fit.ID, {})
        cache = fitCache['timeDmg'] = {}

        def addDmg(addedTime, addedDmg):
            if addedDmg == 0:
                return
            if addedTime not in cache:
                prevTime = max((t for t in cache if t < addedTime), default=None)
                if prevTime is None:
                    cache[addedTime] = 0
                else:
                    cache[addedTime] = cache[prevTime]
            for time in (t for t in cache if t >= addedTime):
                cache[time] += addedDmg

        # We'll handle calculations in milliseconds
        maxTime = maxTime * 1000
        for mod in fit.modules:
            if not mod.isDealingDamage():
                continue
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTime, volley in volleyParams.items():
                    addDmg(currentTime + volleyTime, volley.total)
                if inactiveTime == 0:
                    nonstopCycles += 1
                else:
                    nonstopCycles = 0
                if currentTime > maxTime:
                    break
                currentTime += cycleTime + inactiveTime
        for drone in fit.drones:
            if not drone.isDealingDamage():
                continue
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            volleyParams = drone.getVolleyParameters()
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                for volleyTime, volley in volleyParams.items():
                    addDmg(currentTime + volleyTime, volley.total)
                if currentTime > maxTime:
                    break
                currentTime += cycleTime + inactiveTime
        for fighter in fit.fighters:
            if not fighter.isDealingDamage():
                continue
            cycleParams = fighter.getCycleParametersPerEffectOptimizedDps(reloadOverride=True)
            if cycleParams is None:
                continue
            volleyParams = fighter.getVolleyParametersPerEffect()
            for effectID, abilityCycleParams in cycleParams.items():
                if effectID not in volleyParams:
                    continue
                currentTime = 0
                abilityVolleyParams = volleyParams[effectID]
                for cycleTime, inactiveTime in abilityCycleParams.iterCycles():
                    for volleyTime, volley in abilityVolleyParams.items():
                        addDmg(currentTime + volleyTime, volley.total)
                    if currentTime > maxTime:
                        break
                    currentTime += cycleTime + inactiveTime



FitDamageStatsGraph.register()
