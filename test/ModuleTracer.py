import unittest
import torch
import torch.nn as nn
from mirror.ModuleTracer import *
import pprint
from dataclasses import dataclass
from mirror.visualisations.interfaces import *
from mirror.visualisations.buttons import *

class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()

        self.linear = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=1),
            nn.BatchNorm2d(32)
        )

        self.conv = nn.Sequential(nn.Conv2d(3, 32, kernel_size=3),
                                  nn.ReLU())

    def forward(self, x):
        x = self.conv(x)
        x = self.linear(x)
        return x
#
from mirror.visualisations.WebInterface import Visualisation


class TestVisualisation(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_repeat = 1

    def __call__(self, inputs, layer):
        return inputs.repeat(self.n_repeat, 1, 1, 1), None

    @property
    def name(self):
        return 'dummy'

    @property
    def params(self):
        return { 'n_repeat' : {
            'type': 'slider',
            'min': 1,
            'max': 100,
            'asd': self.n_repeat,
            'step': 1,
            'params': {}
         }
        }


class ModuleTracerTest(unittest.TestCase):
    # def test(self):
    #     module = MyModule()
    #     tracer = ModuleTracer(module)
    #     x = torch.ones((1,3,28,28))
    #     tracer(x)
    #     # tracer_dict = tracer.__dict__()
    #     pprint.pprint(tracer.to_JSON())
    #
    #     tracer = Tracer(module)
    #     tracer(x)
    #     pprint.pprint(tracer.serialized)
    #
    #
    def test(self):
        # module = MyModule()
        # print('weee')
        # vis = WebVisualization(Weights(module, 'cuda'), {}, 'weights')
        # x = torch.ones((1, 3, 28, 28))
        #
        # print(vis(x, module))
        vis = TestVisualisation(None, None)
        print(vis.to_JSON())
        vis.update_params({ 'n_repeat': {'value' : 5}})
        print(vis.to_JSON())
        vis.n_repeat = 10
