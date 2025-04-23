import os
import functools as ft
import time
import traceback
from typing import Optional, List, Union
from collections import defaultdict

import mido
from mido.frozen import freeze_message

from .state import _lock

def _alias(item):
    if item=='cc':
        return 'control_change'
    if item=='pc':
        return 'program_change'
    return item
def _get_filter(item):
    if item is None:
        return item
    if (not isinstance(item, str)) and hasattr(item, '__iter__'):
        return set(_alias(i) for i in item)
    return {_alias(item)}

class MIDI:
    """
    iipyper MIDI object.
    Create one of these and use it to make MIDI handlers and send MIDI:

    ```python
    midi = MIDI()

    @midi.handle
    def my_handler(msg):
        print(msg)

    midi.note_on(channel=0, note=0, velocity=64, time=0)
    ```
    """
    @classmethod
    def print_ports(cls):
        print('Available MIDI inputs:')
        for s in set(mido.get_input_names()):
            print(f'\t{s}') 
        print('Available MIDI outputs:')
        for s in set(mido.get_output_names()):
            print(f'\t{s}')
        MIDI.ports_printed = True

    ports_printed = False

    def __init__(self, 
        in_ports:Optional[List[str]]=None, 
        out_ports:Optional[List[str]]=None, 
        virtual_in_ports:int=1, virtual_out_ports:int=1, 
        suppress_feedback:bool=True,
        suppress_feedback_window:float=1e-3,
        # sleep_time:float=5e-4
        verbose:int=1, 
        ):
        """
        Args:
            in_ports: list of input devices to open (uses all by default)
            out_ports: list of output devices to open (uses none by default)
            virtual_in_ports: number of 'To iipyper X' ports to create
            virtual_out_ports: number of 'From iipyper X' ports to create
            suppress_feedback: if True, ignore any MIDI message recently sent on an output port 
            suppress_feedback_window: max delay in seconds to consider feedback
        """
        if not MIDI.ports_printed and verbose:
            MIDI.print_ports()

        self.running = False

        self.verbose = int(verbose)
        # self.sleep_time = sleep_time
        # type -> list[Optional[set[port], Optional[set[channel]], function]
        self.handlers = []

        self.handler_docs = []

        if isinstance(in_ports, str):
            in_ports = in_ports.split(',')
        if isinstance(out_ports, str):
            out_ports = out_ports.split(',')

        # TODO: fuzzy match port names

        if in_ports is None or len(in_ports)==0:
            in_ports = set(mido.get_input_names())

        # MIDI feedback suppression stuff
        self.suppress_feedback = suppress_feedback
        # map from MIDI event to list of timestamps
        self.recent_outputs = defaultdict(list)
        self.max_feedback_ns = suppress_feedback_window * 1e9

        self.in_ports = {}  
        for port in in_ports:
            cb = self.get_callback(port)
            try:
                self.in_ports[port] = mido.open_input(port, callback=cb)
            except Exception:
                print(f"""WARNING: failed to open MIDI input {port}""")
        for i in range(virtual_in_ports):
            port = f'To iipyper {i+1}'
            cb = self.get_callback(port)
            try:
                self.in_ports[port] = mido.open_input(
                    port, virtual=True, callback=cb)
            except Exception: print(
                f'WARNING: iipyper: failed to open virtual MIDI port {port}')

        if self.verbose:
            print(f"""opened MIDI input ports: {list(self.in_ports)}""")

        self.out_ports = {}
        for i in range(virtual_out_ports):
            port = f'From iipyper {i+1}'
            try:
                self.out_ports[port] = mido.open_output(port, virtual=True)
            except Exception: print(
                f'WARNING: iipyper: failed to open virtual MIDI port {port}')

        if out_ports is None:
            out_ports = []
        for port in out_ports:
            try:
                self.out_ports[port] = mido.open_output(port)
            except Exception:
                print(f"""WARNING: MIDI output {port} not found""")

        if self.verbose:
            print(f"""opened MIDI output ports: {list(self.out_ports)}""")

        self.start()

    def start(self):
        self.running = True

    def handle(self, *a, **kw):
        """MIDI handler decorator.
        
        Decorated function receives the following arguments:
            `msg`: a [mido](https://mido.readthedocs.io/en/stable/messages/index.html) message
            `port`: MIDI port name as a string (optional)

        Args:
            port: (collection of) MIDI ports to filter on (whitelist)
            ignore_port: (collection of) MIDI ports to filter on (blacklist)
            channel: (collection of) MIDI channels (0-index) to filter on
            type: (collection of) MIDI event types to filter on
            note: (collection of) MIDI note numbers to filter on
            velocity: (collection of) MIDI velocities numbers to filter on
            value: (collection of) MIDI values to filter on
            control: (collection of) MIDI cc numbers to filter on
            program: (collection of) MIDI program numbers to filter on
        """
        if len(a):
            # bare decorator
            assert len(a)==1
            assert len(kw)==0
            assert hasattr(a[0], '__call__')
            f = a[0]
            filters = {}
        else:
            # with filter arguments
            for k in kw:
                assert k in {
                    'channel', 'port', 'type', 
                    'note', 'velocity', 'value', 
                    'control', 'program', 'ignore_port'
                    }, f'unknown MIDI message filter "{k}"'
            filters = {k:_get_filter(v) for k,v in kw.items()}
            f = None

        def decorator(f):
            self.handler_docs.append((kw, f.__doc__))

            self.handlers.append((filters, f))
            return f
        
        return decorator if f is None else decorator(f)
    
    def get_docs(self):
        s = ''
        for filters,doc in self.handler_docs:
            s += str(filters)
            if doc is not None: 
                s += doc
            s += '\n'
        return s

    def get_callback(self, port_name):
        if self.verbose>1: print(f'handler for MIDI port {port_name}')
        def callback(msg):

            # check recent outputs.
            # if any are older than threshold, drop them
            # if one is younger, drop it, break the search and ignore the input
            if self.suppress_feedback:
                m = freeze_message(msg)
                t = time.time_ns()
                ts = self.recent_outputs[m]
                while len(ts):
                    age = t - ts.pop()
                    if age<self.max_feedback_ns:
                        if self.verbose > 2:
                            print(f'suppressing MIDI feedback {msg} port={port_name}')
                        return
                    
            if self.verbose > 1:
                print(f'filtering MIDI {msg} port={port_name}')
            if not self.running:
                return
            # check each handler 
            for filters, f in self.handlers:
                filters = {**filters}
                # print(port_name, f'{filters=}')
                # check port
                use_handler = (
                    'port' not in filters 
                    or port_name in filters.pop('port'))
                # print(f"{ 'ignore_port' not in filters=}")
                # print(f"{ port_name not in filters.pop('ignore_port')=}")
                use_handler &= (
                    'ignore_port' not in filters 
                    or port_name not in filters.pop('ignore_port'))
                # check other filters
                use_handler &= all(
                    filt is None 
                    or not hasattr(msg, k)
                    or getattr(msg, k) in filt
                    for k,filt in filters.items())
                # call the handler if it passes the filter
                if not use_handler:
                    continue
                with _lock:
                    if self.verbose>1: print(f'enter handler function {f}')
                    try:
                        f(msg, port_name)
                    except TypeError:
                        f(msg)
                    except Exception as e:
                        print(f'error in MIDI handler {f}:')
                        traceback.print_exc()
                    if self.verbose>1: print(f'exit handler function {f}')

        return callback

    def _send_msg(self, port, m):
        """send on a specific port or all output ports"""
        ports = self.out_ports.values() if port is None else [self.out_ports[port]]
        # print(ports)
        t = time.time_ns()
        m = freeze_message(m)
        for p in ports:
            # print('iipyper send', m)
            # iiuc mido send should already be thread safe
            # with _lock:
            p.send(m)
            self.recent_outputs[m].append(t)


    # # see https://mido.readthedocs.io/en/latest/message_types.html

    def send(self, m:Union[str,mido.Message], *a, port:Optional[str]=None, **kw):
        """
        send a mido message as MIDI. 
        
        These are equivalent:

        ```python
        midi.send(mido.Message('note_on', channel=0, note=0, velocity=64, time=0))
        midi.send('note_on', channel=0, note=0, velocity=64, time=0)
        midi.note_on(channel=0, note=0, velocity=64, time=0)
        ```

        Args:
            m: a [mido](https://mido.readthedocs.io/en/stable/messages/index.html) message or message type
            port: the MIDI port to send on 
                (or sends on all open ports if not specified)
        """
        # print(f'SEND {time.perf_counter()}')
        if isinstance(m, mido.Message):
            self._send_msg(port, m)
            # mido crashes if channel is a np.int8
            m.channel = int(m.channel)
            if len(a)+len(kw) > 0:
                print('warning: extra arguments to MIDI send')
        elif isinstance(m, str):
            try:
                m = mido.Message(m, *a, **kw)
                # mido crashes if channel is a np.int8
                m.channel = int(m.channel)
                self._send_msg(port, m)
            except Exception:
                print('MIDI send failed: bad arguments to mido.Message')
                raise
        else:
            print('MIDI send failed: first argument should be a mido.Message or str')

    def __getattr__(self, name):
        if name=='cc': name = 'control_change'
        if name=='pc': name = 'program_change'
        if name in (
            'note_on', 'note_off', 'polytouch', 'control_change', 
            'program_change', 'aftertouch', 'pitchwheel', 'sysex'):
            return lambda *a, **kw: self.send(name, *a, **kw)
        raise AttributeError
        

