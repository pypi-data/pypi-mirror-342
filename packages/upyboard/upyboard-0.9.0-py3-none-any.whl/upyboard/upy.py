import os 
import sys
import time
import re
import platform
import threading
import posixpath
import ast
import textwrap
import binascii
import shutil
import stat
import subprocess
import json
import urllib.request
import pathlib
import packaging

import click
import dotenv

import serial
from serial.tools import list_ports
from genlib.ansiec import ANSIEC
 

from . import __version__  

#--------------------------------------------------------------

buffer = b''
expected_bytes = 0

def stdout_write_bytes(b):
    global buffer, expected_bytes
    
    if b == b'\x04' or b == b'':
        return

    if expected_bytes > 0: 
        buffer += b
        expected_bytes -= 1

        if expected_bytes == 0: 
            try:
                sys.stdout.buffer.write(buffer)
                sys.stdout.buffer.flush()
            except UnicodeDecodeError:
                sys.stdout.buffer.write(buffer.hex())
            finally:
                buffer = b'' 
    elif ord(b) <= 0x7F:                # ASCII
        sys.stdout.buffer.write(b)
        sys.stdout.buffer.flush()
    else:                               # Multi-byte
        if (ord(b) & 0xF0) == 0xF0:     # 4 byte
            expected_bytes = 3
        elif (ord(b) & 0xE0) == 0xE0:   # 3 byte
            expected_bytes = 2
        elif (ord(b) & 0xC0) == 0xC0:   # 2 byte
            expected_bytes = 1
        else:
            sys.stdout.buffer.write(buffer.hex())
            return 

        buffer = b                      # save first byte  
    
#--------------------------------------------------------------

class Getch:
    def __init__(self):
        if platform.system() == "Windows":
            import msvcrt
            self.impl = msvcrt.getch
        else:
            import sys, tty, termios
            self.sys = sys
            self.tty = tty
            self.termios = termios

    def __call__(self):
        if platform.system() == "Windows":
            return self.impl()
        else:
            fd = self.sys.stdin.fileno()
            old_settings = self.termios.tcgetattr(fd)
            try:
                self.tty.setraw(fd)
                ch = self.sys.stdin.read(1)
                return ch.encode()
            finally:
                self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)

class UpyBoard:
    BUFFER_SIZE = 128

    def __init__(self, port, baudrate=115200, wait=0):                         
        delayed = False
        for attempt in range(wait + 1):
            try:
                self.serial = serial.Serial(port, baudrate, timeout=1)
                break
            except (OSError, IOError): 
                if wait == 0:
                    continue
                if attempt == 0:
                    sys.stdout.write(f"Waiting {wait} seconds for device to connect")
                    delayed = True
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        else:
            if delayed:
                print('')
            raise BaseException(f"failed to access {port}")
        if delayed:
            print('')
        
        self.__init_repl()

    def __init_repl(self):
        self.serial_reader_running = None
        self.serial_out_put_enable = True
        self.serial_out_put_count = 0

    def close(self):
        self.serial.close()

    def read_until(self, min_num_bytes, ending, timeout=10, data_consumer=None):
        assert data_consumer is None or len(ending) == 1
        
        data = self.serial.read(min_num_bytes)
        
        if data_consumer:
            data_consumer(data)
        timeout_count = 0
        
        while True:
            if data.endswith(ending):
                break
            elif self.serial.in_waiting > 0:
                new_data = self.serial.read(1)
                if data_consumer:
                    data_consumer(new_data)
                    data = new_data
                else:                
                    data = data + new_data
                timeout_count = 0
            else:
                timeout_count += 1
                if timeout is not None and timeout_count >= 100 * timeout:
                    break
                time.sleep(0.01)
        return data

    def enter_raw_repl(self, soft_reset=True):
        self.serial.write(b'\r\x03') # ctrl-C: interrupt any running program
        time.sleep(0.1)
        
        n = self.serial.in_waiting
        while n > 0:
            self.serial.read(n)
            n = self.serial.in_waiting

        self.serial.write(b'\r\x01') # ctrl-A: enter raw REPL
        
        if soft_reset:
            data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n>')
            if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
                print(data)
                raise BaseException('could not enter raw repl')

            self.serial.write(b'\x04') # ctrl-D: soft reset
            
            data = self.read_until(1, b'soft reboot\r\n')
            if not data.endswith(b'soft reboot\r\n'):
                print(data)
                raise BaseException('could not enter raw repl')

        data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n'):
            print(data)
            raise BaseException('could not enter raw repl')
            
    def exit_raw_repl(self):
        self.serial.write(b'\r\x02') # ctrl-B: enter friendly REPL
        
    def _follow_write(self, echo):        
        try:
            import msvcrt
            def getkey():
                return msvcrt.getch()

            def putkey(ch):
                if ch == b'\r':
                    ch = b'\n'
                msvcrt.putch(ch)
        except ImportError:
            import sys, tty, termios
            def getkey():
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                return ch
            
            def putkey(ch):
                sys.stdout.write(ch)
                sys.stdout.flush()
        
        while True:
            ch = getkey()
            
            if ch == b'\x03': # Ctrl + C
                self.reset()
                os._exit(0)
            if echo:
                putkey(ch)
            self.serial.write(ch)

    def follow(self, timeout, data_consumer=None, input_stat=None):
        if input_stat[1]:
            threading.Thread(target=self._follow_write, args=(input_stat[0],), daemon=True).start()
        
        data = self.read_until(1, b'\x04', timeout=timeout, data_consumer=data_consumer)
     
        if not data.endswith(b'\x04'):
            raise BaseException('timeout waiting for first EOF reception')
        data = data[:-1]

        data_err = self.read_until(1, b'\x04', timeout=timeout)
        if not data_err.endswith(b'\x04'):
            raise BaseException('timeout waiting for second EOF reception')
        data_err = data_err[:-1]
        
        return data, data_err

    def exec_raw_no_follow(self, command):            
        if isinstance(command, bytes):
            command_bytes = command
        else:
            command_bytes = bytes(command, encoding='utf8')
        
        data = self.read_until(1, b'>')
        if not data.endswith(b'>'):
            raise BaseException('could not enter raw repl')
        
        for i in range(0, len(command_bytes), 256):
            self.serial.write(command_bytes[i:min(i + 256, len(command_bytes))])
            time.sleep(0.01)
        self.serial.write(b'\x04')
        
        data = self.read_until(1, b'OK')
        if not data.endswith(b'OK'):
            raise BaseException('could not exec commandm (response: %r)' % data)

    def exec_raw(self, command, timeout=None, data_consumer=None, input_stat=None):
        self.exec_raw_no_follow(command)
        return self.follow(timeout, data_consumer, input_stat)

    def exec(self, command, stream_output=False, echo_on=False):
        data_consumer = None
        if stream_output or echo_on:
            data_consumer = stdout_write_bytes
        ret, ret_err = self.exec_raw(command, data_consumer=data_consumer, input_stat=(stream_output, echo_on))
        if ret_err:
            raise BaseException(ret_err.decode('utf-8'))
        return ret
    
    def execfile(self, filename, stream_output=False, echo_on=False):
        with open(filename, 'r+b') as f:
            command = f.read()
        return self.exec(command, stream_output, echo_on)
         
    def _exec_command(self, command):
        self.enter_raw_repl()
        try:
            out = self.exec(textwrap.dedent(command))
        except BaseException as ex:
            raise ex
        self.exit_raw_repl()
        return out

    def run(self, filename, stream_output=False, echo_on=False):
        self.enter_raw_repl()

        if not stream_output and not echo_on:           # -n (no waiting)
            with open(filename, "rb") as infile:        # Running without io stream
                self.exec_raw_no_follow(infile.read())           
        elif stream_output and echo_on:                 # -i (echo on)
            self.execfile(filename, True, True)                         
        else:                                           # default (waiting and echo off)
            self.execfile(filename, False, True)            

        self.exit_raw_repl()

    def __repl_serial_to_stdout(self):        
        def hexsend(string_data=''):
            import binascii
            hex_data = binascii.unhexlify(string_data)
            return hex_data

        try:
            data = b''
            try:
                while self.serial_reader_running:
                    count = self.serial.in_waiting
                    if count == 0:
                        time.sleep(0.01)
                        continue

                    if count > 0:
                        data += self.serial.read(count)

                        if len(data) < 20:
                            try:
                                data.decode()
                            except UnicodeDecodeError:
                                continue

                        if data != b'':
                            if self.serial_out_put_enable and self.serial_out_put_count > 0:
                                if platform.system() == 'Windows':   
                                    sys.stdout.buffer.write(data.replace(b"\r", b""))
                                else:
                                    sys.stdout.buffer.write(data)
                                    
                                sys.stdout.buffer.flush()
                        else:
                            self.serial.write(hexsend(data))

                        data = b''
                        self.serial_out_put_count += 1
            except:
                print('')
                return
        except KeyboardInterrupt:
            if serial != None:
                serial.close()
    
    def reset(self):
        command = f"""
            import machine
            machine.soft_reset()
        """
        self._exec_command(command)
    
    def repl(self):
        self.serial_reader_running = True
        self.serial_out_put_enable = True
        self.serial_out_put_count = 1

        self.reset()
        self.read_until(1, b'\x3E\x3E\x3E', timeout=1) # read prompt >>>

        repl_thread = threading.Thread(target=self.__repl_serial_to_stdout, daemon=True, name='REPL')
        repl_thread.start()

        getch = Getch()
        self.serial.write(b'\r') # Update prompt
        
        while True:
            char = getch()

            if char == b'\x07':
                self.serial_out_put_enable = False
                continue

            if char == b'\x0F':
                self.serial_out_put_enable = True
                self.serial_out_put_count = 0
                continue

            if char == b'\x00' or not char:
                continue

            if char == b'\x03':   # Ctrl + X to exit repl mode
                self.serial_reader_running = False
                #self.serial.write(b' ')
                #time.sleep(0.1)
                self.reset()
                print('')
                break
            
            try:
                self.serial.write(b'\r' if char == b'\n' else char)
            except:
                print('')
                break
           
    def fs_get(self, filename):
        command = f"""
            import sys
            import ubinascii
            sys.stdout.buffer.write(b'<<<START>>>')
            with open('{filename}', 'rb') as infile:
                while True:
                    result = infile.read({self.BUFFER_SIZE})
                    if not result:
                        break
                    sys.stdout.buffer.write(ubinascii.hexlify(result))
            sys.stdout.buffer.write(b'<<<END>>>')
        """
        out = self._exec_command(command)
        hexdata = out.split(b'<<<START>>>')[1].split(b'<<<END>>>')[0]
        return binascii.unhexlify(hexdata)

    def fs_state(self, path:str) -> int:
        """
        Return file size of given path.
        """
        command = f"""
            import os
            try:
                st = os.stat('{path}')
                print(st[6])
            except:
                print(0)
        """
        out = self._exec_command(command)
        return int(out.decode('utf-8'))
    
    def fs_ls(self, dir="/"):
        if not dir.startswith("/"):
            dir = "/" + dir
        #if dir.endswith("/"):
        #    dir = dir[:-1]
            
        command = f"""
            import os
            def listdir(dir):
                if dir == '/':                
                    return sorted([dir + f for f in os.listdir(dir)])
                else:
                    return sorted([dir + '/' + f for f in os.listdir(dir)])
            print(listdir('{dir}'))
        """
        out = self._exec_command(command)
        return ast.literal_eval(out.decode("utf-8"))
            
    def fs_is_dir(self, path):
        command = f"""
            vstat = None
            try:
                from os import stat
            except ImportError:
                from os import listdir
                vstat = listdir
            def ls_dir(path):
                if vstat is None:
                    return stat(path)[0] & 0x4000 != 0
                else:
                    try:
                        vstat(path)
                        return True
                    except OSError as e:
                        return False
            print(ls_dir('{path}'))
        """
        out = self._exec_command(command)
        return ast.literal_eval(out.decode("utf-8"))

    def fs_mkdir(self, dir):       
        command = f"""
            import os
            def mkdir(dir):
                parts = dir.split(os.sep)
                dirs = [os.sep.join(parts[:i+1]) for i in range(len(parts))]
                check = 0
                for d in dirs:
                    try:
                        os.mkdir(d)
                    except OSError as e:
                        check += 1
                        if "EEXIST" in str(e):
                            continue
                        else:
                            return False
                return check < len(parts)
            print(mkdir('{dir}'))
        """        
        out = self._exec_command(command)
        return ast.literal_eval(out.decode("utf-8"))

    def fs_putdir(self, local, remote, callback=None):        
        for parent, child_dirs, child_files in os.walk(local, followlinks=True):
            remote_parent = posixpath.normpath(posixpath.join(remote, os.path.relpath(parent, local)))
           
            try:
                self.fs_mkdir(remote_parent)
            except:
                pass
        
            for filename in child_files:
                with open(os.path.join(parent, filename), "rb") as infile:
                    remote_filename = posixpath.join(remote_parent, filename)
                    data = infile.read()

                    total_size = os.path.getsize(os.path.join(parent, filename))                 
                    if callback:
                        th = threading.Thread(target=callback, args=(remote_filename, total_size), daemon=True)
                        th.start()
                        
                    self.fs_put(data, remote_filename)
                    
                    if callback:
                        th.join() 

    def fs_put(self, local_data, remote, callback=None):
        self.enter_raw_repl()
        try:
            self.exec(f"f = open('{remote}', 'wb')")
        except BaseException as e:
            if "EEXIST" in str(e):
                self.exit_raw_repl()
                self.fs_rm(remote)
                self.fs_put(local_data, remote, callback)
            return
    
        size = len(local_data)

        if callback:
            th = threading.Thread(target=callback, args=(remote, size), daemon=True)
            th.start()
               
        for i in range(0, size, self.BUFFER_SIZE):
            chunk_size = min(self.BUFFER_SIZE, size - i)
            chunk = repr(local_data[i : i + chunk_size])
            if not chunk.startswith("b"):
                chunk = "b" + chunk
            self.exec(f"f.write({chunk})")
        
        self.exec("f.close()")
        self.exit_raw_repl()
        
        if callback:
            th.join() 

    def fs_rm(self, filename):
        command = f"""
            import os
            os.remove('{filename}')
        """
        self._exec_command(command)

    def fs_rmdir(self, dir):
        command = f"""
            import os
            def rmdir(dir):
                os.chdir(dir)
                for f in os.listdir():
                    try:
                        os.remove(f)
                    except OSError:
                        pass
                for f in os.listdir():
                    rmdir(f)
                os.chdir('..')
                os.rmdir(dir)
            rmdir('{dir}')
        """
        self._exec_command(command)

    def fs_format(self, type):
        ret = True
        
        if type == "esp32":
            command = """ 
                import os
                os.fsformat('/flash')
            """
        elif type == "efr32mg":
            command = """
                import os
                os.format()
            """
        elif type == "rp2350":
            command = """
                import os
                import rp2
                bdev = rp2.Flash()
                os.VfsFat.mkfs(bdev)
            """
        else:
            ret = False
        try:
            self._exec_command(command)
        except BaseException:
            ret = False
            
        return ret
    
    def fs_df(self):
        command = f"""
            import os
            import json
            def get_fs_info(path='/'):
                stats = os.statvfs(path)
                block_size = stats[0]
                total_blocks = stats[2]
                free_blocks = stats[3]

                total = block_size * total_blocks
                free = block_size * free_blocks
                used = total - free
                usage_pct = round(used / total * 100, 2)
                
                return total, used, free, usage_pct
            print(get_fs_info())
        """
        out = self._exec_command(command)
        return ast.literal_eval(out.decode("utf-8"))
#--------------------------------------------------------------

config = dotenv.find_dotenv(filename=".vscode/.upyboard", usecwd=True)
if config:
    dotenv.load_dotenv(dotenv_path=config)

class ColorfulGroup(click.Group):
    def format_commands(self, ctx, formatter):
        commands = self.list_commands(ctx)
        rows = []
        for cmd_name in commands:
            cmd = self.get_command(ctx, cmd_name)
            if cmd is None or cmd.hidden:
                continue
            help_text = cmd.get_short_help_str()
            cmd_display = click.style(cmd_name, fg='green', bold=True)
            rows.append((cmd_display, help_text))
        if rows:
            with formatter.section('Commands'):
                formatter.write_dl(rows)

def get_micropython_board_info(port:str, is_long:bool=False) -> tuple | str | None:
    """
    Get the firmware version, build date, core name, and device name of the connected device.
       
    :param port: The port name of the connected device.
    :param is_long: If True, display detailed information about the connected device.
    
    :return: The (version, date, core, device) or sring of the connected device.
    """           
    
    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            ser.write(b'\r\x03') 
            time.sleep(0.1)
            ser.reset_input_buffer()

            ser.write(b'\r\x02')
            time.sleep(0.1)

            response = ser.read_all().decode(errors='ignore').strip()
            if response:
                pattern = re.compile(r"(?:MicroPython|Pycom MicroPython)\s+(.*)")
                match = pattern.search(response)
                if match:
                    response = match.group(1)

                if is_long:
                    return response
                else:
                    pattern = re.compile(
                        r"(?P<full_version>[^\s\[]+)"
                        r"(?:\s*\[[^\]]+\])?"
                        r"\s+on\s+(?P<date>\d{4}-\d{2}-\d{2});\s+"
                        r"(?P<manufacturer>.+?)\s+with\s+(?P<core>\S+)"
                    )
                    match = pattern.search(response)
                    if match:
                        full_version = match.group("full_version").lstrip("v")
                        version_match = re.match(r"(\d+\.\d+)", full_version)
                        date = match.group("date")
                        version = version_match.group(1) if version_match else "?"
                        manufacturer = match.group("manufacturer").strip().lower()
                        core = match.group("core").strip().lower()

                        device_list = SUPPORT_DEVICE_TYPES.get(core.strip().lower(), None)                                        
                        if device_list:
                            if core == 'rp2350':
                                manufacturer = manufacturer.split()[-1][:-1]
                            
                            device = device_list.get(manufacturer, None)
                            if not device:
                                device = core
                        else:
                            device = core
     
                        return (version, date, core, device)
    except (OSError, serial.SerialException):
        pass
    
    return None

SUPPORT_DEVICE_TYPES = {'efr32mg':{'xbee3 zigbee':'xnode'}, 'esp32':{'lopy4':'smartfarm1'}, 'rp2350':{'pico2w0':'autocon', 'pico2w1':'xhome', 'pico2w2':'xconvey'}}

_upy = None
_version = 0.0
_core = ""
_device = ""
_device_root_fs = "/"
_core_path = ""
_device_path = ""

@click.group(cls=ColorfulGroup, invoke_without_command=True)
@click.option(
    "--sport",
    "-s",
    envvar="SERIAL_PORT",
    default="",
    type=click.STRING,
    help="Serial port name for connected device.",
    metavar="SPORT",
)
@click.option(
    "--baud",
    '-b',
    envvar="SERIAL_BAUD",
    default=115200,
    type=click.INT,
    help="Baud rate for the serial connection (default 115200).",
    metavar="BAUD",
)
@click.option(
    "--command",
    '-c',
    default="",
    type=click.STRING,
    help=" Command to execute on the connected device.",
)   
@click.version_option(__version__, "-v", "--version", message="upyboard %(version)s")
@click.pass_context
def cli(ctx, sport, baud, command):
    import upyboard
    global _upy, _version, _core, _device, _device_root_fs, _core_path, _device_path

    if ctx.invoked_subcommand == "scan":
            return
        
    descript =  get_micropython_board_info(sport)
    if not descript:
        if sport:
            print("There is no device connected to the" + ANSIEC.FG.BRIGHT_RED + f" {sport}." + ANSIEC.OP.RESET)
        else:
            print("The serial port name is missing.")
        raise click.Abort()

    _version, _, _core, _device = descript
    _version = float(_version)
    
    if not _core in (SUPPORT_DEVICE_TYPES.keys()):
        print("The" + ANSIEC.FG.BRIGHT_RED + f" {_device}" + ANSIEC.OP.RESET + " is not supported.")
        raise click.Abort()
    
    if _device in ('xnode', 'smartfarm1'):
        _device_root_fs = "/flash/"
     
    _core_path = os.path.join(os.path.dirname(upyboard.__file__), os.path.join("core", _core))
    if _core != _device:
        _device_path = os.path.join(os.path.dirname(upyboard.__file__), os.path.join("device", _device))  

    try:
        _upy = UpyBoard(sport, baud)
    except BaseException:
        print("Device is not connected to " + ANSIEC.FG.BRIGHT_RED + f"{sport}" + ANSIEC.OP.RESET)
        print("Please check the port with the scan command and try again.")
        raise click.Abort()

    if ctx.invoked_subcommand is None and command:
        _upy.enter_raw_repl()
        ret = _upy.exec(command)
        click.echo(ret.decode('utf-8', errors='replace'))
        _upy.exit_raw_repl()
        _upy.close()
        

@cli.command()
@click.argument("remote")
@click.argument("local", required=False)
def get(remote, local):
    """
    Download a file from the connected device to the local machine.
    
    :param remote: The remote file to download.\n
    :param local: The local file or directory to save the downloaded content. If not provided, print to stdout.
    """
    
    if not remote.startswith(_device_root_fs):
        remote = posixpath.join(_device_root_fs, remote)
    
    try:
        contents = _upy.fs_get(remote)
    
        if local is None:
            try:
                print(contents.decode("utf-8"))
            except:
                print(f"{contents}")
        else:
            if os.path.isdir(local):
                local = os.path.join(local, os.path.basename(remote))
            open(local, "wb").write(contents)
    except BaseException:
        remote = remote.replace(_device_root_fs, "", 1)
        print(f"The {ANSIEC.FG.BRIGHT_RED} {remote}{ANSIEC.OP.RESET} does not exist or is not a file.")
                
@cli.command()
@click.argument("path")
def mkdir(path):
    """
    Create a directory on the connected device.
    
    :param path: The path to create.
    """
    path_ = path
    if not path_.startswith(_device_root_fs):
        path_ = _device_root_fs + path
        
    if _upy.fs_mkdir(path_):
        print(f"{ANSIEC.FG.BRIGHT_BLUE}{path}{ANSIEC.OP.RESET} is {ANSIEC.FG.BRIGHT_GREEN}created.{ANSIEC.OP.RESET}")
    else:
        print(f"{ANSIEC.FG.BRIGHT_BLUE}{path}{ANSIEC.OP.RESET} is {ANSIEC.FG.BRIGHT_RED}already exists.{ANSIEC.OP.RESET}")

@cli.command()
@click.argument("remote")
def rm(remote):
    """
    Remove a file or directory from the connected device.
    
    :param remote: The remote file or directory to remove.
    """
    
    if not remote.startswith(_device_root_fs):
        remote = _device_root_fs + remote
        
    try:
        if _upy.fs_is_dir(remote):
            _upy.fs_rmdir(remote)
        else:
            _upy.fs_rm(remote)
    except BaseException:
        remote = remote.replace(_device_root_fs, "", 1)
        print("The " + ANSIEC.FG.BRIGHT_RED + f"{remote}" + ANSIEC.OP.RESET + " does not exist.")

def _get_icon_and_size(path, filename, is_dir):
    """
    Return icon and size based on directory or file extension.
    """
    if is_dir:
        return "📁", ""

    ext_icons = {
        ".py": "🐍",
        ".mpy": "📦",
        ".txt": "📄",
        ".cvs": "🗃",
    }
    for ext, icon in ext_icons.items():
        if filename.endswith(ext):
            return icon, _upy.fs_state(path)

    return "📎", _upy.fs_state(path)

@cli.command()
@click.argument("path", default="/")
def ls(path):
    """
    List the files and directories in the specified path on the connected device,
    sorted and including file sizes and icons.
    """
    if not path.startswith(_device_root_fs):
        path = _device_root_fs + path

    try:
        items = []
        listing = _upy.fs_ls(path)

        for f in listing:
            f_name = f.split("/")[-1]
            is_dir = _upy.fs_is_dir(f)
            icon, size = _get_icon_and_size(f, f_name, is_dir)
            items.append((is_dir, f_name, size, icon))

        # Directories first, then files, all sorted by name
        items.sort(key=lambda x: (not x[0], x[1].lower()))

        # Calculate column widths
        size_width = max(len(str(i[2])) for i in items) if items else 1
        name_width = max(len(i[1]) for i in items) if items else 1

        for is_dir, f_name, size, icon in items:
            name_str = ANSIEC.FG.BRIGHT_BLUE + f_name + ANSIEC.OP.RESET if is_dir else f_name
            print(f"{str(size).rjust(size_width)}  {icon}  {name_str.ljust(name_width)}")

    except BaseException:
        print("The path " + ANSIEC.FG.BRIGHT_RED + "does not exist." + ANSIEC.OP.RESET)
                
def _show_waiting(remote_filename, total_size):
    copied_size = 0
    bar_length = 40
    
    print(ANSIEC.FG.BRIGHT_BLUE + remote_filename.replace(_device_root_fs, "", 1) + ANSIEC.OP.RESET, flush=True)
    
    if total_size == 0:
        return
    
    while True:
        progress = min(copied_size / total_size, 1.0)            
        block = int(round(bar_length * progress))
        bar = "#" * block + "-" * (bar_length - block)
        print(ANSIEC.OP.left() + f"[{bar}] {int(progress * 100)}%", end="", flush=True)
        if progress >= 1.0:
            break
        time.sleep(0.1)
        if _core == 'efr32mg':
            copied_size += (115200 // 8 // 100) * 0.8
        elif _core == 'esp32':
            copied_size += (115200 // 8 // 100) * 1 # TODO: need to check
        elif _core == 'rp2350':
            copied_size += (115200 // 8 // 100) * 2
                    
    print(flush=True)

@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    """
    Upload a local file or directory to the connected device.
    
    :param local: The local file or directory to upload.\n
    :param remote: The remote path on the device. If not provided, the local file name will be used.
    """
    if remote is None:
        remote = os.path.basename(os.path.abspath(local))
    else:
        if not remote.startswith(_device_root_fs):
            remote = posixpath.join(_device_root_fs, remote)
        
        try:
            if _upy.fs_is_dir(remote):
                remote = remote + "/" + os.path.basename(os.path.abspath(local))
        except BaseException:
            pass
        
    if os.path.isdir(local):
        _upy.fs_putdir(local, remote, _show_waiting)
    else:
        with open(local, "rb") as infile:        
            _upy.fs_put(infile.read(), remote, _show_waiting)

def _run_error_process(out, local_file):
    print(f"{'-' * 20} Traceback {'-' * 20}")

    for l in out[1:-2]:
        print(l.strip())
    
    try:
        err_line_raw = out[-2].strip()
        
        if "<stdin>" in err_line_raw:
            full_path = os.path.abspath(os.path.join(os.getcwd(), local_file))
            err_line = err_line_raw.replace("<stdin>", full_path, 1)
        else:
            match = re.search(r'File "([^"]+)"', err_line_raw)
            if match:
                device_src_path = os.path.join(_device_path, "src")
                full_path =  os.path.join(device_src_path, match.group(1))
                escaped_filename = re.sub(r"([\\\\])", r"\\\1", full_path)
                err_line = re.sub(r'File "([^"]+)"', rf'File "{escaped_filename}"', err_line_raw)
                
        print(f" {err_line}")
        
        err_content = out[-1].strip()

        match = re.search(r"line (\d+)", err_line)
        if match:
            line = int(match.group(1))
            try:
                with open(full_path, "r") as f:
                    lines = f.readlines()
                    print(f"  {lines[line - 1].rstrip()}")
            except:
                pass    

    except IndexError:
       err_content = out[-1].strip()
    

    print(ANSIEC.FG.BRIGHT_MAGENTA + err_content + ANSIEC.OP.RESET)
    
    
@cli.command()
@click.argument("local_file")
@click.option(
    "--no-waiting",
    "-n",
    is_flag=True,
    help="Do not join input/output stream",
)
@click.option(
    "--input-echo",
    "-i",
    is_flag=True,
    help="Turn on echo for input",
)
def run(local_file, no_waiting, input_echo):
    """
    Run the local file on the connected device.
    
    :param local_file: The local file to run.\n
    :param no_waiting: If True, do not wait for input/output stream.\n
    :param input_echo: If True, turn on echo for input.
    """
    
    try:
        _upy.run(local_file, not no_waiting, input_echo)
    except IOError:
        click.echo(f"File not found: {ANSIEC.FG.BRIGHT_RED + local_file + ANSIEC.OP.RESET}", err=True)
    except BaseException as ex:
        _run_error_process(str(ex).strip().split('\n'), local_file)
        
@cli.command()
def repl():
    """
    Enter the REPL (Read-Eval-Print Loop) mode.
    """
    
    print(ANSIEC.FG.MAGENTA + "Entering REPL mode. Press Ctrl + C to exit." + ANSIEC.OP.RESET)

    _upy.repl()


is_stop_formatting_process = None

def _formatting_process():
    while not is_stop_formatting_process:
        print(ANSIEC.FG.BRIGHT_BLUE + "." + ANSIEC.OP.RESET, end="", flush=True)
        time.sleep(0.1)

@cli.command()
def format():
    """
    Format the file system of the connected device.
    """
    
    global is_stop_formatting_process

    print("Formatting the file system of " + ANSIEC.FG.BRIGHT_YELLOW + f"{_device}" + ANSIEC.OP.RESET)
    
    is_stop_formatting_process = False
    th = threading.Thread(target=_formatting_process, daemon=True)
    th.start()
    ret = _upy.fs_format(_core)
    is_stop_formatting_process = True
    th.join()
        
    if ret:
        print(ANSIEC.OP.left() + ANSIEC.OP.CLEAR_LINE + "The file system has been " + ANSIEC.FG.BRIGHT_BLUE + "formatted" + ANSIEC.OP.RESET)
    else:
        print(ANSIEC.OP.left() + "The device type is " + ANSIEC.FG.BRIGHT_RED + "not supported." + ANSIEC.OP.RESET)
    return ret

@cli.command()
def df():
    """
    Show the file system information of the connected device.
    """
    
    ret = _upy.fs_df()
    if ret:
        out_str = f"""Total: {ret[0]//1024:5} KByte ({ret[0]:5})
Used: {ret[1]//1024:6} KByte ({ret[1]:7})
Free: {ret[2]//1024:6} KByte ({ret[2]:6})
Usage: {round(ret[3],2):5} %""" 
        
        print(out_str)

@cli.command()
def shell():
    """
    Enter an interactive shell for device control.
    """
    import shlex

    current_path = _device_root_fs

    def print_prompt():
        print(f"\n📟 {_device}:{current_path} >", end=" ", flush=True)

    def run_cmd(cmdline):
        nonlocal current_path
        try:
            args = shlex.split(cmdline)
            if not args:
                return
            cmd = args[0]
            
            if cmd == "ls":
                click.Context(ls).invoke(ls, path=current_path)

            elif cmd == "cd":
                if len(args) < 2:
                    print("Usage: cd <dir>")
                    return
                new_path = posixpath.normpath(posixpath.join(current_path, args[1]))
                if _upy.fs_is_dir(new_path):
                    current_path = new_path
                else:
                    print("Not a directory.")

            elif cmd == "get":
                if len(args) < 2:
                    print("Usage: get <remote> [local]")
                    return
                remote = posixpath.join(current_path, args[1])
                local = args[2] if len(args) >= 3 else None
                click.Context(get).invoke(get, remote=remote, local=local)

            elif cmd == "put":
                if len(args) < 2:
                    print("Usage: put <local> [remote]")
                    return
                
                local = args[1]
                remote = args[2] if len(args) >= 3 else None
                if remote is None:
                    remote = os.path.basename(local)
                remote = posixpath.join(current_path, remote)
                click.Context(put).invoke(put, local=local, remote=remote)

            elif cmd == "rm":
                if len(args) < 2:
                    print("Usage: rm <remote>")
                    return
                remote = posixpath.join(current_path, args[1])
                click.Context(rm).invoke(rm, remote=remote)

            elif cmd == "repl":
                _upy.repl()

            elif cmd == "pwd":
                print(current_path)

            else:
                print(f"Unknown command: {cmd}")
        except Exception as e:
            print("Error:", e)

    print(f"Connected to {_device} on {ANSIEC.FG.BRIGHT_GREEN}{_core}{ANSIEC.OP.RESET}")
    print("Type 'exit' to quit shell. Available: ls, cd, get, put, rm, repl, pwd")
    try:
        while True:
            print_prompt()
            line = input()
            if line.strip() == 'exit':
                break
            run_cmd(line.strip())
    except (EOFError, KeyboardInterrupt):
        print()
    finally:
        print("Exiting shell.")
    
def __force_remove_readonly(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"Deletion failed: {path}, error: {e}")

@cli.command()
def reset():
    _upy.reset()
    
@cli.command()
def env(): 
    """
    Create a .vscode folder with the upyboard environment.
    """
    
    vscode_dir = ".vscode" 

    upyboard_env_file = os.path.join(vscode_dir, ".upyboard")
    task_file = os.path.join(vscode_dir, "tasks.json") 
    settings_file = os.path.join(vscode_dir, "settings.json") 
    launch_file = os.path.join(vscode_dir, "launch.json")
    
    old_upyboard_contents = None
    
    task_file_contents = """{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run micropython with upyboard",
            "type": "shell",
            "command": "upy",
            "args": [
                "${file}"
            ],
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
"""

    settings_file_contents = """{
    "python.languageServer": "Pylance",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingModuleSource": "none",
    },
    "python.analysis.extraPaths": [
        "./.vscode"
    ]
}
"""

    launch_file_contents = """{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Python: Current file debug",
        "type": "debugpy",
        "request": "launch",
        "program": "${file}",
        "console": "integratedTerminal"
      }
    ]
  }
"""

    if os.path.exists(vscode_dir):
        upyboard_path = os.path.join(vscode_dir, ".upyboard")
        if os.path.isfile(upyboard_path):
            with open(upyboard_path, "r", encoding="utf-8") as f:
                old_upyboard_contents = f.read()
    
        try:
            print(f"The {vscode_dir} folder already exists. This folder will be deleted to proceed. Do you wish to continue? (y or n): ", end='')
            if input().strip().lower() == 'n':
                print("Canceling the operation")
                return
        except KeyboardInterrupt:
            print("Canceling the operation")
            return
        
        shutil.rmtree(vscode_dir, onerror=__force_remove_readonly)

    core_typehints = os.path.join(_core_path, "typehints")
    shutil.copytree(core_typehints, vscode_dir) 
    
    if _device_path:
        vscode_device_dir = os.path.join(vscode_dir, _device)  
        device_typehints = os.path.join(_device_path, "typehints")  
        shutil.copytree(device_typehints, vscode_device_dir) 

    with open(upyboard_env_file, "w", encoding="utf-8") as f:
        if old_upyboard_contents is not None:
            f.write(old_upyboard_contents)
        else:
            f.write("SERIAL_PORT=\n")

    with open(task_file, "w", encoding="utf-8") as f:
        f.write(task_file_contents)  

    with open(settings_file, "w", encoding="utf-8") as f:
        f.write(settings_file_contents)

    with open(launch_file, "w", encoding="utf-8") as f:
        f.write(launch_file_contents)

    if old_upyboard_contents is None:
        print(f"Please open the {ANSIEC.FG.BRIGHT_GREEN}.upyboard file{ANSIEC.OP.RESET} within the {ANSIEC.FG.BRIGHT_BLUE}.vscode folder{ANSIEC.OP.RESET} and configure the {ANSIEC.FG.BRIGHT_YELLOW}SERIAL_PORT{ANSIEC.OP.RESET} setting.") 


import mpy_cross

@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def upload(local, remote):
    """
    It compiles all source code from the local path into .mpy files and uploads them to the remote path.
    
    :param local: The local source code directory.\n
    :param remote: The remote path on the device. If not provided, root directory will be used.
    """
    
    def _mpy_output_path(base, filepath):
        relative_path = os.path.relpath(filepath, base)
        output_dir = os.path.join(os.path.dirname(base), "mpy", os.path.dirname(relative_path))
        os.makedirs(output_dir, exist_ok=True)
        
        filename = os.path.splitext(os.path.basename(filepath))[0] + ".mpy"
        return os.path.join(output_dir, filename)

    def _conv_py_to_mpy(local, base):
        args = ['_filepath_', '-o', '_outpath_', '-msmall-int-bits=31']
        
        if _core == "efr32mg":
            if _version < 1.19:
                args.append('-mno-unicode')
        elif _core == "esp32":
            args.append('-march=xtensa')
        elif _core == "rp2350":
            args.append('-march=armv7emsp')
        else:
            raise ValueError(f"Unsupported core: {_core}")
        
        if os.path.isfile(local):
            args[0] = local
            args[2] = os.path.splitext(local)[0] + ".mpy"    
            mpy_cross.run(*args)
        else:      
            for filename in os.listdir(local):
                filepath = os.path.join(local, filename)

                if os.path.isdir(filepath):
                    _conv_py_to_mpy(filepath, base)
                    continue

                if not filepath.endswith(".py"):
                    continue
    
                args[0] = filepath
                args[2] = _mpy_output_path(base, filepath)
                mpy_cross.run(*args)


    remote = _device_root_fs + (remote or "")
        
    _conv_py_to_mpy(local, base=local)
   
    if os.path.isfile(local):
        local = os.path.splitext(local)[0] + ".mpy"
        click.Context(put).invoke(put, local=local, remote=remote)
        os.remove(local)
    elif os.path.isdir(local):            
        shutil.rmtree(os.path.join(local, "__pycache__"), ignore_errors=True)

        local_mpy_dir = os.path.join(os.path.dirname(local), "mpy")
        if not os.path.exists(local_mpy_dir):
            return

        _upy.fs_mkdir(remote)

        for item in os.listdir(local_mpy_dir):
            local_item = os.path.join(local_mpy_dir, item)
            remote_item = os.path.join(remote, item).replace("\\", "/")
            click.Context(put).invoke(put, local=local_item, remote=remote_item)

        shutil.rmtree(local_mpy_dir, onerror=__force_remove_readonly)
    else:
        print("The local path is not a file or directory.")
    
@cli.command()
def init():
    """
    Initialize the file system of the device.
    """
    
    if _version < 1.12:
        print("Unkown micropython version " + ANSIEC.FG.BRIGHT_RED + f"{_version}" + ANSIEC.OP.RESET)
        raise click.Abort()
    
    if not click.Context(format).invoke(format):
        print("Unable to format the file system. Please check the " + ANSIEC.FG.BRIGHT_RED + f"{_device}" + ANSIEC.OP.RESET)
        return 
        
    _upy.fs_mkdir(_device_root_fs + "lib/")

    upload_format_str = (
        "Uploading the " 
        + ANSIEC.FG.BRIGHT_YELLOW + "{0}" + ANSIEC.OP.RESET 
        + " library on the " 
        + ANSIEC.FG.BRIGHT_YELLOW + "{1}" + ANSIEC.OP.RESET
    )
    
    core_src= os.path.join(_core_path, "src")
    if os.path.exists(core_src):
        print(upload_format_str.format("Core", _device))
        click.Context(upload).invoke(upload, local=core_src, remote="lib/")
    
    if _device_path:
        device_src = os.path.join(_device_path, "src")
        if os.path.exists(device_src):
            print(upload_format_str.format("Device", _device))
            click.Context(upload).invoke(upload, local=device_src, remote="lib/" + _device)

    print("The job is done!")


def _is_bluetooth_port(port_info):
    bt_keywords = ['bluetooth', 'bth', 'devb', 'rfcomm', 'Blue', 'BT']
    description = port_info.description.lower()
    device = port_info.device.lower()
    return any(keyword in description or keyword in device for keyword in bt_keywords)

@cli.command()
@click.option(
    "--raw",
    "-r",
    is_flag=True,
    default=False,
    help="Enable raw REPL mode for scanning",
)
def scan(raw:bool):
    """
    Display the list of connected boards.
    
    :param raw: If True, display detailed information about the connected device. otherwise, display the version and device name.
    """

    color_tbl = (ANSIEC.FG.BRIGHT_YELLOW, ANSIEC.FG.BRIGHT_GREEN, ANSIEC.FG.BRIGHT_BLUE)
    color_pos = 0    
    
    for port in list_ports.comports():
        if _is_bluetooth_port(port):
            continue
        descript = get_micropython_board_info(port.device, raw)
            
        if descript:
            color_pos = (color_pos + 1) % len(color_tbl)
            if not raw:
                version, date, core, device = descript
                                                 
                print(color_tbl[color_pos] + f"{port.device}" + ANSIEC.OP.RESET + f"\t{version:5} {date:10}" + color_tbl[color_pos] + f"  {device}" + ANSIEC.OP.RESET)
            else:
                print(color_tbl[color_pos] + f"{port.device}" + ANSIEC.OP.RESET + f"\t{descript}")

#--------------------------------------------------------------

UPDATE_INTERVAL = 60 * 60 * 24  
UPDATE_TIMESTAMP_FILE = pathlib.Path.home() / ".upyboard_update_check"


def _should_check_for_updates() -> bool:
    """
    Check if the update check should be performed based on the last check time.
    
    :return: True if the update check should be performed, False otherwise.
    """
    
    if UPDATE_TIMESTAMP_FILE.exists():
        last_check = UPDATE_TIMESTAMP_FILE.stat().st_mtime
        if time.time() - last_check < UPDATE_INTERVAL:
            return False
    return True

def check_for_updates(current_version):
    """
    Check PyPI for a newer version of upyboard and prompt the user to upgrade.
    """
        
    if not _should_check_for_updates():
        return

    try:
        with urllib.request.urlopen("https://pypi.org/pypi/upyboard/json") as resp:
            data = json.loads(resp.read().decode("utf-8"))
        latest_version = data["info"]["version"]

        if packaging.version.parse(latest_version) > packaging.version.parse(current_version):
            if click.confirm(f"A newer version ({latest_version}) is available. Update now?"):
                subprocess.run([
                    sys.executable, "-m", "pip", "install",
                    "--upgrade", "upyboard",
                    "--upgrade-strategy", "eager"
                ])
                sys.exit(0)
    except Exception as e:
        pass
    
    try:
        UPDATE_TIMESTAMP_FILE.touch()
    except Exception:
        pass


def main():    
    check_for_updates(__version__)

    if not any(item in sys.argv for item in ('get', 'put', 'rm', 'run', 'upload')) and sys.argv[-1].split('.')[-1] == 'py':
        index = next((i for i, arg in enumerate(sys.argv[1:], 1) if arg in ['-i', '--input-echo-on', '-n', '--no-waiting']), None)
        if index is not None:
            sys.argv.insert(index, 'run')
        else:
            sys.argv.insert(-1, 'run')

    exit_code = cli()
    sys.exit(exit_code)
        	
if __name__ == '__main__':
    main()