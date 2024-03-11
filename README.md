# get-jrecin-cookies
Get cookies for resource accesses authorized by jrec-in.

## Usage
```pop_email_address``` is the address where you receive the jrecin one-time code, and ```pop_email_password``` is the password for the email account that receives the jrecin one-time code. ```jrecin_address``` is your jrecin login address, and ```jrecin_password``` is your jrecin login password. It is recommended to use Outlook to receive the one-time code. If not using Outlook, you need to specify the address and port of the POP server(```pop_server、pop_port```).
### Build with Docker
Pull our built image directly.
```bash
$ docker pull godmountain/get-jrecin-cookies:latest
$ docker run --name jrecin -e pop_email_address="pop_email_address" \
                           -e pop_email_password="pop_email_password" \
                           -e jrecin_address="jrecin_address" \
                           -e jrecin_password="jrecin_password" godmountain/get-jrecin-cookies:latest
.
.
.
```
When the code execution ends.
```bash
$ docker cp jrecin:/APP/.env /your/local/path
$ cat /your/local/path/.env
```
## Notice!
Not for commercial use, for study purposes only.
