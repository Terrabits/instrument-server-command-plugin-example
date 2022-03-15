# Instrument Server Command Plugin Example

Instrument Server Command Plugin Example is an [Instrument Server](https://github.com/Terrabits/instrument-server) microservice which responds to one command:

`is_rs_devices?`

## Requirements

-   Python ~= 3.7
-   instrument-server ~= 1.3.7
-   *At least one* R&S Instrument

## Install

Run `scripts/install` to install a known-good package and version set.

See the lock file for details:

[requirements.txt.lock](./requirements.txt.lock)

## Instrument Server Command Plugins

The Instrument Server Command Plugin interface can be used to implement commands in python.

Command Plugins are implemented as classes with a specific interface. They are typically subclasses of the `instrument_server.command.Base` class.

Command Plugins must implement the following methods.

```python
Command.is_match(self, received_command)
Command.execute(self, received_command)
```

### is_match

```python
def is_match(self, received_command):
  return True or False
```

The `is_match` method should return `True` if this class can `execute` the `received_command`; it should return `False` otherwise.

Note that `received_command` is of type `bytes`.

### execute

```python
def execute(self, received_command):
  return optional_result
```

If `is_match` returns `True`, the `execute` method will be called. `execute` should perform the work associated with the `received_command` (type: `bytes`), and can optionally return a result.

The input `received_command` is provided for argument parsing.

The command `Base` class provides the `self.devices` property (type: `dict`) for device communcation:

```python
self.devices['name']  # => object
```

Note that devices are referenced by their `name` from the project YAML config file.

## `is_rs_devices?` Command

The `IsRsDevices` Command Plugin can be found in [plugins/commands/is_rs_devices.py](plugins/commands/is_rs_devices.py).

### `is_match`

`is_match` should only return true if the `received_command` is `is_rs_devices?`.

```python
def is_match(self, received_command):
      return received_command.strip() == b'is_rs_devices?'
```

### `execute`

As noted above, connected `devices` can be accessed via the `self.devices` property (type: `dict`).

```python
def execute(self, received_command):
      for device in self.devices.values():
          id_string = device.query(b'*IDN?\n').strip()
          if b'ROHDE' not in id_string.upper():
              # not R&S device
              return b'false'

      # all devices R&S
      return b'true'
```

This implementation loops through each device *object*, queries `*IDN?`, then performs a case-insensitive search for the substring `rohde`.

It returns `false` if any device `*IDN?` response does not contain `rohde` (case-insensitive). Otherwise it returns `true`.

## Project Config File

Every `instrument-server` project is required to include a YAML config file. By convention, the config file must contain the following sections:

```yaml
plugins: {...}
devices: {...}
# Translation Commands (Optional)
...
```

The config file for this project is [command_plugin_example.yaml](command_plugin_example.yaml). Each section of the file is explained below.

### Plugins

```yaml
plugins:
  plugins.commands.is_rs_devices: {}
```

The `is_rs_devices?` command plugin is referenced for import. No plugin configuration settings are provided.

### Devices

```yaml
instrument:
  type:        socket
  address:     localhost
  port:        5025
  timeout:     5
```

`instrument` is the only device declared. It uses the (TCP) `socket` connection type.

Edit the `address` field to match the address of the R&S Instrument.

### Translation Commands

An `instrument-server` project file may include `Translation` command definition(s).

No Translation commands are defined in this project.

## Start

Run `scripts/start` to serve `command_plugin_example.yaml` on all network interfaces on port `9000`.

`scripts/start` calls the `instrument-server` Command Line Interface (CLI), which provides additional settings.

From `instrument-server --help`:

```comment
usage: instrument-server [-h] [--address ADDRESS] [--port PORT]
                         [--termination TERMINATION] [--debug-mode]
                         config_filename

Command Line Interface for starting Instrument Server microservices

positional arguments:
  config_filename

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS, -a ADDRESS
                        Set listening address. Default: 0.0.0.0
  --port PORT, -p PORT  Set listening port. Default: random
  --termination TERMINATION, -t TERMINATION
                        Set the termination character. Default: "\n"
  --debug-mode, -d      print debug info to stdout
```

## Client Script

The `client.py` script is provided for testing. It connects to the Instrument Server Command Plugin Example microservice, sends `init`, then checks for errors.

`client.py` can be run from the command line as follows:

```shell
scripts/start-in-background
# => Running on 0.0.0.0:9000...

# run client
python client.py
# => is_rs_devices? true
```

## References

-   [Introduction to YAML](https://dev.to/paulasantamaria/introduction-to-yaml-125f)
-   [instrument-server](https://github.com/Terrabits/instrument-server)
