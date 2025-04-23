# cronvice

*maintain your programs running under SCREEN using AT job scheduler*

## Example

``` python
 # example
cronvice --help
```

## Installation

``` {.bash org-language="sh"}
# you need the scheduler
sudo  apt install at
# you nee the code (anti PEP 668 way)
pip3 install cronvice
```

All scripts must be in \~/.myservice/anyname/tag

-   where \~/.myservice is the S-PATH, path to scripts structure
-   anyname - can be number of different subfolders
-   tag must be a executable script with a uniqe name in all
    \~/.myservice
-   \~/.config/cronvice/cfg.json - contains the S-PATH (\"services\")
-   without a parameter, interactive tui is run, quit it with .q

## Usage

Harmless calls

``` example
cris l
cris t syncthing
cris p syncthing
cris c syncthing
```

-   r(un)
-   a(dd)
-   d(elete)
-   e(nter)
-   c(omment show)
-   t(ime show)
-   p(ath show)
-   l(ist cron)
-   x (block service call with impossible timestamp)
