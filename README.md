# Logs Browser
Script that gives informations extracted from Minecraft server log files
## Prerequisites
- Python ≥ 3.9
- Minecraft server logs
## Install
```bash
git clone https://github.com/VictorEgret/Logs-Browser.git
cd Logs-Browser
python browser.py [logs folder path]
```
## Output
Format: \<UUID> \<Username> \<Time> \<Address:Port> \<File path>
```
➜  Logs-Browser git:(main) ✗ python3.10 browser.py example_logs
Logs data browser by solvictor for Minecraft 1.19.3
abcdef01-abcd-abcd-abcd-abcdef012345 User 19:15:35 127.0.0.1:55953 example_logs/2022-10-11-7.log.gz
                                          19:25:57 127.0.0.1:57327 example_logs/latest.log
```
