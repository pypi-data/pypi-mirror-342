import pandas as pd
from typing import List

import numpy as np
from pandas import DataFrame
from pyPhasesML import FeatureExtraction as pyPhasesFeatureExtraction
from pyPhasesRecordloader import RecordSignal, Signal, Event, ChannelsNotPresent

from SleePyPhases.PSGEventManager import PSGEventManager

class RecordFeatureExtraction(pyPhasesFeatureExtraction):
    """batchManipulation for the physionet challenge 2023
    segmentSignal: Recordsignal of the segment with 18 EEG channels
    """

    def step(self, stepname: str, recordSignal: RecordSignal, eventlist: List[Event], channel=None, **options) -> Signal:
        if hasattr(self, stepname):
            # call method
            if channel is None:
                return getattr(self, stepname)(recordSignal, eventlist, **options)
            else:
                return getattr(self, stepname)(recordSignal, eventlist, channel, **options)
        else:
            raise Exception(f"FeatureExtraction '{stepname}' not found")
        
    def updateMetadataByStep(self, stepname: str, recordSignal: RecordSignal, eventlist: List[Event], metadata: pd.DataFrame, channel=None, **options):
        features = self.step(stepname, recordSignal, eventlist, channel, **options)

        if features is None:
            return None
        
        recordId = recordSignal.recordId
        # update row with index recordId and channel with features dict or create new if not exist
        
        for featureName, value in features.items():
            idx = (recordId, channel)
            if idx not in metadata.index:
                metadata.loc[idx, "recordId"] = recordId
                metadata.loc[idx, "channel"] = channel
                metadata.loc[idx, featureName] = value
            else:
                metadata.at[idx, featureName] = value

        return features


    def __init__(self, project) -> None:
        super().__init__()
        self.project = project

    def _SleepCycles(self, segmentSignal: RecordSignal, eventlist: List[Event]):
               
        stages = [e for e in eventlist if e.name in ["undefined", "W", "N1", "N2", "N3", "R"]]
        rem = [e for e in stages if e.name == "R"]
        nrem = [e for e in stages if e.name in ["N1", "N2", "N3"]]

        cycles = {'start': [], 'stop': []}

        # Find REM start and end times
        rem_starts = [rem[i].start for i in range(1, len(rem)) if rem[i].start - rem[i-1].end() > 1]
        rem_ends = [rem[i-1].end() for i in range(1, len(rem)) if rem[i].start - rem[i-1].end() > 1]

        if len(rem_ends) == 0 or len(nrem) == 0:
            return cycles
        
        # Set cycle start and stop times
        cycles['start'] = [nrem[0].start] + rem_ends + [rem[-1].end()]
        cycles['stop'] = [rem[0].start] + rem_starts + [nrem[-1].end()]

        # Apply duration mask (> 30 minutes)
        mask = np.array(cycles['stop']) - np.array(cycles['start']) > 30*60

        cycles["start"] = (np.array(cycles['start'] )[mask] // 30).tolist()
        cycles["stop"] = (np.array(cycles['stop'])[mask] // 30).tolist()

        # transform everything to integers
        cycles["start"] = [int(i) for i in cycles["start"]]
        cycles["stop"] = [int(i) for i in cycles["stop"]]

        # cycles in epochs (30 seconds)
        return cycles
        
    
    def _windowedBandpower(self, signal: Signal, lower, upper, windowsize):
        import scipy

        def bandpower(x, fs, fmin, fmax):
            f, Pxx = scipy.signal.periodogram(x, fs, window="hamming")
            ind_min = np.argmax(f > fmin) - 1
            ind_max = np.argmax(f > fmax)
            f_dist = f[1] - f[0]
            return sum(Pxx[ind_min:ind_max] * f_dist)

        windowsize = int(windowsize)
        bp = np.zeros(int(np.floor(signal.signal.size / windowsize)))
        for i in range(bp.size):
            x = signal.signal[i * windowsize : (i + 1) * windowsize]
            bp[i] = bandpower(x, signal.frequency, lower, upper)

        return bp

    def _swa(self, signal: Signal):
        from scipy.ndimage.filters import uniform_filter1d

        power_5s = self._windowedBandpower(signal, lower=1, upper=4.5, windowsize=5 * signal.frequency)
        power_epoch_mean = uniform_filter1d(power_5s, size=6, mode="mirror")[3::6]
        # filter according to felix implementation
        filterFactor = 3
        factor = np.insert(
            (filterFactor * power_epoch_mean[0:-1] < power_epoch_mean[1:]) * (filterFactor - 1) + 1, 0, 1
        )
        power_epoch_mean = power_epoch_mean / factor

        return power_epoch_mean
                

    def _ligtOffset(self, segmentSignal: RecordSignal, eventlist):
        ligthEvents = [e for e in eventlist if e.name in ["lightOn", "lightOff"]]
        
        offsetStart = 0
        if lightOff := [e for e in ligthEvents if e.name == "lightOff"]:
            offsetStart = lightOff[0].start
        
        offsetEnd = None
        if lightOn := [e for e in ligthEvents if e.name == "lightOn"]:
            offsetEnd = lightOn[0].start
        
        return offsetStart, offsetEnd
        
    def _updateEvents(self, eventlist, offsetStart, offsetEnd):
        
        # update events
        newEvents = []
        for event in eventlist:
            if offsetStart > 0:
                if event.end() <= offsetStart:
                    continue
                if event.start < offsetStart:
                    event.duration -= offsetStart - event.start
                    event.start = 0
                else:
                    event.start -= offsetStart
            if offsetEnd is not None:
                if event.start >= offsetEnd - offsetStart:
                    continue
                if event.end() > offsetEnd - offsetStart:
                    event.duration -= event.end() - offsetEnd + offsetStart
            newEvents.append(event)
        return newEvents

    # TODO: outsource to PSGEventManager
    def _tailorToSleepScoring(self, segmentSignal: RecordSignal, eventlist):

        sleepEventNames = ["R", "N1", "N2", "N3", "W"]
        sleepEvents = [e for e in eventlist if e.name in sleepEventNames]

        if len(sleepEvents) == 0:
            return segmentSignal, []
        
        # fix if the last sleep stage has no duration (should be fixed in Recordloader (Alice))
        if sleepEvents[-1].duration == 0:
            sleepEvents[-1].duration = 30

        offsetStart = sleepEvents[0].start
        offsetEnd = sleepEvents[-1].end()

        lightOff, lightOn = self._ligtOffset(segmentSignal, eventlist)
        if lightOff is not None:
            offsetStart = max(offsetStart, lightOff)
        if lightOn is not None:
            offsetEnd = min(offsetEnd, lightOn)

        segmentSignal.signalOffset(offsetStart, offsetEnd)

        newEvents = self._updateEvents(eventlist, offsetStart, offsetEnd)

        return segmentSignal, newEvents

    def _SWAandCycles(self, segmentSignal: RecordSignal, eventlist: List[Event], channel: str):

        cycles = self._SleepCycles(segmentSignal, eventlist)
        swa_cycles_n2n3 = DataFrame(index=range(len(cycles["start"])), columns=[channel])
        swa_cycles_all = DataFrame(index=range(len(cycles["start"])), columns=[channel])

        signal = segmentSignal.getSignalByName(channel)

        # check if the scoring is longer than the actual signal
        sleepEventNames = ["R", "N1", "N2", "N3", "W"]
        sleepEvents = [e for e in eventlist if e.name in sleepEventNames]        
        scoringLength = sleepEvents[-1].end() - sleepEvents[0].start
        signalLength = signal.signal.shape[0] / signal.frequency
        if scoringLength > signalLength:
            newLength = (len(signal.signal)/signal.frequency//30)*30
            newLength = min(newLength, signalLength)
            eventlist = self._updateEvents(eventlist, 0, newLength)
            signal.signal = signal.signal[:int(newLength*signal.frequency)]


        labelSignal = PSGEventManager().getEventSignalFromList(
            eventlist,
            int(len(signal.signal)/signal.frequency//30),
            targetFrequency=0.03333,
            forceGapBetweenEvents=False,
        )

        if "sleepStage" not in labelSignal:
            raise ChannelsNotPresent("SleepStagesAASM")
        
        labelSignal = labelSignal["sleepStage"]

        stage_mask = ((labelSignal == PSGEventManager.INDEX_NREM2) | (labelSignal == PSGEventManager.INDEX_NREM3)) * 1.0
        stage_mask[stage_mask == 0] = np.nan

        power_epoch_mean = self._swa(signal)
        assert len(power_epoch_mean) == len(labelSignal)

        signal_masked = stage_mask * power_epoch_mean

        for cycle_number, (start, end) in enumerate(zip(cycles["start"], cycles["stop"])):
            swa_cycles_all.loc[cycle_number, channel] = np.nanmean(
                power_epoch_mean[start:end]
            )
            swa_cycles_n2n3.loc[cycle_number, channel] = np.nanmean(
                signal_masked[start:end]
            )
        return swa_cycles_all, swa_cycles_n2n3, cycles
    

    def SWA3(self, segmentSignal: RecordSignal, eventlist: List[Event], channel: str):
        
        segmentSignal, eventlist = self._tailorToSleepScoring(segmentSignal, eventlist)
        if len(eventlist) == 0:
            return {}

        swa_cycles_all, swa_cycles_n2n3, cycles = self._SWAandCycles(segmentSignal, eventlist, channel)

        if len(cycles["start"]) == 0:
            return {}

        # erste höchste letzte
        return {
            "deltapower_0.5_all_first": swa_cycles_all.iloc[0].to_list()[0],
            "deltapower_0.5_all_max": swa_cycles_all.max().to_list()[0],
            "deltapower_0.5_all_last": swa_cycles_all.iloc[-1].to_list()[0],
            "deltapower_0.5_n2n3_first": swa_cycles_n2n3.iloc[0].to_list()[0],
            "deltapower_0.5_n2n3_max": swa_cycles_n2n3.max().to_list()[0],
            "deltapower_0.5_n2n3_last": swa_cycles_n2n3.iloc[-1].to_list()[0],
        }
    
    def REMCycleLength(self, segmentSignal: RecordSignal, eventlist: List[Event], channel: str):
        cycles = self._SleepCycles(segmentSignal, eventlist)

        lastStop = 0
        remEvents = [e for e in eventlist if e.name == "R"]

        ret = {
            "cycle-count": len(cycles["start"]),
        }
        frequencyFactor = 30
        
        for cycleNumber, (start, stop) in enumerate(zip(cycles["start"], cycles["stop"])):
            start *= frequencyFactor
            stop *= frequencyFactor
            # if lastStop > 0:
            remTime = sum([e.duration for e in remEvents if e.start >= lastStop and e.start < start])
            ret[f"cycle-{cycleNumber}-rem-duration"] = remTime

            lastStop = stop

        # remTime = sum([e.duration for e in remEvents if e.start >= lastStop and e.start < start])
        # ret[f"cycle-{cycleNumber}-rem-duration"] = remTime

        return ret
    
    def spindles(self, segmentSignal: RecordSignal, eventlist: List[Event], channel: str):
        from .external.sumo.sumo.scripts.a7.butter_filter import butter_bandpass_filter, downsample
        # from .external.sumo.a7.detect_spindles import detect_spindle
        from .external.sumo.sumo.scripts.predict_plain_data import SimpleDataset
        # from .external.sumo.sumo.predict_plain_data import A7
        import pytorch_lightning as pl
        from torch.utils.data import Dataset, DataLoader
        import torch
        from .external.sumo.sumo.model.sumo import SUMO
        from .external.sumo.sumo.config.config import Config
        # from .external.sumo.model.data import spindle_vect_to_indices

        config = Config('predict', create_dirs=False)

        def get_model(p):
            # p = Path(p)

            model_checkpoint = torch.load(p)

            model = SUMO(config)
            model.load_state_dict(model_checkpoint['state_dict'])

            return model

        eegSignal = segmentSignal.getSignalByName(channel)
        resample_rate = 100
        model_path = "SleePyPhases/external/sumo/sumo/output/final.ckpt"
        
        if len(eegSignal.signal) == 0:
            return None

        eegs = []
        eegSignal = downsample(butter_bandpass_filter(eegSignal.signal, 0.3, 30.0, eegSignal.frequency, 10), eegSignal.frequency, resample_rate)
        eegs.append(eegSignal)

        dataset = SimpleDataset(eegs)
        dataloader = DataLoader(dataset)
        model = get_model(model_path)
        trainer = pl.Trainer(num_sanity_val_steps=0, logger=False)
        predictions = trainer.predict(model, dataloader)
        pred = predictions[0]

        # spindles_a7 = A7(x, resample_rate)
        spindle_vect = pred[0].numpy()
        
        diff = np.diff(np.r_[0, spindle_vect, 0])  # be able to detect spindles at the start and end of vector
        spindles = np.c_[np.argwhere(diff == 1), np.argwhere(diff == -1)]  / resample_rate
        # spindles = spindle_vect_to_indices(spindle_vect) / resample_rate


        # frequencies, psd = signal.welch(eegs[0][s.start:s.end()], 
        #                                 fs=100,
        #                                 nperseg=min(256, s.duration),
        #                                 scaling='spectrum')
        # dominant_freq = frequencies[np.argmax(psd)]

        spindles = [Event("spindle", s[0], s[1] - s[0]) for s in spindles]

        
        return {
            "spindles-count": len(spindles),
            "spindles-mean-druation": np.array([s.duration for s in spindles]).mean()
        }
    
