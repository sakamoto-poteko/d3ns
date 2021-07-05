# D3NS

D3NS (Django Dynamic DNS) is aim to build a no-ip compatible dynamic DNS server. It has the following functionalities:
    - provides noip compatible http update interface with credential verification
    - provides web page for query dns records under a specific credential
    - stores dns records either in a local text file or in a database

## Interfaces

### Create a user

Before one can create or update a host's address, a credential must be obtained. Launch `GET /create_user` and the system will automatically create one for you. Record your id and key and keep them in a safe place.

### Create and update a host

Visit `GET nic/update?hostname=your_host_name&myip=ip_address` to create a host. Note the user id and key must be attached as basic authentication so the host can be created or updated. If the credential is incorrect or not being passed, `403 Forbidded` will be returned.

### Query all my hosts

Index page `GET /` and `GET /query_hosts` will return all hosts a user has. Same as create/update host, the credential must be passed.

### Query a single host

`GET /host?hostname=your_host_name` returns the ip address of this host. Anyone with hostname can access this interface and no credential is required. If a host does not exist, `404 Not Found` will be returned.

## Models

Two models are adopted. One is `Credential` and the other one is `Host`. For the sake of simplicity, our homebrewed `Credential` model is used for user authentication, instead of those provided by Django framework. The `Credential` is rather simple, containing only `id` and `key` two fields. Both of them are UUID. `Host` model has `hostname`, `address`, `updated` and `user` fields. While `updated` is the last update timestamp, it's not shown anywhere in UX. `user` field is a foreign key to `Credential`.