# Viessman-monitor

A free alternative to ViCarePlus (https://www.viessmann.fr/fr/produits/connectivite/vicare-app/vicare-plus.html)

Read the doc from [PyViCare](https://github.com/somm15/PyViCare) before first use.

Credentials for logging to the [Viessmann Developer Portal](https://developer.viessmann.com/) are stored in a file called `config.ini` with :
```
[viessmann]
email=<your@email.fr>
password=<your-password>
client_id=<from-developer-portal>
```

Monitoring is performed by simply running the script `monitor.py`.  
> The task can be triggered periodically with `crontab`. For example, hourly :
> ```
> * */1 * * * cd /path/to/folder && /path/to/python monitor.py
> ```

Datas are saved in a CSV-type database, inside a directory next to `monitor.py`.
> The data directory is called by default `data`, and can be easily change in the script.
