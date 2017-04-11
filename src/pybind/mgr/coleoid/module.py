"""
A RESTful API for Ceph
"""

import json
import inspect
import StringIO
import threading
import traceback
import ConfigParser

import api
import common

from uuid import uuid4
from flask import Flask
from OpenSSL import SSL
from flask_restful import Api

from mgr_module import MgrModule, CommandResult

# Global instance to share
instance = None



class CommandsRequest(object):
    """
    This class handles parallel as well as sequential execution of
    commands. The class accept a list of iterables that should be
    executed sequentially. Each iterable can contain several commands
    that can be executed in parallel.

    Example:
    [[c1,c2],[c3,c4]]
     - run c1 and c2 in parallel
     - wait for them to finish
     - run c3 and c4 in parallel
     - wait for them to finish
    """


    def __init__(self, commands_arrays):
        self.id = str(id(self))

        # Filter out empty sub-requests
        commands_arrays = filter(
            lambda x: len(x) != 0,
            commands_arrays,
        )

        self.running = []
        self.waiting = commands_arrays[1:]
        self.finished = []
        self.failed = []

        self.lock = threading.RLock()
        if not len(commands_arrays):
            # Nothing to run
            return

        # Process first iteration of commands_arrays in parallel
        results = self.run(commands_arrays[0])

        self.running.extend(results)


    def run(self, commands):
        """
        A static method that will execute the given list of commands in
        parallel and will return the list of command results.
        """

        # Gather the results (in parallel)
        results = []
        for index in range(len(commands)):
            tag = '%s:%d' % (str(self.id), index)

            # Store the result
            result = CommandResult(tag)
            result.command = common.humanify_command(commands[index])
            results.append(result)

            # Run the command
            instance.send_command(result, json.dumps(commands[index]), tag)

        return results


    def next(self):
        with self.lock:
            if not self.waiting:
                # Nothing to run
                return

            # Run a next iteration of commands
            commands = self.waiting[0]
            self.waiting = self.waiting[1:]

            self.running.extend(self.run(commands))


    def finish(self, tag):
        with self.lock:
            for index in range(len(self.running)):
                if self.running[index].tag == tag:
                    if self.running[index].r == 0:
                        self.finished.append(self.running.pop(index))
                    else:
                        self.failed.append(self.running.pop(index))
                    return True

            # No such tag found
            return False


    def is_running(self, tag):
        for result in self.running:
            if result.tag == tag:
                return True
        return False


    def is_ready(self):
        with self.lock:
            return not self.running and self.waiting


    def is_waiting(self):
        return bool(self.waiting)


    def is_finished(self):
        with self.lock:
            return not self.running and not self.waiting


    def has_failed(self):
        return bool(self.failed)


    def get_state(self):
        with self.lock:
            if not self.is_finished():
                return "pending"

            if self.has_failed():
                return "failed"

            return "success"


    def humanify(self):
        return {
            'id': self.id,
            'running': map(
                lambda x: (x.command, x.outs, x.outb),
                self.running
            ),
            'finished': map(
                lambda x: (x.command, x.outs, x.outb),
                self.finished
            ),
            'waiting': map(
                lambda x: (x.command, x.outs, x.outb),
                self.waiting
            ),
            'failed': map(
                lambda x: (x.command, x.outs, x.outb),
                self.failed
            ),
            'is_waiting': self.is_waiting(),
            'is_finished': self.is_finished(),
            'has_failed': self.has_failed(),
            'state': self.get_state(),
        }



class Module(MgrModule):
    COMMANDS = []

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        global instance
        instance = self

        self.requests = []
        self.requests_lock = threading.RLock()

        self.tokens = {}
        self.disable_auth = False

        self.app = None
        self.api = None


    def serve(self):
        try:
            self._serve()
        except:
            self.log.error(str(traceback.format_exc()))


    def _serve(self):
        # Load stored authentication tokens
        self.tokens = self.get_config_json("tokens") or {}

        # Create the Flask app
        self.app = Flask('coleoid')
        self.app.config['RESTFUL_JSON'] = {
            'sort_keys': True,
            'indent': 4,
            'separators': (',', ': '),
        }
        self.api = Api(self.app)

        # Add the resources as defined in api module
        for _obj in dir(api):
            obj = getattr(api, _obj)
            # We need this try statement because some objects (request)
            # throw exception on any out of context object access
            try:
                _endpoint = getattr(obj, '_endpoint', None)
            except:
                _endpoint = None
            if _endpoint:
                self.api.add_resource(obj, _endpoint)

        # use SSL context for https
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file('/etc/ssl/private/ceph-coleoid.key')
        context.use_certificate_file('/etc/ssl/certs/ceph-coleoid.crt')

        self.app.run(host='0.0.0.0', port=8002, ssl_context=context)


    def notify(self, notify_type, tag):
        try:
            self._notify(notify_type, tag)
        except:
            self.log.error(str(traceback.format_exc()))


    def _notify(self, notify_type, tag):
        if notify_type == "command":
            # we can safely skip all the sequential commands
            if tag == 'seq':
                return

            request = filter(
                lambda x: x.is_running(tag),
                self.requests)

            if len(request) != 1:
                self.log.warn("Unknown request '%s'" % str(tag))
                return

            request = request[0]
            request.finish(tag)
            if request.is_ready():
                request.next()
        else:
            self.log.debug("Unhandled notification type '%s'" % notify_type)


    def get_doc_api(self):
        doc = {}
        for _obj in dir(api):
            obj = getattr(api, _obj)
            # We need this try statement because some objects (request)
            # throw exception on any out of context object access
            try:
                _endpoint = getattr(obj, '_endpoint', None)
            except:
                _endpoint = None
            if _endpoint:
                doc[_endpoint] = {}
                for method in 'get', 'post', 'patch', 'delete':
                    if getattr(obj, method, None):
                        doc[_endpoint][method.upper()] = inspect.getdoc(getattr(obj, method)).split('\n')
        return doc


    def get_mons(self):
        mon_map_mons = self.get('mon_map')['mons']
        mon_status = json.loads(self.get('mon_status')['json'])

        # Add more information
        for mon in mon_map_mons:
            mon['in_quorum'] = mon['rank'] in mon_status['quorum']
            mon['server'] = self.get_metadata("mon", mon['name'])['hostname']
            mon['leader'] = mon['rank'] == mon_status['quorum'][0]

        return mon_map_mons


    def get_osd_pools(self):
        osds = dict(map(lambda x: (x['osd'], []), self.get('osd_map')['osds']))
        pools = dict(map(lambda x: (x['pool'], x), self.get('osd_map')['pools']))
        crush_rules = self.get('osd_map_crush')['rules']

        osds_by_pool = {}
        for pool_id, pool in pools.items():
            pool_osds = None
            for rule in [r for r in crush_rules if r['ruleset'] == pool['crush_ruleset']]:
                if rule['min_size'] <= pool['size'] <= rule['max_size']:
                    pool_osds = common.crush_rule_osds(self.get('osd_map_tree')['nodes'], rule)

            osds_by_pool[pool_id] = pool_osds

        for pool_id in pools.keys():
            for in_pool_id in osds_by_pool[pool_id]:
                osds[in_pool_id].append(pool_id)

        return osds


    def get_osds(self, ids=[], pool_id=None):
        # Get data
        osd_map = self.get('osd_map')
        osd_metadata = self.get('osd_metadata')

        # Update the data with the additional info from the osd map
        osds = osd_map['osds']

        # Filter by osd ids
        if ids:
            osds = filter(
                lambda x: str(x['osd']) in ids,
                osds
            )

        # Get list of pools per osd node
        pools_map = self.get_osd_pools()

        # map osd IDs to reweight
        reweight_map = dict([
            (x.get('id'), x.get('reweight', None))
            for x in self.get('osd_map_tree')['nodes']
        ])

        # Build OSD data objects
        for osd in osds:
            osd['pools'] = pools_map[osd['osd']]
            osd['server'] = osd_metadata.get(str(osd['osd']), {}).get('hostname', None)

            osd['reweight'] = reweight_map.get(osd['osd'], 0.0)

            if osd['up']:
                osd['valid_commands'] = common.OSD_IMPLEMENTED_COMMANDS
            else:
                osd['valid_commands'] = []

        # Filter by pool
        if pool_id:
            pool_id = int(pool_id)
            osds = filter(
                lambda x: pool_id in x['pools'],
                osds
            )

        return osds


    def get_osd_by_id(self, osd_id):
        osd = filter(
            lambda x: x['osd'] == osd_id,
            self.get('osd_map')['osds']
        )

        if len(osd) != 1:
            return None

        return osd[0]


    def get_pool_by_id(self, pool_id):
        pool = filter(
            lambda x: x['pool'] == pool_id,
            self.get('osd_map')['pools'],
        )

        if len(pool) != 1:
            return None

        return pool[0]


    def submit_request(self, _request):
        request = CommandsRequest(_request)
        self.requests.append(request)
        return request.humanify()


    def run_command(self, command):
        # tag with 'seq' so that we can ingore these in notify function
        result = CommandResult('seq')

        self.send_command(result, json.dumps(command), 'seq')
        return result.wait()


    def verify_user(self, username, password):
        r, outb, outs = self.run_command({
            'prefix': 'auth get',
            'entity': username,
        })

        if r != 0:
            return 'No such user/key'

        ## check the capabilities, we are looking for mon allow *
        conf = ConfigParser.ConfigParser()

        # ConfigParser can't handle tabs, remove them
        conf.readfp(StringIO.StringIO(outb.replace('\t', '')))

        if not conf.has_section(username):
            return 'Failed to parse the auth details'

        key = conf.get(username, 'key')

        if password != key:
            return 'Invalid key'

        if not conf.has_option(username, 'caps mon'):
            return 'No mon caps set'

        caps = conf.get(username, 'caps mon')

        if caps != '"allow *"':
            return 'Insufficient mon caps set'

        # Returning '' means 'no objections'
        return ''


    def set_token(self, user):
        self.tokens[user] = str(uuid4())

        self.set_config_json("tokens", self.tokens)

        return self.tokens[user]


    def unset_token(self, user):
        if user not in self.tokens:
            return False

        del self.tokens[user]
        self.set_config_json("tokens", self.tokens)

        return True
