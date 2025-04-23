## nacos-sdk-python v2

A Python implementation of Nacos OpenAPI.

see: [https://nacos.io/zh-cn/docs/open-API.html](https://nacos.io/zh-cn/docs/open-API.html)

[![Pypi Version](https://camo.githubusercontent.com/e12233f7e290ac3e5f3860fcb8f8aebb21fcfabaab11572dc1a25d700f4c9f9a/68747470733a2f2f62616467652e667572792e696f2f70792f6e61636f732d73646b2d707974686f6e2e737667)](https://badge.fury.io/py/nacos-sdk-python) [![License](https://camo.githubusercontent.com/c355f200ea90fddaa407b6eaab303663a669248ea3ca7b1fcf77dbe04ff5f48c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d417061636865253230322e302d626c75652e737667)](https://github.com/nacos-group/nacos-sdk-python/blob/master/LICENSE)

### Supported Python version：

Python 3.7+

### Supported Nacos version

Supported Nacos version over 2.x

## Installation

```shell
 pip install nacos-sdk-python==2.0.3
```

## Client Configuration

```
from v2.nacos import NacosNamingService, ClientConfigBuilder, GRPCConfig, Instance, SubscribeServiceParam, \
    RegisterInstanceParam, DeregisterInstanceParam, BatchRegisterInstanceParam, GetServiceParam, ListServiceParam, \
    ListInstanceParam, NacosConfigService, ConfigParam
    
client_config = (ClientConfigBuilder()
                 .access_key(os.getenv('NACOS_ACCESS_KEY'))
                 .secret_key(os.getenv('NACOS_SECRET_KEY'))
                 .server_address(os.getenv('NACOS_SERVER_ADDR', 'localhost:8848'))
                 .log_level('INFO')
                 .grpc_config(GRPCConfig(grpc_timeout=5000))
                 .build())
```

-   _server\_address_ - **required** - Nacos server address
-   _access\_key_ - The aliyun accessKey to authenticate.
-   _secret\_key_ - The aliyun secretKey to authenticate.
-   _credentials\_provider_ - The custom access key manager.
-   _username_ - The username to authenticate.
-   _password_ - The password to authenticate.
-   _log\_level_ - Log level | default: `logging.INFO`
-   _cache\_dir_ - cache dir path. | default: `~/nacos/cache`
-   _log\_dir_ - log dir path. | default: `~/logs/nacos`
-   _namespace\_id_ - namespace id. | default: \`\`
-   _grpc\_config_ - grpc config.
    -   _max\_receive\_message\_length_ - max receive message length in grpc. | default: 100 \* 1024 \* 1024
    -   _max\_keep\_alive\_ms_ - max keep alive ms in grpc. | default: 60 \* 1000
    -   _initial\_window\_size_ - initial window size in grpc. | default: 10 \* 1024 \* 1024
    -   _initial\_conn\_window\_size_ - initial connection window size in grpc. | default: 10 \* 1024 \* 1024
    -   _grpc\_timeout_ - grpc timeout in milliseconds. default: 3000
-   _tls\_config_ - tls config
    -   _enabled_ - whether enable tls.
    -   _ca\_file_ - ca file path.
    -   _cert\_file_ - cert file path.
    -   _key\_file_ - key file path.
-   _kms\_config_ - aliyun kms config
    -   _enabled_ - whether enable aliyun kms.
    -   _endpoint_ - aliyun kms endpoint.
    -   _access\_key_ - aliyun accessKey.
    -   _secret\_key_ - aliyun secretKey.
    -   _password_ - aliyun kms password.

## Config Client

```

config_client = await NacosConfigService.create_config_service(client_config)

```

### config client common parameters

> `param: ConfigParam`

-   `param` _data\_id_ Data id.
-   `param` _group_ Group, use `DEFAULT_GROUP` if no group specified.
-   `param` _content_ Config content.
-   `param` _tag_ Config tag.
-   `param` _app\_name_ Application name.
-   `param` _beta\_ips_ Beta test ip address.
-   `param` _cas\_md5_ MD5 check code.
-   `param` _type_ Config type.
-   `param` _src\_user_ Source user.
-   `param` _encrypted\_data\_key_ Encrypted data key.
-   `param` _kms\_key\_id_ Kms encrypted data key id.
-   `param` _usage\_type_ Usage type.

### Get Config

```
content = await config_client.get_config(ConfigParam(
            data_id=data_id,
            group=group
        ))
```

-   `param` _ConfigParam_ config client common parameters. When getting configuration, it is necessary to specify the required data\_id and group in param.
-   `return` Config content if success or an exception will be raised.

Get value of one config item following priority:

-   Step 1 - Get from local failover dir.
    
-   Step 2 - Get from one server until value is got or all servers tried.
    
    -   Content will be saved to snapshot dir after got from server.
-   Step 3 - Get from snapshot dir.
    

### Add Listener

```
async def config_listener(tenant, data_id, group, content):
    print("listen, tenant:{} data_id:{} group:{} content:{}".format(tenant, data_id, group, content))

await config_client.add_listener(dataID, groupName, config_listener)
```

-   `param` _ConfigParam_ config client common parameters.
-   `listener` _listener_ Configure listener, defined by the namespace\_id、group、data\_id、content.
-   `return`

Add Listener to a specified config item.

-   Once changes or deletion of the item happened, callback functions will be invoked.
-   If the item is already exists in server, callback functions will be invoked for once.
-   Callback functions are invoked from current process.

### Remove Listener

```
await client.remove_listener(dataID, groupName, config_listener)
```

-   `param` _ConfigParam_ config client common parameters.
-   `return` True if success or an exception will be raised.

Remove watcher from specified key.

### Publish Config

```
res = await client.publish_config(ConfigParam(
            data_id=dataID,
            group=groupName,
            content="Hello world")
        )
```

-   `param` _ConfigParam_ config client common parameters. When publishing configuration, it is necessary to specify the required data\_id, group and content in param.
-   `return` True if success or an exception will be raised.

Publish one congfig data item to Nacos.

-   If the data key is not exist, create one first.
-   If the data key is exist, update to the content specified.
-   Content can not be set to None, if there is need to delete config item, use function **remove** instead.

### Remove Config

```
res = await client.remove_config(ConfigParam(
            data_id=dataID,
            group=groupName
        ))
```

-   `param` _ConfigParam_ config client common parameters.When removing configuration, it is necessary to specify the required data\_id and group in param.
-   `return` True if success or an exception will be raised.

Remove one config data item from Nacos.

### Stop Config Client

## Naming Client

```

naming_client = await NacosNamingService.create_naming_service(client_config)

```

### Register Instance

```
response = await client.register_instance(
            request=RegisterInstanceParam(service_name='nacos.test.1', group_name='DEFAULT_GROUP', ip='1.1.1.1',
                port=7001, weight=1.0, cluster_name='c1', metadata={'a': 'b'},
                enabled=True,
                healthy=True, ephemeral=True))
```

### Batch Register Instance

```
param1 = RegisterInstanceParam(service_name='nacos.test.1',
                                       group_name='DEFAULT_GROUP',
                                       ip='1.1.1.1',
                                       port=7001,
                                       weight=1.0,
                                       cluster_name='c1',
                                       metadata={'a': 'b'},
                                       enabled=True,
                                       healthy=True,
                                       ephemeral=True
                                       )
param2 = RegisterInstanceParam(service_name='nacos.test.1',
                               group_name='DEFAULT_GROUP',
                               ip='1.1.1.1',
                               port=7002,
                               weight=1.0,
                               cluster_name='c1',
                               metadata={'a': 'b'},
                               enabled=True,
                               healthy=True,
                               ephemeral=True
                               )
param3 = RegisterInstanceParam(service_name='nacos.test.1',
                               group_name='DEFAULT_GROUP',
                               ip='1.1.1.1',
                               port=7003,
                               weight=1.0,
                               cluster_name='c1',
                               metadata={'a': 'b'},
                               enabled=True,
                               healthy=False,
                               ephemeral=True
                               )
response = await client.batch_register_instances(
    request=BatchRegisterInstanceParam(service_name='nacos.test.1', group_name='DEFAULT_GROUP',
                                       instances=[param1, param2, param3]))
```

### Deregister Instance

```
response = await client.deregister_instance(
          request=DeregisterInstanceParam(service_name='nacos.test.1', group_name='DEFAULT_GROUP', ip='1.1.1.1',
                                          port=7001, cluster_name='c1', ephemeral=True)
      )
```

### Update Instance

```
response = await client.update_instance(
            request=RegisterInstanceParam(service_name='nacos.test.1', group_name='DEFAULT_GROUP', ip='1.1.1.1',
                                          port=7001, weight=2.0, cluster_name='c1', metadata={'a': 'b'},
                                          enabled=True,
                                          healthy=True, ephemeral=True))
```

### Get Service

```
service = await client.get_service(
            GetServiceParam(service_name='nacos.test.1', group_name='DEFAULT_GROUP', cluster_name='c1'))
```

### List Service

```

service_list = await client.list_services(ListServiceParam())

```

### List Instance

```

instance_list = await client.list_instances(ListInstanceParam(service_name='nacos.test.1', healthy_only=True))
instance_list = await client.list_instances(ListInstanceParam(service_name='nacos.test.1', healthy_only=False))
instance_list = await client.list_instances(ListInstanceParam(service_name='nacos.test.1', healthy_only=None))

```

### Subscribe

```
async def cb(instance_list: list[Instance]):
  print('received subscribe callback', str(instance_list))

await client.subscribe(
  SubscribeServiceParam(service_name='nacos.test.1', group_name='DEFAULT_GROUP', subscribe_callback=cb))
```

### Unsubscribe

```
async def cb(instance_list: list[Instance]):
  print('received subscribe callback', str(instance_list))

await client.unsubscribe(
            SubscribeServiceParam(service_name='nacos.test.1', group_name='DEFAULT_GROUP', subscribe_callback=cb))
```

## nacos-sdk-python 1.0

A Python implementation of Nacos OpenAPI.

see: [https://nacos.io/docs/latest/guide/user/open-api/](https://nacos.io/docs/latest/guide/user/open-api/)

[![Pypi Version](https://camo.githubusercontent.com/e12233f7e290ac3e5f3860fcb8f8aebb21fcfabaab11572dc1a25d700f4c9f9a/68747470733a2f2f62616467652e667572792e696f2f70792f6e61636f732d73646b2d707974686f6e2e737667)](https://badge.fury.io/py/nacos-sdk-python) [![License](https://camo.githubusercontent.com/c355f200ea90fddaa407b6eaab303663a669248ea3ca7b1fcf77dbe04ff5f48c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d417061636865253230322e302d626c75652e737667)](https://github.com/nacos-group/nacos-sdk-python/blob/master/LICENSE)

### Supported Python version：

Python 2.7 Python 3.6 Python 3.7

### Supported Nacos version

Nacos 0.8.0+ Nacos 1.x Nacos 2.x with http protocol

## Installation

```shell
pip install nacos-sdk-python
```

## Getting Started

```python
import nacos

# Both HTTP/HTTPS protocols are supported, if not set protocol prefix default is HTTP, and HTTPS with no ssl check(verify=False)
# "192.168.3.4:8848" or "https://192.168.3.4:443" or "http://192.168.3.4:8848,192.168.3.5:8848" or "https://192.168.3.4:443,https://192.168.3.5:443"
SERVER_ADDRESSES = "server addresses split by comma"
NAMESPACE = "namespace id"

# no auth mode
client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)
# auth mode
# client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, ak="{ak}", sk="{sk}")

# get config
data_id = "config.nacos"
group = "group"
print(client.get_config(data_id, group))
```

## Configuration

```
client = NacosClient(server_addresses, namespace=your_ns, ak=your_ak, sk=your_sk)
```

-   _server\_addresses_ - **required** - Nacos server address, comma separated if more than 1.
-   _namespace_ - Namespace. | default: `None`
-   _ak_ - The accessKey to authenticate. | default: null
-   _sk_ - The secretKey to authentication. | default: null
-   _credentials\_provider_ - The custom access key manager | default: null
-   _log\_level_ - Log level. | default: null
-   _log\_rotation\_backup\_count_ - The number of log files to keep. | default: `7`

#### Extra Options

Extra option can be set by `set_options`, as following:

```
client.set_options({key}={value})
# client.set_options(proxies={"http":"192.168.3.50:809"})
```

Configurable options are:

-   _default\_timeout_ - Default timeout for get config from server in seconds.
-   _pulling\_timeout_ - Long polling timeout in seconds.
-   _pulling\_config\_size_ - Max config items number listened by one polling process.
-   _callback\_thread\_num_ - Concurrency for invoking callback.
-   _failover\_base_ - Dir to store failover config files.
-   _snapshot\_base_ - Dir to store snapshot config files.
-   _no\_snapshot_ - To disable default snapshot behavior, this can be overridden by param _no\_snapshot_ in _get_ method.
-   _proxies_ - Dict proxy mapping, some environments require proxy access, so you can set this parameter, this way http requests go through the proxy.

## API Reference

### Get Config

> `NacosClient.get_config(data_id, group, timeout, no_snapshot)`

-   `param` _data\_id_ Data id.
    
-   `param` _group_ Group, use `DEFAULT_GROUP` if no group specified.
    
-   `param` _timeout_ Timeout for requesting server in seconds.
    
-   `param` _no\_snapshot_ Whether to use local snapshot while server is unavailable.
    
-   `return` W Get value of one config item following priority:
    
-   Step 1 - Get from local failover dir(default: `${cwd}/nacos-data/data`).
    
    -   Failover dir can be manually copied from snapshot dir(default: `${cwd}/nacos-data/snapshot`) in advance.
    -   This helps to suppress the effect of known server failure.
-   Step 2 - Get from one server until value is got or all servers tried.
    
    -   Content will be save to snapshot dir after got from server.
-   Step 3 - Get from snapshot dir.
    

### Add Watchers

> `NacosClient.add_config_watchers(data_id, group, cb_list)`

-   `param` _data\_id_ Data id.
-   `param` _group_ Group, use `DEFAULT_GROUP` if no group specified.
-   `param` _cb\_list_ List of callback functions to add.
-   `return`

Add watchers to a specified config item.

-   Once changes or deletion of the item happened, callback functions will be invoked.
-   If the item is already exists in server, callback functions will be invoked for once.
-   Multiple callbacks on one item is allowed and all callback functions are invoked concurrently by `threading.Thread`.
-   Callback functions are invoked from current process.

### Remove Watcher

> `NacosClient.remove_config_watcher(data_id, group, cb, remove_all)`

-   `param` _data\_id_ Data id.
-   `param` _group_ Group, use "DEFAULT\_GROUP" if no group specified.
-   `param` _cb_ Callback function to delete.
-   `param` _remove\_all_ Whether to remove all occurrence of the callback or just once.
-   `return`

Remove watcher from specified key.

### Publish Config

> `NacosClient.publish_config(data_id, group, content, timeout)`

-   `param` _data\_id_ Data id.
-   `param` _group_ Group, use "DEFAULT\_GROUP" if no group specified.
-   `param` _content_ Config value.
-   `param` _timeout_ Timeout for requesting server in seconds.
-   `return` True if success or an exception will be raised.

Publish one data item to Nacos.

-   If the data key is not exist, create one first.
-   If the data key is exist, update to the content specified.
-   Content can not be set to None, if there is need to delete config item, use function **remove** instead.

### Remove Config

> `NacosClient.remove_config(data_id, group, timeout)`

-   `param` _data\_id_ Data id.
-   `param` _group_ Group, use "DEFAULT\_GROUP" if no group specified.
-   `param` _timeout_ Timeout for requesting server in seconds.
-   `return` True if success or an exception will be raised.

Remove one data item from Nacos.

### Register Instance

`NacosClient.add_naming_instance(service_name, ip, port, cluster_name, weight, metadata, enable, healthy,ephemeral,group_name,heartbeat_interval)`

-   `param` _service\_name_ **required** Service name to register to.
-   `param` _ip_ **required** IP of the instance.
-   `param` _port_ **required** Port of the instance.
-   `param` _cluster\_name_ Cluster to register to.
-   `param` _weight_ A float number for load balancing weight.
-   `param` _metadata_ Extra info in JSON string format or dict format
-   `param` _enable_ A bool value to determine whether instance is enabled or not.
-   `param` _healthy_ A bool value to determine whether instance is healthy or not.
-   `param` _ephemeral_ A bool value to determine whether instance is ephemeral or not.
-   `param` _heartbeat\_interval_ Auto daemon heartbeat interval in seconds.
-   `return` True if success or an exception will be raised.

### Deregister Instance

> `NacosClient.remove_naming_instance(service_name, ip, port, cluster_name)`

-   `param` _service\_name_ **required** Service name to deregister from.
-   `param` _ip_ **required** IP of the instance.
-   `param` _port_ **required** Port of the instance.
-   `param` _cluster\_name_ Cluster to deregister from.
-   `param` _ephemeral_ A bool value to determine whether instance is ephemeral or not.
-   `return` True if success or an exception will be raised.

### Modify Instance

> `NacosClient.modify_naming_instance(service_name, ip, port, cluster_name, weight, metadata, enable)`

-   `param` _service\_name_ **required** Service name.
-   `param` _ip_ **required** IP of the instance.
-   `param` _port_ **required** Port of the instance.
-   `param` _cluster\_name_ Cluster name.
-   `param` _weight_ A float number for load balancing weight.
-   `param` _metadata_ Extra info in JSON string format or dict format.
-   `param` _enable_ A bool value to determine whether instance is enabled or not.
-   `param` _ephemeral_ A bool value to determine whether instance is ephemeral or not.
-   `return` True if success or an exception will be raised.

### Query Instances

> `NacosClient.list_naming_instance(service_name, clusters, namespace_id, group_name, healthy_only)`

-   `param` _service\_name_ **required** Service name to query.
-   `param` _clusters_ Cluster names separated by comma.
-   `param` _namespace\_id_ Customized group name, default `blank`.
-   `param` _group\_name_ Customized group name , default `DEFAULT_GROUP`.
-   `param` _healthy\_only_ A bool value for querying healthy instances or not.
-   `return` Instance info list if success or an exception will be raised.

### Query Instance Detail

> `NacosClient.get_naming_instance(service_name, ip, port, cluster_name)`

-   `param` _service\_name_ **required** Service name.
-   `param` _ip_ **required** IP of the instance.
-   `param` _port_ **required** Port of the instance.
-   `param` _cluster\_name_ Cluster name.
-   `return` Instance info if success or an exception will be raised.

### Send Instance Beat

> `NacosClient.send_heartbeat(service_name, ip, port, cluster_name, weight, metadata)`

-   `param` _service\_name_ **required** Service name.
-   `param` _ip_ **required** IP of the instance.
-   `param` _port_ **required** Port of the instance.
-   `param` _cluster\_name_ Cluster to register to.
-   `param` _weight_ A float number for load balancing weight.
-   `param` _ephemeral_ A bool value to determine whether instance is ephemeral or not.
-   `param` _metadata_ Extra info in JSON string format or dict format.
-   `return` A JSON object include server recommended beat interval if success or an exception will be raised.

### Subscribe Service Instances Changed

> `NacosClient.subscribe(listener_fn, listener_interval=7, *args, **kwargs)`

-   `param` _listener\_fn_ **required** Customized listener function. with signature `fn_listener1(event, instance)->None`
-   `param` _listener\_interval_ Listen interval , default 7 second.
-   `param` _service\_name_ **required** Service name which subscribes.
-   `param` _clusters_ Cluster names separated by comma.
-   `param` _namespace\_id_ Customized group name, default `blank`.
-   `param` _group\_name_ Customized group name , default `DEFAULT_GROUP`.
-   `param` _healthy\_only_ A bool value for querying healthy instances or not.
-   `return`

### Unsubscribe Service Instances Changed

> `NacosClient.unsubscribe(service_name, listener_name)`

-   `param` _service\_name_ **required** Service name to subscribed.
-   `param` _listener\_name_ listener\_name which is customized.
-   `return`

### Stop All Service Subscribe

> `NacosClient.stop_subscribe()`

-   `return`

## Debugging Mode

Debugging mode if useful for getting more detailed log on console.

Debugging mode can be set by:

```
client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username=USERNAME, password=PASSWORD,log_level="DEBUG")
```