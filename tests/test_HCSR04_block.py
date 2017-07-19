from unittest.mock import patch, MagicMock, ANY
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
import sys
sys.modules["RPi"] = MagicMock()
sys.modules["RPi.GPIO"] = MagicMock()
from HCSR04_block import HCSR04


class TestHCSR04(NIOBlockTestCase):
    trig_gpio = 1
    echo_gpio = 2
    def test_process_signals(self):
        """Signals pass through block unmodified."""
        with patch(HCSR04.__module__ + '.GPIO') as mock_gpio:
            # input() must return these values so that while loops execute
            mock_gpio.input.side_effect = [0, 1, 1, 2]
            blk = HCSR04()
            self.configure_block(blk, {"trig" : self.trig_gpio,
                                       "echo" : self.echo_gpio})
            self.assertEqual(mock_gpio.setmode.call_count, 1)
            self.assertEqual(mock_gpio.setup.call_count, 2)
            self.assertTrue((self.trig_gpio, mock_gpio.OUT) in \
                            [a[0] for a in mock_gpio.setup.call_args_list])
            self.assertTrue((self.echo_gpio, mock_gpio.IN) in \
                            [a[0] for a in mock_gpio.setup.call_args_list])
            blk.start()
            blk.process_signals([Signal({"hello": "n.io"})])
            blk.stop()
            self.assertEqual(mock_gpio.cleanup.call_count,1)
            self.assert_num_signals_notified(1)
            self.assertDictEqual(
                {"distance": ANY},
                self.last_notified[DEFAULT_TERMINAL][0].to_dict())
