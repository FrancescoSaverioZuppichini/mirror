import unittest
from mirror.visualisations.core import Visualisation
from mirror.visualisations.web import WebInterface
from functools import partial


class ModuleTracerTest(unittest.TestCase):
    def test(self):
        class TestVisualisation(Visualisation):

            def __call__(self, inputs, layer, something=1, *args, **kwargs):
                self.something = something
                return None

        params = {'something': {
            'type': 'slider',
            'min': 1,
            'max': 100,
            'value': 1,
            'step': 1,
            'params': {}
        }
        }

        TestVisWeb = partial(WebInterface.from_visualisation, TestVisualisation,
                                       params=params,
                                       name='something')
        test_vis_web = TestVisWeb(None, None)

        test_vis_web(None, None)

        self.assertEqual(test_vis_web.callable.something,  1)

        state = test_vis_web.to_JSON()
        state['params']['something']['value'] = 4 #simulate change in the front end

        test_vis_web.from_JSON(state)

        self.assertEqual(test_vis_web.callable.something,  1)


