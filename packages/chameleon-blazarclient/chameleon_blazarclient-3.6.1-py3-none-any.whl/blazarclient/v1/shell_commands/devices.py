# Copyright (c) 2014 Bull.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from blazarclient import command
from blazarclient import exception
import logging


class ListDevices(command.ListCommand):
    """Print a list of devices."""
    resource = 'device'
    log = logging.getLogger(__name__ + '.ListDevices')
    list_columns = ['id', 'name', 'device_type']
    long_columns = ['machine_name', 'model', 'device_name', 'device_driver', 'reservable']

    def get_parser(self, prog_name):
        parser = super(ListDevices, self).get_parser(prog_name)
        parser.add_argument(
            '--sort-by', metavar="<device_column>",
            help='column name used to sort result',
            default='name'
        )
        return parser


class ShowDevice(command.ShowCommand):
    """Show device details."""
    resource = 'device'
    json_indent = 4
    name_key = 'name'
    log = logging.getLogger(__name__ + '.ShowDevice')

    def get_parser(self, prog_name):
        parser = super(ShowDevice, self).get_parser(prog_name)
        if self.allow_names:
            help_str = 'Name or ID of %s to look up'
        else:
            help_str = 'ID of %s to look up'
        parser.add_argument('id', metavar=self.resource.upper(),
                            help=help_str % self.resource)
        return parser


class CreateDevice(command.CreateCommand):
    """Create a device."""
    resource = 'device'
    json_indent = 4
    log = logging.getLogger(__name__ + '.CreateDevice')

    def get_parser(self, prog_name):
        parser = super(CreateDevice, self).get_parser(prog_name)
        parser.add_argument(
            'name', metavar=self.resource.upper(),
            help='Name of the device to add'
        )
        parser.add_argument(
            '--device-type',
            default='container',
            help='Choose from container, vm, or shell. '
                 'Default to container'
        )
        parser.add_argument(
            '--device-driver',
            default='zun',
            help='The driver of the device'
        )
        parser.add_argument(
            '--extra', metavar='<key>=<value>',
            action='append',
            dest='extra_capabilities',
            default=[],
            help='Extra capabilities key/value pairs to add for the device'
        )
        return parser

    def args2body(self, parsed_args):
        params = {}
        parsed_args_dict = vars(parsed_args)
        for arg in ['name', 'device_type', 'device_driver']:
            if parsed_args_dict.get(arg):
                params[arg] = parsed_args_dict.get(arg)
        extras = {}
        if parsed_args.extra_capabilities:
            for capa in parsed_args.extra_capabilities:
                key, _sep, value = capa.partition('=')
                extras[key] = value
            params.update(extras)
        return params


class UpdateDevice(command.UpdateCommand):
    """Update attributes of a device."""
    resource = 'device'
    json_indent = 4
    log = logging.getLogger(__name__ + '.UpdateDevice')
    name_key = 'name'

    def get_parser(self, prog_name):
        parser = super(UpdateDevice, self).get_parser(prog_name)
        parser.add_argument(
            '--device-type',
            help='Choose from container, vm, or shell. '
                 'Default to container'
        )
        parser.add_argument(
            '--device-driver',
            help='The driver of the device'
        )
        parser.add_argument(
            '--extra', metavar='<key>=<value>',
            action='append',
            dest='extra_capabilities',
            default=[],
            help='Extra capabilities key/value pairs to update for the device'
        )
        return parser

    def args2body(self, parsed_args):
        params = {}
        parsed_args_dict = vars(parsed_args)
        for arg in ['name', 'device_type', 'device_driver']:
            if parsed_args_dict.get(arg):
                params[arg] = parsed_args_dict.get(arg)
        extras = {}
        if parsed_args.extra_capabilities:
            for capa in parsed_args.extra_capabilities:
                key, _sep, value = capa.partition('=')
                extras[key] = value
            params['values'] = extras
        return params


class UnsetAttributeDevice(UpdateDevice):
    log = logging.getLogger(__name__ + '.UnsetAttributeDevice')

    def get_parser(self, prog_name):
        parser = super(UpdateDevice, self).get_parser(prog_name)
        parser.add_argument(
            '--extra', metavar='<key>',
            action='append',
            dest='extra_capabilities',
            default=[],
            help='Extra capability keys which should be unset from the device.',
        )
        return parser

    def args2body(self, parsed_args):
        if parsed_args.extra_capabilities:
            return {
                'values': {
                    cap: None for cap in parsed_args.extra_capabilities
                }
            }
        else:
            return {}


class DeleteDevice(command.DeleteCommand):
    """Delete a device."""
    resource = 'device'
    log = logging.getLogger(__name__ + '.DeleteDevice')
    name_key = 'name'


class ShowDeviceAllocation(command.ShowAllocationCommand):
    """Show device allocation details."""
    resource = 'device'
    json_indent = 4
    log = logging.getLogger(__name__ + '.ShowDeviceAllocation')


class ListDeviceAllocations(command.ListAllocationCommand):
    """List device allocations."""
    resource = 'device'
    log = logging.getLogger(__name__ + '.ListDeviceAllocations')
    list_columns = ['resource_id', 'reservations']

    def get_parser(self, prog_name):
        parser = super(ListDeviceAllocations, self).get_parser(prog_name)
        parser.add_argument(
            '--sort-by', metavar="<device_column>",
            help='column name used to sort result',
            default='resource_id'
        )
        return parser


class ReallocateDevice(command.ReallocateCommand):
    """Reallocate device from current allocations."""
    resource = 'device'
    json_indent = 4
    log = logging.getLogger(__name__ + '.ReallocateDevice')
    name_key = 'name'

    def get_parser(self, prog_name):
        parser = super(ReallocateDevice, self).get_parser(prog_name)
        parser.add_argument(
            '--lease-id',
            help='Lease ID to reallocate device from.')
        parser.add_argument(
            '--reservation-id',
            help='Reservation ID to reallocate device from')
        return parser

    def args2body(self, parsed_args):
        params = {}

        if parsed_args.reservation_id:
            params['reservation_id'] = parsed_args.reservation_id
        elif parsed_args.lease_id:
            params['lease_id'] = parsed_args.lease_id

        return params


class ShowDeviceProperty(command.ShowPropertyCommand):
    """Show device property."""
    resource = 'device'
    json_indent = 4
    log = logging.getLogger(__name__ + '.ShowDeviceProperty')


class ListDeviceProperties(command.ListCommand):
    """List device properties."""
    resource = 'device'
    log = logging.getLogger(__name__ + '.ListDeviceProperties')
    list_columns = ['property', 'private', 'property_values']

    def args2body(self, parsed_args):
        params = {
            'detail': parsed_args.detail,
            'all': parsed_args.all,
        }
        if parsed_args.sort_by:
            if parsed_args.sort_by in self.list_columns:
                params['sort_by'] = parsed_args.sort_by
            else:
                msg = 'Invalid sort option %s' % parsed_args.sort_by
                raise exception.BlazarClientException(msg)

        return params

    def retrieve_list(self, parsed_args):
        """Retrieve a list of resources from Blazar server."""
        blazar_client = self.get_client()
        body = self.args2body(parsed_args)
        resource_manager = getattr(blazar_client, self.resource)
        data = resource_manager.list_properties(**body)
        return data

    def get_parser(self, prog_name):
        parser = super(ListDeviceProperties, self).get_parser(prog_name)
        parser.add_argument(
            '--detail',
            action='store_true',
            help='Return properties with values and attributes.',
            default=False
        )
        parser.add_argument(
            '--sort-by', metavar="<property_column>",
            help='column name used to sort result',
            default='property'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Return all properties, public and private.',
            default=False
        )
        return parser


class UpdateDeviceProperty(command.UpdatePropertyCommand):
    """Update attributes of a device property."""
    resource = 'device'
    json_indent = 4
    log = logging.getLogger(__name__ + '.UpdateDeviceProperty')
    name_key = 'property_name'
