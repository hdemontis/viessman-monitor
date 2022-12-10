#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import stat, chown
from pathlib import Path
from datetime import datetime
from contextlib import ContextDecorator
from csv import DictWriter
from configparser import ConfigParser

from gazboiler import GazBoiler


class DataBase(ContextDecorator):
    
    fieldnames = [
        'date', 
        'heure',
        'temperature exterieure',
        'conso gaz chauffage',
        'conso gaz eau chaude',
        ]
    is_new = False
    
    def __init__(self, file, folder: Path = "."):
        folder.mkdir(exist_ok=True, parents=True)
        self.path = folder.joinpath(file)
        if not self.path.is_file():
            self.is_new = True
        self._fid = open(self.path, mode="a", newline='')
    
    def close(self):
        self.__exit__()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *exc):
        self._fid.close()
        st = stat(cwd())
        if st.st_uid is not None:
            for path in [self.path, self.path.parent]:
                chown(path, int(st.st_uid), int(st.st_gid))
    
    def append(self, data: dict):
        writer = DictWriter(self._fid, 
                            fieldnames=self.fieldnames)
        if self.is_new:
            writer.writeheader()
        writer.writerow(data)


def today():
    today = datetime.now()
    return today.date(), today.time()


def cwd(path: str = None):
    cwd = Path(__file__).parent
    if path is None:
        return cwd
    else:
        return cwd.joinpath(path)


def main(): 
    # --- lecture des parametres de connexion
    parser = ConfigParser()
    parser.read(cwd("config.ini"))
    
    # --- relevé température par chaudiere
    boiler = GazBoiler(**parser["viessmann"], 
                       token=cwd("token.save"))
    
    # --- relevé + écriture dans la base de donnée
    date, time = today()    # date et heure du jour
    with DataBase(folder=cwd("data"), 
                  file=f"monitor_{date.year}.csv") as db:
        db.append({
            "date": date.isoformat(),
            "heure": time.isoformat("seconds"),
            "temperature exterieure": boiler.outside_temperature, 
            "conso gaz chauffage": boiler.heating_consumption,
            "conso gaz eau chaude": boiler.hotwater_consumption,
        })


if __name__ == "__main__":
    main()