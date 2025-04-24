from typing import List

import numpy as np
from pyPhasesML import FeatureExtraction as pyPhasesFeatureExtraction
from pyPhasesML import ModelManager
from pyPhasesRecordloader import RecordSignal, Event

from .DataAugmentation import DataAugmentation


class FeatureExtraction(pyPhasesFeatureExtraction):
    """augmentation for the physionet challenge 2023
    segmentSignal: Recordsignal of the segment with 18 EEG channels
    """

    def __init__(self, project) -> None:
        super().__init__()
        self.project = project

    def time(self, segmentSignal: RecordSignal):
        segmentLength = segmentSignal.getShape()[1]
        # segmentLengthInHOurs = segmentLength / segmentSignal.targetFrequency / 3600
        # hour, minutes = segmentSignal.start.split(":")
        # startTimeInHours = int(hour) + int(minutes) / 60
        # endTimeInHours = startTimeInHours + segmentLengthInHOurs
        hour = segmentSignal.start
        endTimeInHours = hour + 1
        return np.linspace(hour, endTimeInHours, segmentLength)

    def featureModel(self, segmentSignal: RecordSignal, featureName: str, xChannels: List[str]):
        import torch
        useGPU = torch.cuda.is_available() and False
        with self.project:
            config = self.project.config["featureConfigs", featureName]
            self.project.config.update(config)
            self.project.addConfig(config)

            self.project.trigger("configChanged", None)
            self.project.setConfig("trainingParameter.batchSize", 1)
            self.project.setConfig("recordWise", True)

            modelPath = self.project.getConfig("featureModel", torch)

            # this is needed for mutlithreading
            ModelManager.loadModel(self.project)
            # get feature model
            model = ModelManager.getModel(True)
            model.useGPU = useGPU
            state = model.load(modelPath)
            model.loadState(state)
            featureModel = model.model.eval()

            featureModel = featureModel.cuda() if useGPU else featureModel.cpu()

            # we assum that the segment is already preprocessed for the model
            array = segmentSignal.getSignalArray(xChannels, transpose=True)

            da = DataAugmentation(self.project.config, self.project.getConfig("datasetSplit"), recordAnnotations={})
            array, _ = da.augmentSegment(array, None)
            array = array.transpose(2, 1, 0)

            features = model.predict(array, get_likelihood=True)
            _, features = da.restoreLength(None, features, length=segmentSignal.getShape()[1])
            features = features[:, :, 1]

        return features

    def spindles(self, segmentSignal: RecordSignal): #xChannels: List[str]
        from .external.sumo.a7.butter_filter import butter_bandpass_filter, downsample
        # from .external.sumo.a7.detect_spindles import detect_spindle
        from .external.sumo.predict_plain_data import SimpleDataset
        from .external.sumo.predict_plain_data import A7
        import pytorch_lightning as pl
        from torch.utils.data import Dataset, DataLoader
        import torch
        from .external.sumo.model.sumo import SUMO
        from .external.sumo.model.config import Config
        # from .external.sumo.model.data import spindle_vect_to_indices

        config = Config('predict', create_dirs=False)

        def get_model(p):
            # p = Path(p)

            model_checkpoint = torch.load(p)

            model = SUMO(config)
            model.load_state_dict(model_checkpoint['state_dict'])

            return model

        eegSignals = [s for s in segmentSignal.signals if s.typeStr == "eeg"]
        resample_rate = 100
        model_path = "SleePyPhases/external/sumo/model/final.ckpt"
        
        eegs = []
        for eegSignal in eegSignals:
            eegSignal = downsample(butter_bandpass_filter(eegSignal.signal, 0.3, 30.0, eegSignal.frequency, 10), eegSignal.frequency, resample_rate)
            eegs.append(eegSignal)

        dataset = SimpleDataset(eegs)
        dataloader = DataLoader(dataset)
        model = get_model(model_path)
        trainer = pl.Trainer(num_sanity_val_steps=0, logger=False)
        predictions = trainer.predict(model, dataloader)

        for x, pred in zip(eegs, predictions):
            # spindles_a7 = A7(x, resample_rate)
            spindle_vect = pred[0].numpy()
            
            diff = np.diff(np.r_[0, spindle_vect, 0])  # be able to detect spindles at the start and end of vector
            spindles = np.c_[np.argwhere(diff == 1), np.argwhere(diff == -1)]  / resample_rate
            # spindles = spindle_vect_to_indices(spindle_vect) / resample_rate

        
        return [Event("spindle-slow", 500, 10)]